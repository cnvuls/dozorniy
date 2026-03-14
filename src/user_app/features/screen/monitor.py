import asyncio
import uuid

from core.events import ConnectedEvent, DisconnectedEvent, EventBus
from features.screen.logic import capture_screen, to_base64
from features.screen.request import ScreenRequest


class ScreenMonitor:
    def __init__(self, bus: EventBus, interval: int = 10):
        self.bus = bus
        self.interval = 0.5
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
                raw_frame = capture_screen(target_size=(1920, 1080))
                b64_string = to_base64(raw_frame)

                req = ScreenRequest(
                    type="screen_frame",
                    img_base64=b64_string,
                    event_id=uuid.uuid4(),
                )
                await self.bus.publish(req)
                await asyncio.sleep(self.interval)
        except asyncio.CancelledError:
            pass
