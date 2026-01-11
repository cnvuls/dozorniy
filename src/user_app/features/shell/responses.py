from core.responses.base import ResponseBase


class ShellCommand(ResponseBase):
    command: str
