from core.events import EventBus
from core.events.other import TelemetryUpdateEvent
from core.registry import FeatureRegistry
from core.responses.base import ResponseHandler
from features.telemetry.response import TelemetryResponse


@FeatureRegistry.register(
    name="telemetry",
    command_key="telemetry",
    response_model=TelemetryResponse,
    version="1.0.0",
    is_hidden=True,
)
class TelemetryHandler(ResponseHandler):
    def __init__(self, bus: EventBus) -> None:
        self.bus = bus

    async def handle(self, response: TelemetryResponse) -> None:
        await self.bus.publish(
            TelemetryUpdateEvent(user_id=response.user_id, text=response.text)
        )
