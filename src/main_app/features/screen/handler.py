from core.events import EventBus
from core.events.network import FrameData
from core.registry import FeatureRegistry
from core.responses.base import ResponseHandler
from features.screen.request import ScreenRequest
from features.screen.response import ScreenResponse


@FeatureRegistry.register(
    command_key="screen_frame",
    response_model=ScreenResponse,
    request_model=ScreenRequest,
    name="Демонстрация экрана",
    version="1.0.0",
    is_hidden=True,
)
class ShellHandler(ResponseHandler):
    def __init__(self, bus: EventBus):
        self.bus: EventBus = bus

    async def handle(self, response: ScreenResponse) -> None:
        await self.bus.publish(
            FrameData(base64_img=response.img_base64, user_id=response.user_id)
        )
