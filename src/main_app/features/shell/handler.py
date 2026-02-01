# Copyright (c) 2026 hackhype. SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

from core.events import EventBus, OutputConnection
from core.registry import FeatureRegistry
from core.responses.base import ResponseHandler
from features.shell.response import ShellResponse


@FeatureRegistry.register(command_key="shell_result", response_model=ShellResponse)
class ShellHandler(ResponseHandler):

    def __init__(self, bus: EventBus):
        self.bus: EventBus = bus

    async def handle(self, response: ShellResponse) -> None:
        if response.exit_code == 0:
            message = response.stdout
        else:
            message = f"error: {response.stderr}, code: {response.exit_code}"

        await self.bus.publish(OutputConnection(text=message))
