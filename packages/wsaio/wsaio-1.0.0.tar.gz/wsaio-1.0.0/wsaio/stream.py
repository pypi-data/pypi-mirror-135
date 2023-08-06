from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable, Generator, Optional

StreamParserT = Callable[['StreamReader'], Generator[None, None, None]]
StreamErrorHandlerT = Callable[[Exception], Awaitable[None]]
ClosedCallbackT = Callable[[Optional[asyncio.Future[None]]], None]


class StreamProtocol(asyncio.Protocol):
    def __init__(self, stream: Stream) -> None:
        self.stream = stream
        self.loop = self.stream.loop

        self._paused = False
        self._connection_lost = False

        self._drain_waiter = None
        self._close_waiter = self.loop.create_future()

        self.transport = None

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self.transport = transport

    def pause_writing(self) -> None:
        assert not self._paused
        self._paused = True

    def resume_writing(self) -> None:
        assert self._paused
        self._paused = False

        if self._drain_waiter is not None:
            if not self._drain_waiter.done():
                self._drain_waiter.set_result(None)

            self._drain_waiter = None

    def connection_lost(self, exc: Optional[Exception]) -> None:
        if self._paused and self._drain_waiter is not None:
            if not self._drain_waiter.done():
                if exc is not None:
                    self._drain_waiter.set_exception(exc)
                else:
                    self._drain_waiter.set_result(None)

        if not self._close_waiter.done():
            if exc is not None:
                self._close_waiter.set_exception(exc)
            else:
                self._close_waiter.set_result(None)

    def data_received(self, data: bytes) -> None:
        self.stream.feed_data(data)

    def eof_received(self) -> Optional[bool]:
        self.stream.feed_eof()
        assert self.transport is not None

        ctx = self.transport.get_extra_info('ssl_context')
        return ctx is not None

    def add_closed_callback(self, callback: ClosedCallbackT) -> None:
        self._close_waiter.add_done_callback(callback)

    async def wait_for_drain(self) -> None:
        if self._close_waiter.done():
            raise ConnectionResetError('Connection lost')

        if self._paused:
            assert (
                self._drain_waiter is None
                or self._drain_waiter.done()
            )

            self._drain_waiter = self.loop.create_future()
            await self._drain_waiter

    async def wait_for_close(self) -> None:
        await self._close_waiter


class StreamReader:
    def __init__(self, stream: Stream) -> None:
        self.stream = stream
        self.buffer = bytearray()
        self.parser = None

    def set_parser(self, parser: Optional[StreamParserT]) -> None:
        if parser is not None:
            self.parser = parser(self)
            self.step_parser(None)
        else:
            self.parser = None

    def step_parser(self, data: Optional[bytes]) -> None:
        if data is not None:
            self.buffer.extend(data)

        if self.parser is not None:
            try:
                self.parser.send(None)
            except StopIteration:
                pass
            except Exception as exc:
                self.stream.call_error_handler(exc)

    def fill(self) -> Generator[None, None, None]:
        yield

    def read(self, n: int) -> Generator[None, None, bytes]:
        while len(self.buffer) < n:
            yield from self.fill()

        data = self.buffer[:n]
        del self.buffer[:n]

        return bytes(data)


class Stream:
    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        self.transport: Optional[asyncio.Transport] = None
        self.protocol: Optional[StreamProtocol] = None
        self.connected = False

        self._reader = StreamReader(self)
        self._error_handler = None

    async def create_connection(self, host: str, post: int, **kwargs: Any) -> None:
        transport, protocol = await self.loop.create_connection(
            lambda: StreamProtocol(self), host, post, **kwargs
        )

        assert isinstance(transport, asyncio.Transport)
        assert isinstance(protocol, StreamProtocol)

        self.transport, self.protocol = transport, protocol
        self.connected = True

    def feed_data(self, data: bytes) -> None:
        self._reader.step_parser(data)

    def feed_eof(self) -> None:
        return None

    def set_parser(self, parser: Optional[StreamParserT]) -> None:
        self._reader.set_parser(parser)

    def set_error_handler(self, handler: StreamErrorHandlerT) -> None:
        self._error_handler = handler

    def call_error_handler(self, exc: Exception) -> None:
        if self._error_handler is not None:
            self.loop.create_task(self._error_handler(exc))
        else:
            self.loop.call_exception_handler({
                'message': 'Unhandled exception in stream',
                'exception': exc,
                'stream': self,
            })

    def write(self, data: bytes) -> None:
        if not self.connected:
            raise RuntimeError('cannot write to stream because it is not connected')

        assert self.transport is not None

        self.transport.write(data)

    def add_closed_callback(self, callback: ClosedCallbackT) -> None:
        if not self.connected:
            raise RuntimeWarning(
                'cannot add closed callback because stream is not connected'
            )

        assert self.protocol is not None

        self.protocol.add_closed_callback(callback)

    async def close(self) -> None:
        if not self.connected:
            raise RuntimeError('cannot close stream because it is not connected')

        assert (
            self.transport is not None
            and self.protocol is not None
        )

        if not self.transport.is_closing():
            self.transport.close()

        await self.protocol.wait_for_close()

    async def drain(self) -> None:
        if self.protocol is not None:
            await self.protocol.wait_for_drain()
