# main_app/core/responses/base.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

T_Response = TypeVar("T_Response", bound="ResponseBase")


class ResponseBase(BaseModel):
    """
    [CLIENT -> SERVER]
    """

    message_id: UUID = Field(default_factory=uuid4)
    user_id: int
    # INFO: ID запроса от клиента, на который мы отвечаем
    event_id: UUID

    # INFO: защита от дибила
    model_config = {"frozen": True}


class ResponseHandler(ABC, Generic[T_Response]):
    """
    INFO: Обычно логика формирования ответа лежит в RequestHandler,
    но если нужна отдельная логика обработки исходящих ответов:
    """

    @abstractmethod
    async def handle(self, response: T_Response) -> None:
        pass
