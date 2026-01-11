from abc import ABC, abstractmethod
from typing import Any

from config.settings import Config
from core.events import EventBus


class AbstractFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_object(bus: EventBus, config: Config, **kwargs) -> Any:
        pass
