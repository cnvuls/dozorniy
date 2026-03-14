# Copyright (c) 2026 hackhype. SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

from core.events import ConsoleLogEvent, EventBus
from core.registry import FeatureRegistry
from core.responses.base import ResponseHandler
from features.shell.request import ShellRequest
from features.shell.response import ShellResponse


@FeatureRegistry.register(
    command_key="shell_result",
    response_model=ShellResponse,
    request_model=ShellRequest,
    name="Терминал",
    version="1.1.0",
    args_model=ShellRequest,
)
class ShellHandler(ResponseHandler):
    def __init__(self, bus: EventBus):
        self.bus: EventBus = bus

    async def handle(self, response: ShellResponse) -> None:
        if response.exit_code == 0:
            message = response.stdout
        else:
            message = f"error: {response.stderr}, code: {response.exit_code}"

        await self.bus.publish(ConsoleLogEvent(text=message, source="handler"))
