from typing import Awaitable, Callable, Protocol

from main_app.core.responses.base import ResponseBase  # INFO: Смена импорта

# INFO: Теперь Callable работает с Response
NextMiddleware = Callable[[ResponseBase], Awaitable[None]]


class ResponseMiddleware(Protocol):
    """Протокол для мидлварей обработки ответов"""

    async def __call__(self, response: ResponseBase, next_: NextMiddleware) -> None:
        pass
