from abc import ABC, abstractmethod
from typing import Any

from core.events import EventBus


class AbstractFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_object(bus: EventBus) -> Any:
        pass
