from core.responses.base import ResponseBase


class MessageResponse(ResponseBase):
    text: str
    title: str
