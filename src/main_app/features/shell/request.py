from core.requests.base import RequestBase


class ShellRequest(RequestBase):
    """
    Класс от сервера к клиенту очень простой и базовый
    """

    type: str = "shell"

    command: str
