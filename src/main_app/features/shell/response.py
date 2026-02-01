from core.responses.base import ResponseBase


class ShellResponse(ResponseBase):

    stdout: str = ""
    stderr: str = ""
    exit_code: int
