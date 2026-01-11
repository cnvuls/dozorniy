import json
from typing import Dict, List, Optional, Type

from pydantic import ValidationError

from main_app.core.events import (EventBus, IncomingRawMessage,
                                  OutgoingRawMessage, SendingCommand,
                                  SendServerCommand)
from main_app.core.requests.base import RequestBase
from main_app.core.responses.base import \
    ResponseBase  # INFO: Бывший RequestBase
from main_app.core.responses.middleware import ResponseMiddleware
from main_app.core.responses.responsebus import \
    ResponseBus  # INFO: Бывший RequestBus


class ResponseDispatcher:
    def __init__(self, respbus: ResponseBus, bus: EventBus) -> None:
        self._respbus: ResponseBus = respbus
        self._middlewares: List[ResponseMiddleware] = []
        self._type_map: Dict[str, Type[ResponseBase]] = {}
        self._bus: EventBus = bus

        # INFO: Подписка на сырые входящие
        self._bus.subscribe(IncomingRawMessage, self.dispatch)

    def bind(self, msg_type: str, resp_cls: Type[ResponseBase]) -> None:
        self._type_map[msg_type] = resp_cls

    def _parse_payload(self, text: str) -> Optional[dict]:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None

    async def dispatch(self, raw: IncomingRawMessage):
        try:
            data = json.loads(raw.text)
        except json.JSONDecodeError:
            return

        msg_type = data.get("type", "")
        model_cls = self._type_map.get(msg_type)
        data["user_id"] = raw.user_id

        if not model_cls:
            return

        async def tail_call(d: dict):
            return await self._process_after_middleware(model_cls, d)

        chain = tail_call
        for mw in reversed(self._middlewares):

            def make_step(current_mw, next_step):
                async def step(d: dict):
                    print(d)
                    return await current_mw(d, next_step)

                return step

            chain = make_step(mw, chain)

        await chain(data)

    async def _process_after_middleware(self, resp_cls: Type[ResponseBase], data: dict):
        try:
            response_instance = resp_cls.model_validate(data)

            await self._respbus.execute(response_instance)
        except ValidationError as e:
            print(e)
            # TODO: Обработка ошибок валидации
            pass


class RequestDispatcher:
    def __init__(self, bus: EventBus) -> None:
        self._event_bus: EventBus = bus
        self._event_bus.subscribe(RequestBase, self.send)

    async def send(self, request: RequestBase) -> None:
        data = request.model_dump()

        await self._event_bus.publish(
            SendingCommand(
                user_id=request.user_id,
                text=request.model_validate(data).model_dump_json(),
            )
        )
