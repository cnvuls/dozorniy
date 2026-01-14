# Copyright (c) 2026 hackhype. SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

import json
from typing import Callable, Dict, List, Optional, Type

from core.events import EventBus, ReceiveMessage, SendMessage
from core.middleware.base import RequestMiddleware, ResponseMiddleware
from core.requests.base import RequestBase
from core.responses.base import ResponseBase
from core.responses.bus import ResponseBus
from pydantic import ValidationError


class ResponseDispatcher:
    def __init__(self, respbus: ResponseBus, bus: EventBus) -> None:
        self._respbus = respbus
        self._bus = bus
        self._type_map: Dict[str, Type[ResponseBase]] = {}
        self._middlewares: List[ResponseMiddleware] = []
        self._bus.subscribe(ReceiveMessage, self.dispatch)

    def bind(self, msg_type: str, model_cls: Type[ResponseBase]):
        self._type_map[msg_type] = model_cls

    async def dispatch(self, raw: ReceiveMessage):
        try:
            data = json.loads(raw.text)
        except json.JSONDecodeError:
            return

        msg_type = data.get("type", "")
        model_cls = self._type_map.get(msg_type)

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

    async def _process_after_middleware(
        self, model_cls: Type[ResponseBase], data: dict
    ):
        try:
            command_obj = model_cls.model_validate(data)
            await self._respbus.execute(command_obj)
        except ValidationError as e:
            print(e)


class RequestDispatcher:
    def __init__(self, bus: EventBus) -> None:
        self._event_bus: EventBus = bus
        self._middlewares: List[RequestMiddleware] = []
        self._event_bus.subscribe(RequestBase, self.send)

    def add_middleware(self, middleware: RequestMiddleware):
        self._middlewares.append(middleware)

    async def send(self, request: RequestBase) -> None:
        data = request.model_dump(mode="json")

        async def send_to_bus(current_data: dict) -> None:
            await self._event_bus.publish(SendMessage(text=json.dumps(current_data)))

        wrapped_action = send_to_bus

        for middleware in reversed(self._middlewares):

            def create_step(m, n):
                async def step(d: dict) -> None:
                    print(d)
                    await m(d, n)

                return step

            wrapped_action = create_step(middleware, wrapped_action)

        await wrapped_action(data)
