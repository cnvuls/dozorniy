from abc import ABC, abstractmethod

from core.events import EventBus, ReceivingMessage


class UiAbstract(ABC):
    def __init__(self, bus: EventBus):
        self.bus = bus

    @abstractmethod
    async def recieve_message(self, event: ReceivingMessage):
        pass

    @abstractmethod
    async def send_message(self, *args, **kwargs):
        pass

    @abstractmethod
    async def main_loop(self):
        pass
