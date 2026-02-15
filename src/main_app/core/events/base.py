import asyncio
from typing import Dict, Type, Callable, List, Any
from abc import ABC
from dataclasses import asdict, dataclass

@dataclass(kw_only=True)
class AbstractEvent(ABC):
    def as_dict(self):
        data = {"name": self.__class__.__name__}
        data.update(asdict(self))
        return data


class EventBus:
    def __init__(self):

        self._subscribers: Dict[Type, List[Callable]] = {}

        self._cache: Dict[Type, List[Callable]] = {}

    def subscribe(self, event_type: Type[AbstractEvent], callback: Callable) -> None:
        """Подписаться на событие (или базовый класс событий)."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

        self._cache.clear()
    
    def unsubscribe(self, event_Type: Type[AbstractEvent], callback: Callable) -> None:
        """Отписка от события (также базовых классов)"""
        if event_Type in self._subscribers:
            try:
                self._subscribers[event_Type].remove(callback)
                self._cache.clear()
            except ValueError:
                pass

    async def publish(self, event: Any) -> None:
        """Опубликовать событие. Работает с учетом наследования."""
        event_type = type(event)

        handlers = self._cache.get(event_type)

        if handlers is None:
            handlers = []

            for cls in event_type.__mro__:
                if cls in self._subscribers:
                    handlers.extend(self._subscribers[cls])

            self._cache[event_type] = handlers

        if not handlers:
            return

        for handler in handlers:
            asyncio.create_task(handler(event))


