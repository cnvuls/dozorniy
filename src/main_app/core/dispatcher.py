import json
from typing import Any, Optional

from pydantic import ValidationError

from core.events import EventBus, IncomingRawMessage, SendingCommand
from core.requests.base import RequestBase
from core.responses.base import ResponseBase


class ResponseDispatcher:
    def __init__(self, bus: EventBus) -> None:
        self._type_map: dict[str, type[ResponseBase]] = {}
        self._bus: EventBus = bus

        self._bus.subscribe(IncomingRawMessage, self.dispatch)

    def bind(self, msg_type: str, resp_cls: type[ResponseBase]) -> None:
        self._type_map[msg_type] = resp_cls

    def _parse_payload(self, text: str) -> Optional[dict[str, Any]]:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None

    async def dispatch(self, raw: IncomingRawMessage) -> None:
        try:
            data: dict[str, Any] = json.loads(raw.text)
        except json.JSONDecodeError:
            return

        msg_type = str(data.get("type", ""))
        model_cls = self._type_map.get(msg_type)
        data["user_id"] = raw.user_id

        if not model_cls:
            return

        try:
            response_instance = model_cls.model_validate(data)
            await self._bus.publish(response_instance)
        except ValidationError as e:
            print(f"[Dispatcher] Validation Error: {e}")


class RequestDispatcher:
    def __init__(self, bus: EventBus) -> None:
        self._event_bus: EventBus = bus
        self._event_bus.subscribe(RequestBase, self.send)

    async def send(self, request: RequestBase) -> None:
        data: dict[str, Any] = request.model_dump(mode="json")

        json_str = json.dumps(data)

        await self._event_bus.publish(
            SendingCommand(
                user_id=request.user_id,
                text=json_str,
            )
        )
