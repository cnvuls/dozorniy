import time
import uuid
from abc import ABC, abstractmethod

from pydantic import BaseModel, Field, computed_field


class RequestBase(BaseModel, ABC):
    """
    [SERVER -> CLIENT]
    Базовая команда, которую Сервер шлет Агенту.
    """

    # 1. Тип команды (computed_field попадет в JSON при сериализации)
    @computed_field
    @property
    @abstractmethod
    def type(self) -> str:
        return "default"

    # 2. Метаданные (обязательно отправляем)
    event_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    timestamp: float = Field(default_factory=lambda: time.time())
    user_id: int

    model_config = {"frozen": True}
