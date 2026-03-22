import asyncio
import socket
from typing import Dict

import websockets
from websockets import serve

from connection.abstracts import ConnectionBase
from core.events import (
    EventBus,
    IncomingRawMessage,
    InfoLogEvent,
    SendingCommand,
    UpdateUserEvent,
)
from core.events.base import AbstractEvent


def get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


class GetInitialUsersEvent(AbstractEvent):
    pass


class WebSocketConnection(ConnectionBase):
    def __init__(self, bus: EventBus) -> None:
        self._clients: Dict[int, dict] = {}
        self.bus = bus
        self._server_instance = None
        self._stop_event = None

        self.bus.subscribe(SendingCommand, self.send_message)

    async def send_message(self, event: SendingCommand) -> None:
        client_data = self._clients.get(event.user_id)
        if client_data:
            await client_data["socket"].send(event.text)

    async def register_client(self, socket: websockets.ServerConnection) -> int:
        user_name = str(await socket.recv())
        user_id = len(self._clients) + 1
        self._clients[user_id] = {"socket": socket, "name": user_name}
        await self.bus.publish(
            UpdateUserEvent(action="connect", user_id=user_id, user_name=user_name)
        )
        return user_id

    async def broadcast_message(self, text: str) -> None:
        if self._clients:
            await asyncio.gather(
                *[data["socket"].send(text) for _, data in self._clients.values()],
                return_exceptions=True,
            )

    async def unregister_client(self, client_id: int) -> None:
        if client_id in self._clients:
            self._clients.pop(client_id)
            await self.bus.publish(
                UpdateUserEvent(action="disconnect", user_id=client_id)
            )

    async def stop(self):
        """Остановка сервера и отключение всех клиентов."""
        if self._stop_event:
            self._stop_event.set()
        
        if self._server_instance:
            self._server_instance.close()
            await self._server_instance.wait_closed()

        tasks = [
            data["socket"].close(code=1001, reason="Server shutdown")
            for data in self._clients.values()
        ]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        self._clients.clear()

    async def handler_client(self, websocket: websockets.ServerConnection) -> None:
        client_id = await self.register_client(websocket)
        try:
            async for message in websocket:
                await self.bus.publish(
                    IncomingRawMessage(text=str(message), user_id=client_id)
                )
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister_client(client_id)

    async def main_loop(self):
        host = "0.0.0.0"
        port = 8888
        self._stop_event = asyncio.Event()

        await self.bus.publish(
            InfoLogEvent(
                text=f"Server is activated on ws://{get_local_ip()}:{port}",
                source="websocket",
            )
        )

        async with serve(self.handler_client, host, port, ping_timeout=10) as server:
            self._server_instance = server
            await self._stop_event.wait()

    async def main(self):
        await self.main_loop()
