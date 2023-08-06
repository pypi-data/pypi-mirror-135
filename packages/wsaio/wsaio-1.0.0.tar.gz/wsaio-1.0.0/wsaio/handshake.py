from __future__ import annotations

import asyncio
from http import HTTPStatus
from io import StringIO
from typing import Any, Generator, TYPE_CHECKING, Tuple
from urllib.parse import urlparse

from . import hdrs
from . import secrets
from .exceptions import HandshakeFailureError
from .stream import Stream, StreamReader

if TYPE_CHECKING:
    from typing_extensions import Self

URLInfo = Tuple[str, int, str, str]


class WebSocketHandshake:
    def __init__(self, stream: Stream, url: URLInfo) -> None:
        self.stream = stream
        (
            self.host,
            self.port,
            self.path,
            self.query,
        ) = url

        self.status = None
        self.headers = hdrs.HTTPHeaders()

        self._complete = self.stream.loop.create_future()

    @classmethod
    async def from_url(cls, url: str, loop: asyncio.AbstractEventLoop, **kwargs: Any) -> Self:
        parsed = urlparse(url)

        if parsed.scheme not in ('ws', 'wss'):
            raise ValueError(f'URL scheme should be ws or wss, not {parsed.scheme!r}')

        hostname = parsed.hostname
        if hostname is None:
            raise ValueError('URL host name should not be None')

        port = parsed.port
        if port is None:
            if parsed.scheme == 'wss':
                port = 443
                kwargs.setdefault('ssl', True)
            else:
                port = 80

        path = parsed.path or '/'

        query = parsed.query
        if query:
            query = f'?{query}'

        stream = Stream(loop)
        await stream.create_connection(hostname, port, **kwargs)

        return cls(stream, (hostname, port, path, query))

    def sanitize(self, value: bytes) -> str:
        return value.strip().decode('utf-8')

    def response_parser(self, reader: StreamReader) -> Generator[None, None, None]:
        start = 0

        while True:
            index = reader.buffer.find(b'\r\n', start)
            if index == -1:
                yield from reader.fill()
            else:
                if self.status is None:
                    self.status = reader.buffer[start:index].decode('utf-8')
                else:
                    key, value = reader.buffer[start:index].split(b':', 1)
                    self.headers[self.sanitize(key)] = self.sanitize(value)

                start = index + 2

                if reader.buffer[start:start + 2] == b'\r\n':
                    del reader.buffer[:start + 2]
                    break

        self.stream.set_parser(None)
        self._complete.set_result(None)

    async def error_handler(self, exc: Exception) -> None:
        self._complete.set_exception(exc)

    async def negotiate(self, *, timeout: float = 10) -> None:
        seckey = secrets.genseckey()
        acckey = secrets.genacckey(seckey.encode('utf-8'))

        headers: dict[str, str] = {}

        headers[hdrs.HOST] = f'{self.host}:{self.port}'
        headers[hdrs.CONNECTION] = 'Upgrade'
        headers[hdrs.UPGRADE] = 'websocket'
        headers[hdrs.SEC_WEBSOCKET_KEY] = seckey
        headers[hdrs.SEC_WEBSOCKET_VERSION] = '13'

        buffer = StringIO()

        buffer.write(f'GET {self.path}{self.query} HTTP/1.1\r\n')

        for key, value in headers.items():
            buffer.write(f'{key}: {value}\r\n')

        buffer.write('\r\n')

        self.stream.set_parser(self.response_parser)
        self.stream.set_error_handler(self.error_handler)

        self.stream.write(buffer.getvalue().encode('utf-8'))

        try:
            await asyncio.wait_for(self._complete, timeout)
        except asyncio.TimeoutError:
            raise HandshakeFailureError('The handshake timed out while waiting for response')

        assert self.status is not None
        version, code, _ = self.status.split(' ', 2)

        if version != 'HTTP/1.1':
            raise HandshakeFailureError(f'Expected HTTP/1.1, got {version}')

        if code != str(HTTPStatus.SWITCHING_PROTOCOLS.value):
            raise HandshakeFailureError(f'Expected status code 101, got {code}')

        if self.headers.getone(hdrs.CONNECTION).lower() != 'upgrade':
            raise HandshakeFailureError(f'The {hdrs.CONNECTION!r} header is not \'upgrade\'')

        if self.headers.getone(hdrs.UPGRADE).lower() != 'websocket':
            raise HandshakeFailureError(f'The {hdrs.UPGRADE!r} header is not \'websocket\'')

        if self.headers.getone(hdrs.SEC_WEBSOCKET_ACCEPT) != acckey:
            raise HandshakeFailureError(
                f'The {hdrs.SEC_WEBSOCKET_ACCEPT!r} header does not match the secret key'
            )
