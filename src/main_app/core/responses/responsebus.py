from typing import Dict, List, Type

from core.middleware.base import MiddlewareNext, ResponseMiddleware
from core.responses.base import ResponseBase, ResponseHandler


class ResponseBus:
    def __init__(self) -> None:
        self._handlers: Dict[Type[ResponseBase], ResponseHandler] = {}
        self._middlewares: List[ResponseMiddleware] = []

    def register(self, response_class: Type[ResponseBase], handler: ResponseHandler):
        self._handlers[response_class] = handler

    def add_middleware(self, middleware: ResponseMiddleware):
        self._middlewares.append(middleware)

    async def execute(self, response: ResponseBase) -> None:
        response_type = type(response)
        handler = self._handlers.get(response_type)

        if not handler:
            # TODO: Интегрировать с логгером вместо print
            print(
                f"[ResponseBus] CRITICAL: No handler registered for {response_type.__name__}"
            )
            return

        async def core_handler(res: ResponseBase) -> None:
            await handler.handle(res)

        wrapped_action = core_handler

        for middleware in reversed(self._middlewares):

            def create_wrapper(m: ResponseMiddleware, n: MiddlewareNext):
                async def wrapper(res: ResponseBase) -> None:
                    await m(res, n)

                return wrapper

            wrapped_action = create_wrapper(middleware, wrapped_action)

        await wrapped_action(response)
