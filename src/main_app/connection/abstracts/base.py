from abc import ABC, abstractmethod
from typing import Any, Dict

from core.events import SendingCommand, UpdateUserEvent


class ClientConnection(ABC):
    """Абстракция клиентского соединения (WebSocket, TCP, etc.)"""

    @abstractmethod
    async def send(self, text: str) -> None:
        pass

    @abstractmethod
    async def receive(self) -> str:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass


class ConnectionBase(ABC):
    def __init__(self) -> None:
        self._clients: Dict[int, Any] = {}

    @abstractmethod
    async def register_client(self, socket) -> int:
        pass

    @abstractmethod
    async def unregister_client(self, client_id: int) -> None:
        pass

    @abstractmethod
    async def send_message(self, event: SendingCommand) -> None:
        pass

    @abstractmethod
    async def stop(self):
        pass

    @abstractmethod
    async def handler_client(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    async def broadcast_message(self, text: str) -> None:
        pass

    @abstractmethod
    async def main(self):
        pass
