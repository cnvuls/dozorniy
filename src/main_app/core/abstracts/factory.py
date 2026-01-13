from abc import ABC, abstractmethod
from typing import Any

from main_app.core.events import EventBus


class AbstractFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_object(bus: EventBus) -> Any:
        pass
