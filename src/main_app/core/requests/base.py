import time
from typing import Literal
import uuid
from abc import ABC, abstractmethod

from pydantic import BaseModel, Field, computed_field


class RequestBase(BaseModel, ABC):
    """
    [SERVER -> CLIENT]
    Базовая команда, которую Сервер шлет Агенту.
    """

    type:str

    event_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    timestamp: float = Field(default_factory=lambda: time.time())
    user_id: int

    model_config = {"frozen": True}
