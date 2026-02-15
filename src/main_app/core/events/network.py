from dataclasses import dataclass
from .base import AbstractEvent
from typing import Dict, Any, Literal, Optional

@dataclass
class IncomingRawMessage(AbstractEvent):
    user_id: int
    text: str


@dataclass
class OutgoingRawMessage(AbstractEvent):
    user_id: int
    data: Dict[str, Any]

@dataclass
class SendingCommand(AbstractEvent):
    text: str
    user_id: int


@dataclass
class UpdateUserEvent(AbstractEvent):
    action: Literal["connect", "disconnect"]
    user_id: int
    user_name: Optional[str] = None


@dataclass
class SendServerCommand(AbstractEvent):
    user_id: int
    command: str
    payload: Dict[str, Any]
    request_id: str


