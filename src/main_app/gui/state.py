from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, Tuple

from core.events import OutputConnection, ReceivingMessage, UpdateUserEvent


@dataclass(frozen=True)
class GuiSnapshot:
    users: Dict[int, str]
    last_messages: Tuple[str, ...]
    last_logs: Tuple[str, ...]


class GuiStateStore:
    """Collects lightweight state for future GUI implementations."""

    def __init__(self, max_items: int = 50) -> None:
        self._users: Dict[int, str] = {}
        self._messages: Deque[str] = deque(maxlen=max_items)
        self._logs: Deque[str] = deque(maxlen=max_items)

    def attach(self, bus) -> None:
        bus.subscribe(ReceivingMessage, self._on_message)
        bus.subscribe(OutputConnection, self._on_log)
        bus.subscribe(UpdateUserEvent, self._on_user_event)

    async def _on_message(self, event: ReceivingMessage) -> None:
        self._messages.append(f"{event.user_id}: {event.text}")

    async def _on_log(self, event: OutputConnection) -> None:
        self._logs.append(event.text)

    async def _on_user_event(self, event: UpdateUserEvent) -> None:
        if event.action == "connect":
            self._users[event.user_id] = event.user_name or f"user-{event.user_id}"
        else:
            self._users.pop(event.user_id, None)

    def snapshot(self) -> GuiSnapshot:
        return GuiSnapshot(
            users=dict(self._users),
            last_messages=tuple(self._messages),
            last_logs=tuple(self._logs),
        )
