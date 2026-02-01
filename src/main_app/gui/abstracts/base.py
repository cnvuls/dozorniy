from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ServerConnection:
    data: bool


class UiAbstract(ABC):
    def __init__(self):
        #self.bus = bus
       pass

    @abstractmethod
    async def main_loop(self):
        pass
