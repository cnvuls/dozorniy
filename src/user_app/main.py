import asyncio
import os
import sys

from connection.websocket import WebsocketConnection
from core.dispatcher import RequestDispatcher, ResponseDispatcher
from core.events import EventBus
from core.loader import autodiscover_features
from core.registry import FeatureRegistry
from core.responses.bus import ResponseBus
from core.config import config

from features.telemetry.monitor import TelemetryMonitor
from features.screen.monitor import ScreenMonitor

class ClientApp:
    def __init__(self) -> None:
        self.bus = EventBus()
        self.connection = WebsocketConnection(
            bus=self.bus,
            port=config.SERVER_PORT,
            ip=config.SERVER_HOST,
            name=config.AGENT_NAME,
            reconnect_delay=config.RECONNECT_DELAY,
        )

    def _init_layers(self):
        self.req_dispatcher = RequestDispatcher(self.bus)
        self.resp_bus = ResponseBus()
        self.resp_dispatcher = ResponseDispatcher(self.resp_bus, self.bus)

        autodiscover_features(base_package="features")
        features = FeatureRegistry.get_features()

        for meta in features:
            try:
                handler_instance = meta.handler_cls(bus=self.bus)
                self.resp_dispatcher.bind(meta.command_key, meta.response_model)
                self.resp_bus.register(meta.response_model, handler_instance)
            except Exception as e:
                print(f"Error registering {meta.command_key}: {e}")

        self.telemetry = TelemetryMonitor(self.bus, interval=config.TELEMETRY_INTERVAL)
        self.screen = ScreenMonitor(self.bus, interval=config.SCREEN_INTERVAL)

    async def run(self) -> None:
        self._init_layers()
        await self.connection.main_loop()

async def main() -> None:
    app = ClientApp()
    await app.run()

if __name__ == "__main__":
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
