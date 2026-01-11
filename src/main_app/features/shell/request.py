from main_app.core.requests.base import RequestBase


class ShellRequest(RequestBase):
    """
    Класс от сервера к клиенту очень простой и базовый
    """

    @property
    def type(self) -> str:
        return "shell"

    command: str
