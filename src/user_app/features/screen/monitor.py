import asyncio
import uuid
from core.events import EventBus, ConnectedEvent, DisconnectedEvent
from features.screen.request import ScreenRequest

class ScreenMonitor:
    def __init__(self, bus: EventBus, interval: int = 10):
        self.bus = bus
        self.interval = interval
        self._task = None
        
        # Подписываемся на события сокета
        self.bus.subscribe(ConnectedEvent, self.start)
        self.bus.subscribe(DisconnectedEvent, self.stop)

    async def start(self, event=None):
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._loop())

    async def stop(self, event=None):
        if self._task and not self._task.done():
            self._task.cancel()
            self._task = None

    async def _loop(self):
        try:
            while True:
                req = ScreenRequest(
                    type="screen",
                    image="placeholder",
                    event_id=uuid.uuid4()
                )
                await self.bus.publish(req)
                await asyncio.sleep(self.interval)
        except asyncio.CancelledError:
            pass
