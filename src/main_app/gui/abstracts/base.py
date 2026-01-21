from abc import ABC, abstractmethod


class UiAbstract(ABC):
    def __init__(self):
        #self.bus = bus
       pass

    @abstractmethod
    async def main_loop(self):
        pass
