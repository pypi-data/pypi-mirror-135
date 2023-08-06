from __future__ import annotations

import asyncio
from typing import Any, Optional, Union

from .exceptions import FrameDecodeError, HandshakeFailureError
from .frame import WebSocketCloseCode
from .handshake import WebSocketHandshake
from .reader import WebSocketReader
from .writer import WebSocketWriter


class WebSocketProtocol:
    async def on_open(self) -> None:
        pass

    async def on_ping(self, data: bytes) -> None:
        pass

    async def on_pong(self, data: bytes) -> None:
        pass

    async def on_text(self, data: str) -> None:
        pass

    async def on_binary(self, data: bytes) -> None:
        pass

    async def on_close(self, data: bytes, code: int) -> None:
        pass

    async def on_closed(self, exc: Optional[BaseException]) -> None:
        pass


class WebSocketClient(WebSocketProtocol):
    def __init__(self, *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        self.loop = loop

        self.stream = None
        self.reader = None
        self.writer = None

        self._opened = True
        self._closing = False

    def is_opened(self) -> bool:
        return self._opened

    def is_closing(self) -> bool:
        return self._closing

    async def _ping_hook(self, data: bytes) -> None:
        await self.pong(data)
        await self.on_ping(data)

    async def _close_hook(self, data: bytes, code: int) -> None:
        if not self.is_closing():
            await self.close(code=code)
        else:
            assert self.stream is not None
            await self.stream.close()

        await self.on_close(data, code)

    async def _error_hook(self, exc: Exception) -> None:
        if isinstance(exc, FrameDecodeError):
            if not self.is_closing():
                await self.close(exc.message, code=exc.code)

        await self.stream.close()

    def _closed_hook(self, future: asyncio.Future[None]) -> None:
        self._opened = False

        assert self.loop is not None
        self.loop.create_task(self.on_closed(future.exception()))

    async def ping(self, data: Optional[Union[str, bytes]] = None) -> None:
        if not self.is_opened():
            raise RuntimeError('The WebSocket is not opened')

        assert self.writer is not None
        await self.writer.ping(data, mask=True)

    async def pong(self, data: Optional[Union[str, bytes]] = None) -> None:
        if not self.is_opened():
            raise RuntimeError('The WebSocket is not opened')

        assert self.writer is not None
        await self.writer.pong(data, mask=True)

    async def send(self, data: Optional[Union[str, bytes]], *, binary: bool = False) -> None:
        if not self.is_opened():
            raise RuntimeError('The WebSocket is not opened')

        assert self.writer is not None
        await self.writer.send(data, binary=binary, mask=True)

    async def close(
        self,
        data: Optional[Union[str, bytes]] = None,
        *,
        code: int = WebSocketCloseCode.NORMAL_CLOSURE
    ) -> None:
        if not self.is_opened():
            raise RuntimeError('The WebSocket is not opened')

        if self.is_closing():
            raise RuntimeError('The WebSocket is already closing')

        self._closing = True

        assert self.writer is not None
        await self.writer.close(data, code=code, mask=True)

    async def connect(self, url: str, *, timeout: float = 10, **kwargs: Any) -> None:
        if self.loop is None:
            self.loop = asyncio.get_running_loop()

        handshake = await WebSocketHandshake.from_url(url, self.loop, **kwargs)

        try:
            await handshake.negotiate(timeout=timeout)
        except HandshakeFailureError:
            await handshake.stream.close()
            raise

        self.stream = handshake.stream

        self.reader = WebSocketReader(self.stream)
        self.writer = WebSocketWriter(self.stream)

        self.reader.on_ping = self._ping_hook
        self.reader.on_pong = self.on_pong
        self.reader.on_text = self.on_text
        self.reader.on_binary = self.on_binary
        self.reader.on_close = self._close_hook

        self._opened = True
        self.loop.create_task(self.on_open())

        self.stream.add_closed_callback(self._closed_hook)
        self.stream.set_error_handler(self._error_hook)
        self.stream.set_parser(self.reader.frame_parser)
