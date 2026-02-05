from typing import Literal
from core.requests.base import RequestBase


class ShellRequest(RequestBase):
    """
    Класс от сервера к клиенту очень простой и базовый
    """
    type: Literal["shell"] = "shell"
   
    command: str
