from typing import Any, Dict, Literal, Optional

from pydantic import Base64Bytes

from .base import AbstractEvent


class IncomingRawMessage(AbstractEvent):
    user_id: int
    text: str


class OutgoingRawMessage(AbstractEvent):
    user_id: int
    data: Dict[str, Any]


class SendingCommand(AbstractEvent):
    text: str
    user_id: int


class FrameData(AbstractEvent):
    base64_img: bytes
    user_id: int


class UpdateUserEvent(AbstractEvent):
    action: Literal["connect", "disconnect"]
    user_id: int
    user_name: str = "Не указан"


class SendServerCommand(AbstractEvent):
    user_id: int
    command: str
    payload: Dict[str, Any]
    request_id: str
