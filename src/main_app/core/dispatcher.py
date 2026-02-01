import json
from typing import Any, Awaitable, Callable, Dict, List, Optional, Type, cast

from pydantic import ValidationError

from core.events import EventBus, IncomingRawMessage, SendingCommand
from core.middleware.base import MiddlewareNext, ResponseMiddleware
from core.requests.base import RequestBase
from core.responses.base import ResponseBase
from core.responses.responsebus import ResponseBus


class ResponseDispatcher:
    def __init__(self, respbus: ResponseBus, bus: EventBus) -> None:
        self._respbus: ResponseBus = respbus
        self._middlewares: list[ResponseMiddleware] = []
        self._type_map: dict[str, Type[ResponseBase]] = {}
        self._bus: EventBus = bus

        self._bus.subscribe(IncomingRawMessage, self.dispatch)

    def bind(self, msg_type: str, resp_cls: Type[ResponseBase]) -> None:
        self._type_map[msg_type] = resp_cls

    def _parse_payload(self, text: str) -> Optional[Dict[str, Any]]:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None

    async def dispatch(self, raw: IncomingRawMessage) -> None:
        try:
            # Явно указываем тип переменной data
            data: Dict[str, Any] = json.loads(raw.text)
        except json.JSONDecodeError:
            return

        msg_type = str(data.get("type", ""))
        model_cls = self._type_map.get(msg_type)
        data["user_id"] = raw.user_id

        if not model_cls:
            return

        async def tail_call(d: Dict[str, Any]) -> None:
            await self._process_after_middleware(model_cls, d)

        chain: MiddlewareNext = tail_call
        for mw in reversed(self._middlewares):

            def make_step(
                current_mw: ResponseMiddleware, next_step: MiddlewareNext
            ) -> MiddlewareNext:

                async def step(d: dict[str, Any]) -> None:
                    await current_mw(cast(Any, d), next_step)

                return step

            chain = make_step(mw, chain)

        await chain(data)

    async def _process_after_middleware(
        self, resp_cls: Type[ResponseBase], data: Dict[str, Any]
    ) -> None:
        try:
            response_instance = resp_cls.model_validate(data)
            await self._respbus.execute(response_instance)
        except ValidationError as e:
            print(f"[Dispatcher] Validation Error: {e}")


class RequestDispatcher:
    def __init__(self, bus: EventBus) -> None:
        self._event_bus: EventBus = bus
        self._event_bus.subscribe(RequestBase, self.send)
        self._middlewares: list[ResponseMiddleware] = []

    def add_middleware(self, middleware: Any):
        self._middlewares.append(middleware)

    async def send(self, request: RequestBase) -> None:
        data: Dict[str, Any] = request.model_dump(mode="json")

        async def tail_call(d: Dict[str, Any]) -> None:
            await self._process_after_middleware(request, d)

        chain: MiddlewareNext = tail_call

        for mw in reversed(self._middlewares):

            def make_step(current_mw: Any, next_step: MiddlewareNext) -> MiddlewareNext:

                async def step(d: Dict[str, Any]) -> None:
                    await current_mw(cast(Any, d), next_step)

                return step

            chain = make_step(mw, chain)

        await chain(data)

    async def _process_after_middleware(
        self, request: RequestBase, data: Dict[str, Any]
    ) -> None:
        import json

        json_str = json.dumps(data)

        await self._event_bus.publish(
            SendingCommand(
                user_id=request.user_id,
                text=json_str,
            )
        )
