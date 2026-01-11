from abc import ABC, abstractmethod

from core.events import EventBus, SendMessage


class ConnectionBase(ABC):
    def __init__(self, bus: EventBus, port: int, ip: str, name: str) -> None:
        self.bus: EventBus = bus
        self.port: int = port
        self.ip: str = ip
        self.name: str = name

    @abstractmethod
    async def receive_message(self, data: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def send_message(self, event: SendMessage) -> None:
        raise NotImplementedError

    @abstractmethod
    async def main_loop(self) -> None:
        raise NotImplementedError
