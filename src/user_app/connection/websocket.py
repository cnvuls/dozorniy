from __future__ import annotations

import asyncio
import logging
from typing import Optional

import websockets
from connection.abstracts import ConnectionBase
from core.events import EventBus, ReceiveMessage, SendMessage


class WebsocketConnection(ConnectionBase):
    def __init__(
        self,
        bus: EventBus,
        port: int,
        ip: str,
        name: str,
        reconnect_delay: float = 3.0,
    ) -> None:
        super().__init__(bus, port, ip, name)
        self.bus = bus
        self.port = port
        self.ip = ip
        self.name = name
        self.reconnect_delay = reconnect_delay
        self.logger = logging.getLogger("client.connection")
        self.socket: Optional[websockets.ClientConnection] = None
        self.bus.subscribe(SendMessage, self.send_message)

    async def send_message(self, event: SendMessage) -> None:
        if self.socket is None:
            self.logger.warning("Попытка отправить сообщение при отсутствующем сокете.")
            return
        await self.socket.send(event.text)

    async def receive_message(self, data: str) -> None:
        print("_______________________________")
        await self.bus.publish(ReceiveMessage(text=data))

    async def main_loop(self) -> None:
        while True:
            try:
                async with websockets.connect(f"ws://{self.ip}:{self.port}") as sock:
                    self.socket = sock
                    await sock.send(f"{self.name}")
                    self.logger.info(
                        "Соединение установлено с %s:%s", self.ip, self.port
                    )
                    async for raw in sock:
                        await self.receive_message(str(raw))
            except Exception as exc:
                self.logger.warning("Проблемы с соединением: %s", exc)
                await asyncio.sleep(self.reconnect_delay)

    def _is_socket_ready(self) -> bool:
        if not self.socket:
            return False
        try:
            closed_attr = getattr(self.socket, "closed")
        except AttributeError:
            return True
        if callable(closed_attr):
            try:
                closed_value = closed_attr()
            except TypeError:
                closed_value = False
        else:
            closed_value = closed_attr
        return not bool(closed_value)
