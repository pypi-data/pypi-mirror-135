import asyncio
import socket
from abc import abstractmethod
from functools import partial
from typing import Any, Optional

from ..utils import OptionsType, awaitable, bind_socket
from .base import SimpleServer


class TCPServer(SimpleServer):
    PROTO_NAME = "tcp"

    def __init__(
        self, address: str = None, port: int = None,
        options: OptionsType = (), sock: socket.socket = None, **kwargs: Any
    ):
        if not sock:
            if not (address and port):
                raise RuntimeError(
                    "You should pass socket instance or "
                    '"address" and "port" couple',
                )

            self.make_socket = partial(
                bind_socket,
                address=address,
                port=port,
                options=options,
            )
        elif not isinstance(sock, socket.socket):
            raise ValueError("sock must be socket instance")
        else:
            self.make_socket = lambda: sock     # type: ignore

        self.socket: Optional[socket.socket] = None

        super().__init__(**kwargs)

    @abstractmethod
    async def handle_client(
        self, reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> Any:
        raise NotImplementedError

    def make_client_handler(
        self, reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> Any:
        return self.create_task(awaitable(self.handle_client)(reader, writer))

    async def start(self) -> None:
        self.socket = self.make_socket()
        self.server = await asyncio.start_server(
            self.make_client_handler,
            sock=self.socket,
        )

    async def stop(self, exc: Exception = None) -> None:
        await super().stop(exc)

        if self.server:
            await self.server.wait_closed()
