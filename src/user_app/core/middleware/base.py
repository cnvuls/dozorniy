from typing import Awaitable, Callable, Protocol

from core.responses.base import ResponseBase

NextMiddleware = Callable[[ResponseBase], Awaitable[None]]


class ResponseMiddleware(Protocol):
    async def __call__(self, response: ResponseBase, next_: NextMiddleware) -> None:
        pass


class RequestMiddleware(Protocol):
    async def __call__(self, response: ResponseBase, next_: NextMiddleware) -> None:
        pass
