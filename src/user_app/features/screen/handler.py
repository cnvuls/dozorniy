import asyncio
import uuid

from core.events import ConnectedEvent, DisconnectedEvent, EventBus
from core.registry import FeatureRegistry
from core.responses.base import ResponseHandler
from features.screen.logic import capture_screen, to_base64
from features.screen.request import ScreenRequest
from features.screen.response import FrameTimeOption, ScreenResponse


@FeatureRegistry.register(command_key="screen_rate", response_model=ScreenResponse)
class ScreenMonitor(ResponseHandler):
    def __init__(self, bus: EventBus):
        self.bus = bus
        self.interval: FrameTimeOption = FrameTimeOption.SLOW
        self._task = None
        self._interrupt_event = asyncio.Event()

        self.bus.subscribe(ConnectedEvent, self.start)
        self.bus.subscribe(DisconnectedEvent, self.stop)
        self.full = False

    async def handle(self, command: ScreenResponse):
        print(command)
        self.interval = command.frame_time
        self.full = command.window_fullscreen
        self._interrupt_event.set()

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
                if self.full:
                    raw_frame = capture_screen(target_size=None)
                else:
                    raw_frame = capture_screen(target_size=(160, 80))
                b64_string = to_base64(raw_frame)

                req = ScreenRequest(
                    type="screen_frame",
                    img_base64=b64_string,
                    event_id=uuid.uuid4(),
                )
                await self.bus.publish(req)

                try:
                    self._interrupt_event.clear()
                    await asyncio.wait_for(
                        self._interrupt_event.wait(), timeout=self.interval.value
                    )
                except asyncio.TimeoutError:
                    pass
        except asyncio.CancelledError:
            pass
