import asyncio
import uuid

from core.events import ConnectedEvent, DisconnectedEvent, EventBus
from features.screen.request import ScreenRequest


class ScreenMonitor:
    def __init__(self, bus: EventBus, interval: int = 10):
        self.bus = bus
        self.interval = interval
        self._task = None

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
                    type="screen_frame",
                    img_base64=b"""
                    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
                    """,
                    event_id=uuid.uuid4(),
                )
                await self.bus.publish(req)
                await asyncio.sleep(self.interval)
        except asyncio.CancelledError:
            pass
