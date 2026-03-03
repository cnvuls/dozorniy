from core.events import EventBus
from core.events.other import RequestFeatureList, ResponseFeatureList
from core.registry import FeatureRegistry

class FeatureService:
    def __init__(self, bus: EventBus):
        self.bus = bus
        self.bus.subscribe(RequestFeatureList, self._handle_get_features)

    async def _handle_get_features(self, event: RequestFeatureList):
        all_features = FeatureRegistry.get_features()
        public_features = [f for f in all_features if not f.is_hidden]
        await self.bus.publish(ResponseFeatureList(content=public_features))
