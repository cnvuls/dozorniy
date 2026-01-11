# Copyright (c) 2026 hackhype. SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

from typing import Dict, Type

from core.responses.base import ResponseBase, ResponseHandler


class ResponseBus:
    def __init__(self) -> None:
        self._handlers: Dict[Type[ResponseBase], ResponseHandler] = {}

    def register(self, model_cls: Type[ResponseBase], handler: ResponseHandler):
        """Обучаем шину: какой класс кто обрабатывает"""
        self._handlers[model_cls] = handler

    async def execute(self, command: ResponseBase) -> None:

        cmd_type = type(command)
        handler = self._handlers.get(cmd_type)

        if not handler:
            print(f"[Bus] CRITICAL: Нет хендлера для {cmd_type.__name__}")
            return

        await handler.handle(command)
