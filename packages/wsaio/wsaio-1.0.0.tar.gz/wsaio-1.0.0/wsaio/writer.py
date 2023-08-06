from __future__ import annotations

from typing import Optional, Union

from . import secrets
from .frame import WebSocketCloseCode, WebSocketFrame, WebSocketOpcode
from .stream import Stream


class WebSocketWriter:
    def __init__(self, stream: Stream) -> None:
        self.stream = stream

    def compile_frame(self, frame: WebSocketFrame, *, mask: bool = True) -> bytes:
        frame.validate()

        if isinstance(frame.data, str):
            data = frame.data.encode('utf-8')
        else:
            data = frame.data

        mask_bit = mask << 7
        length = len(data)

        buffer = bytearray((frame.head, 0))

        if length < 126:
            buffer[1] = mask_bit | length
        elif length < (1 << 16):
            buffer[1] = mask_bit | 126
            buffer.extend(length.to_bytes(2, 'big', signed=False))
        else:
            buffer[1] = mask_bit | 127
            buffer.extend(length.to_bytes(8, 'big', signed=False))

        if frame.code is not None:
            data = frame.code.to_bytes(2, 'big', signed=False) + data

        if mask:
            secmask = secrets.genmask()
            buffer.extend(secmask)
            buffer.extend(secrets.mask(data, secmask))
        else:
            buffer.extend(data)

        return bytes(buffer)

    async def write_frame(self, frame: WebSocketFrame, *, mask: bool = True) -> None:
        self.stream.write(self.compile_frame(frame, mask=mask))
        await self.stream.drain()

    async def ping(
        self, data: Optional[Union[str, bytes]] = None, *, mask: bool = False
    ) -> None:
        frame = WebSocketFrame(WebSocketOpcode.PING, data=data)
        await self.write_frame(frame, mask=mask)

    async def pong(
        self, data: Optional[Union[str, bytes]] = None, *, mask: bool = False
    ) -> None:
        frame = WebSocketFrame(WebSocketOpcode.PONG, data=data)
        await self.write_frame(frame, mask=mask)

    async def close(
        self,
        data: Optional[Union[str, bytes]] = None,
        *,
        code: int = WebSocketCloseCode.NORMAL_CLOSURE,
        mask: bool = False
    ) -> None:
        frame = WebSocketFrame(WebSocketOpcode.CLOSE, data=data, code=code)
        await self.write_frame(frame, mask=mask)

    async def send(
        self,
        data: Optional[Union[str, bytes]] = None,
        *,
        binary: bool = False,
        mask: bool = False
    ) -> None:
        frame = WebSocketFrame(
            WebSocketOpcode.BINARY if binary else WebSocketOpcode.TEXT, data=data
        )
        await self.write_frame(frame, mask=mask)
