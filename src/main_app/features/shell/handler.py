from main_app.core.events import EventBus, OutputConnection
from main_app.core.registry import FeatureRegistry
from main_app.core.responses.base import ResponseHandler
from main_app.features.shell.response import ShellResponse


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
