from codecs import IncrementalDecoder, getincrementaldecoder
from contextlib import contextmanager
from io import BytesIO, StringIO
from typing import Awaitable, Callable, Generator, Optional, Union

from . import secrets
from .exceptions import FrameDecodeError
from .frame import WebSocketCloseCode, WebSocketFrame, WebSocketOpcode
from .stream import Stream, StreamReader

_INVALID_OPCODE_MSG = 'The WebSocket received a frame with an invalid or unknown opcode: {!r}'
_MISSING_CLOSE_CODE_MSG = 'The WebSocket received a close frame with payload data but no close code'
_INVALID_CLOSE_CODE_MSG = (
    'The WebSocket received a close frame with an invalid or unknown close code: {!r}'
)

_INVALID_LENGTH_MSG = (
    'The WebSocket received a frame with an invalid non-extended payload length: {!r}'
)
_LARGE_CONTROL_MSG = (
    'The WebSocket received a control frame with a payload length that exceeds 125: {!r}'
)

_FRAGMENTED_CONTROL_MSG = 'The WebSocket received a fragmented control frame'
_MEANINGLESS_RSV_BITS_MSG = (
    'The WebSocket received a frame with a reserved bit set but no meaning was negotiated'
)
_NON_UTF_8_MSG = 'The WebSocket received a text or close frame with non-UTF-8 payload data'

_EXPECTED_CONT_MSG = (
    'The WebSocket received a non-continuation data frame while reading a fragmented frame'
)
_UNEXPECTED_CONT_MSG = (
    'The WebSocket received a continuation frame but no fragmented frame was received'
)

_IncrementalDecoder = getincrementaldecoder('utf-8')

PingCallbackT = Callable[[bytes], Awaitable[None]]
PongCallbackT = Callable[[bytes], Awaitable[None]]
TextCallbackT = Callable[[str], Awaitable[None]]
BinaryCallbackT = Callable[[bytes], Awaitable[None]]
CloseCallbackT = Callable[[bytes, int], Awaitable[None]]


