from core.requests.base import RequestBase


class ShellRequest(RequestBase):
    type: str = "shell_result"
    stdout: str
    stderr: str
    exit_code: int
