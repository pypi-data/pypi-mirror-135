from __future__ import annotations

import enum
from typing import Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from typing_extensions import Self


class WebSocketOpcode(enum.IntEnum):
    CONTINUATION = 0x0
    TEXT = 0x1
    BINARY = 0x2
    CLOSE = 0x8
    PING = 0x9
    PONG = 0xA


class WebSocketCloseCode(enum.IntEnum):
    message: str

    def __new__(cls, value: int, message: str):
        self = int.__new__(cls, value)
        self._value_ = value

        self.message = message
        return self

    NORMAL_CLOSURE = 1000, 'Normal Closure'
    GOING_AWAY = 1001, 'Going Away'
    PROTOCOL_ERROR = 1002, 'Protocol Error'
    UNSUPPORTED_DATA = 1003, 'Unsupported Data'
    NO_STATUS_RECEIVED = 1005, 'No Status Received'
    ABNORMAL_CLOSURE = 1006, 'Abnormal Closure'
    INVALID_PAYLOAD_DATA = 1007, 'Invalid Payload Data'
    POLICY_VIOLATION = 1008, 'Policy Violation'
    MESSAGE_TOO_BIG = 1009, 'Message Too Big'
    MANDATORY_EXTENSION = 1010, 'Mandatory Extension'
    INTERNAL_SERVER_ERROR = 1011, 'Internal Server Error'
    TLS_HANDSHAKE = 1015, 'TLS Handshake'

    @classmethod
    def from_code(cls, code: int):
        try:
            return cls(code)
        except ValueError:
            if not 3000 <= code <= 4999:
                raise TypeError(f'Invalid WebSocketCloseCode: {code!r}')

            return code


class WebSocketFrame:
    __slots__ = ('head', 'data', 'code')

    def __init__(
        self,
        opcode: WebSocketOpcode,
        *,
        data: Optional[Union[str, bytes]],
        code: Optional[int] = None,
    ) -> None:
        self.head = int(opcode)
        self.set_fin(True)
        self.set_data(data)
        self.set_code(code)

    @classmethod
    def from_head(cls, head: int) -> Self:
        self = cls.__new__(cls)
        self.head = head
        return self

    @property
    def opcode(self) -> int:
        return self.head & 0xF

    @property
    def fin(self) -> int:
        return (self.head >> 7) & 1

    @property
    def rsv1(self) -> int:
        return (self.head >> 6) & 1

    @property
    def rsv2(self) -> int:
        return (self.head >> 5) & 1

    @property
    def rsv3(self) -> int:
        return (self.head >> 4) & 1

    def set_opcode(self, op: WebSocketOpcode) -> None:
        self.head |= op

    def set_fin(self, value: int) -> None:
        self.head |= value << 7

    def set_rsv1(self, value: int) -> None:
        self.head |= value << 6

    def set_rsv2(self, value: int) -> None:
        self.head |= value << 5

    def set_rsv3(self, value: int) -> None:
        self.head |= value << 4

    def set_code(self, code: Optional[int]):
        self.code = int(code) if code is not None else None

    def set_data(self, data: Optional[Union[str, bytes]]) -> None:
        if data is not None:
            self.data = data
        else:
            self.data = b''

    def get_string(self) -> str:
        if isinstance(self.data, bytes):
            return self.data.decode('utf-8')
        else:
            return self.data

    def get_bytes(self) -> bytes:
        if isinstance(self.data, str):
            return self.data.encode('utf-8')
        else:
            return self.data

    def is_control(self) -> bool:
        return self.opcode > 0x7

    def validate(self) -> None:
        try:
            opcode = WebSocketOpcode(self.opcode)
        except ValueError:
            raise ValueError(f'Frame has invalid opcode: {self.opcode!r}')

        if opcode is WebSocketOpcode.TEXT:
            if isinstance(self.data, bytes):
                self.data = self.data.decode('utf-8')

        if self.is_control():
            length = len(self.data)
            if self.code is not None:
                length += 2

            if length > 125:
                raise ValueError(f'Control frame length exceeds 125: {length}')

            if not self.fin:
                raise ValueError('Control frame is fragmented')

        if self.code is not None:
            if opcode is not WebSocketOpcode.CLOSE:
                raise ValueError('Non-close frame has close code')

            self.code = WebSocketCloseCode.from_code(self.code)
