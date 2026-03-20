from core.requests.base import RequestBase


class MessageRequest(RequestBase):
    type: str = "message"
    title: str = "Dozorniy"
    text: str
