from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel


class ResponseBase(BaseModel):
    timestamp: float
    event_id: UUID


T = TypeVar("T", bound="ResponseBase")


class ResponseHandler(ABC, Generic[T]):
    """
    Базовый класс. Больше не занимается валидацией.
    Принимает уже готовый объект команды.
    """

    @abstractmethod
    async def handle(self, command: T):
        pass
