from core.events import EventBus
from core.registry import FeatureRegistry
from core.responses.base import ResponseHandler
from features.message.request import MessageRequest

@FeatureRegistry.register(
    name="Отправить сообщения",
    version="1.0.0",
    command_key="message",
    request_model=MessageRequest,
    args_model=MessageRequest,
)
class MessageHandler(ResponseHandler):
    def __init__(self, bus: EventBus):
        self.bus: EventBus = bus

    async def handle(self, response: MessageRequest) -> None:
        await self.bus.publish(response)