class WebSocketReader:
    def __init__(self, stream: Stream) -> None:
        self.stream = stream

        self.on_ping: Optional[PingCallbackT] = None
        self.on_pong: Optional[PongCallbackT] = None
        self.on_text: Optional[TextCallbackT] = None
        self.on_binary: Optional[BinaryCallbackT] = None
        self.on_close: Optional[CloseCallbackT] = None

        self._fragment_buffer: Optional[Union[StringIO, BytesIO]] = None
        self._fragment_decoder: Optional[IncrementalDecoder] = None
        self._fragmented_frame: Optional[WebSocketFrame] = None

    def _run_callback(self, frame: WebSocketFrame) -> None:
        if frame.opcode == WebSocketOpcode.PING:
            assert self.on_ping is not None
            coro = self.on_ping(frame.get_bytes())

        elif frame.opcode == WebSocketOpcode.PONG:
            assert self.on_pong is not None
            coro = self.on_pong(frame.get_bytes())

        elif frame.opcode == WebSocketOpcode.TEXT:
            assert self.on_text is not None
            coro = self.on_text(frame.get_string())

        elif frame.opcode == WebSocketOpcode.BINARY:
            assert self.on_binary is not None
            coro = self.on_binary(frame.get_bytes())

        elif frame.opcode == WebSocketOpcode.CLOSE:
            assert self.on_close is not None
            assert frame.code is not None
            coro = self.on_close(frame.get_bytes(), frame.code)

        else:
            raise ValueError('Invalid frame opcode')

        self.stream.loop.create_task(coro)

    @contextmanager
    def _catch_decode_error(self):
        try:
            yield
        except UnicodeDecodeError:
            raise FrameDecodeError(_NON_UTF_8_MSG, WebSocketCloseCode.INVALID_PAYLOAD_DATA)

    def _init_fragmenter(self, frame: WebSocketFrame, data: bytes) -> None:
        self._fragmented_frame = frame

        if frame.opcode == WebSocketOpcode.TEXT:
            self._fragment_buffer = StringIO()
            self._fragment_decoder = _IncrementalDecoder()
        else:
            self._fragment_buffer = BytesIO()

        self._write_fragment(data)

    def _write_fragment(self, data: bytes) -> None:
        assert self._fragmented_frame is not None

        if self._fragmented_frame.opcode == WebSocketOpcode.TEXT:
            assert isinstance(self._fragment_buffer, StringIO)
            assert self._fragment_decoder is not None

            self._fragment_buffer.write(self._fragment_decoder.decode(data))
        else:
            assert isinstance(self._fragment_buffer, BytesIO)

            self._fragment_buffer.write(data)

    def _reset_fragmenter(self) -> None:
        self._fragment_buffer = None
        self._fragment_decoder = None
        self._fragmented_frame = None

    def frame_parser(self, reader: StreamReader) -> Generator[None, None, None]:
        while True:
            fbyte, sbyte = yield from reader.read(2)

            masked = (sbyte >> 7) & 1
            length = sbyte & ~(1 << 7)

            frame = WebSocketFrame.from_head(fbyte)

            try:
                WebSocketOpcode(frame.opcode)
            except ValueError:
                raise FrameDecodeError(
                    _INVALID_OPCODE_MSG.format(frame.opcode), WebSocketCloseCode.PROTOCOL_ERROR
                )

            if any((frame.rsv1, frame.rsv2, frame.rsv3)):
                raise FrameDecodeError(
                    _MEANINGLESS_RSV_BITS_MSG, WebSocketCloseCode.PROTOCOL_ERROR
                )

            if frame.is_control():
                yield from self._handle_control_frame(reader, frame, masked, length)
            else:
                yield from self._handle_data_frame(reader, frame, masked, length)

    def _read_length(self, reader: StreamReader, bits: int) -> Generator[None, None, int]:
        if bits == 126:
            data = yield from reader.read(2)
        elif bits == 127:
            data = yield from reader.read(8)
        else:
            if bits > 127:  # XXX: Is this even possible?
                raise FrameDecodeError(_INVALID_LENGTH_MSG, WebSocketCloseCode.PROTOCOL_ERROR)

            return bits

        return int.from_bytes(data, 'big', signed=False)

    def _read_payload(
        self, reader: StreamReader, length: int, masked: int
    ) -> Generator[None, None, bytes]:
        if masked:
            mask = yield from reader.read(4)
            data = yield from reader.read(length)
            return secrets.mask(data, mask)

        data = yield from reader.read(length)
        return data

    def _set_close_code(self, frame: WebSocketFrame, data: bytes) -> bytes:
        if not data:
            frame.set_code(WebSocketCloseCode.GOING_AWAY)
            return b''
        elif len(data) < 2:
            raise FrameDecodeError(_MISSING_CLOSE_CODE_MSG, WebSocketCloseCode.PROTOCOL_ERROR)

        code = int.from_bytes(data[:2], 'big', signed=False)

        try:
            WebSocketCloseCode.from_code(code)
        except ValueError:
            raise FrameDecodeError(
                _INVALID_CLOSE_CODE_MSG.format(code), WebSocketCloseCode.PROTOCOL_ERROR
            )

        frame.set_code(code)
        return data[2:]

    def _handle_control_frame(
        self, reader: StreamReader, frame: WebSocketFrame, masked: int, length: int
    ) -> Generator[None, None, None]:
        if not frame.fin:
            raise FrameDecodeError(_FRAGMENTED_CONTROL_MSG, WebSocketCloseCode.PROTOCOL_ERROR)

        if length > 125:
            raise FrameDecodeError(
                _LARGE_CONTROL_MSG.format(length), WebSocketCloseCode.PROTOCOL_ERROR
            )

        data = yield from self._read_payload(reader, length, masked)

        if frame.opcode == WebSocketOpcode.CLOSE:
            data = self._set_close_code(frame, data)

            with self._catch_decode_error():
                frame.set_data(data.decode('utf-8'))
        else:
            frame.set_data(data)

        self._run_callback(frame)

    def _handle_data_frame(
        self, reader: StreamReader, frame: WebSocketFrame, masked: int, length: int
    ) -> Generator[None, None, None]:
        length = yield from self._read_length(reader, length)
        data = yield from self._read_payload(reader, length, masked)

        if frame.opcode == WebSocketOpcode.CONTINUATION:
            if self._fragmented_frame is None:
                raise FrameDecodeError(_UNEXPECTED_CONT_MSG, WebSocketCloseCode.PROTOCOL_ERROR)

            with self._catch_decode_error():
                self._write_fragment(data)

        elif self._fragmented_frame is not None:
            raise FrameDecodeError(_EXPECTED_CONT_MSG, WebSocketCloseCode.PROTOCOL_ERROR)

        if not frame.fin:
            if self._fragmented_frame is None:
                with self._catch_decode_error():
                    self._init_fragmenter(frame, data)
        else:
            if self._fragmented_frame is not None:
                assert self._fragment_buffer is not None
                assert self._fragmented_frame is not None

                frame = self._fragmented_frame
                data = self._fragment_buffer.getvalue()
                self._reset_fragmenter()

            elif frame.opcode == WebSocketOpcode.TEXT:
                with self._catch_decode_error():
                    data = data.decode('utf-8')

            frame.set_data(data)
            self._run_callback(frame)
