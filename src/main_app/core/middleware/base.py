from collections.abc import Awaitable, Callable
from typing import Any, Protocol

from main_app.core.responses.base import ResponseBase

MiddlewareNext = Callable[[dict[str, Any]], Awaitable[None]]


class ResponseMiddleware(Protocol):
    async def __call__(self, response: ResponseBase, next_: MiddlewareNext) -> None:
        pass


class RequestMiddleware(Protocol):
    async def __call__(self, response: ResponseBase, next_: MiddlewareNext) -> None:
        pass
