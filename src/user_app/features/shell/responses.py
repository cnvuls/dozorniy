from core.responses.base import ResponseBase


class ShellResponse(ResponseBase):
    command: str
