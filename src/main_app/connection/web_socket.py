import asyncio
from typing import Dict

import websockets
# from utils.get_ipadress import getIpAddress # <--- Убрали, чтобы не висло
from websockets import serve

from config.loader import load_config
from connection.abstracts import ConnectionBase
from core.events import (EventBus, IncomingRawMessage,
                                  OutputConnection, SendingCommand,
                                  UpdateUserEvent)


class WebSocketConnection(ConnectionBase):
    def __init__(self, bus: EventBus) -> None:
        self._clients: Dict[int, websockets.ServerConnection] = {}
        self.bus = bus
        self._config = load_config()

        self.bus.subscribe(SendingCommand, self.send_message)

    async def send_message(self, event: SendingCommand) -> None:
        if event.user_id in self._clients:
            await self._clients[event.user_id].send(event.text)

    async def register_client(self, socket: websockets.ServerConnection) -> int:
        user_name = str(await socket.recv())
        user_id = len(self._clients) + 1
        print(user_name)
        self._clients[user_id] = socket
        await self.bus.publish(UpdateUserEvent("connect", user_id, user_name))
        print(user_name)
        return user_id

    async def broadcast_message(self, text: str) -> None:
        if self._clients:
            await asyncio.gather(
                *[client.send(text) for _, client in self._clients.items()],
                return_exceptions=True,
            )

    async def unregister_client(self, client_id: int) -> None:
        if client_id in self._clients:
            self._clients.pop(client_id)
            await self.bus.publish(UpdateUserEvent("disconnect", client_id))

    async def stop(self):
        tasks = [
            sock.close(code=1001, reason="Server shutdown")
            for sock in self._clients.values()
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

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
        # === ИСПРАВЛЕНИЕ ЗАВИСАНИЯ ===
        # Мы убрали getIpAddress() и просто пишем 127.0.0.1
        host = "0.0.0.0"
        port = self._config.port

        await self.bus.publish(
            OutputConnection(f"Server is activated on ws://127.0.0.1:{port}")
        )

        async with serve(self.handler_client, host, port, ping_timeout=10) as server:
            self._server_instance = server
            await asyncio.Future()  # Работаем вечно

    async def main(self):
        await self.main_loop()
