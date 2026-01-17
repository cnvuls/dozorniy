import asyncio
import os
import sys
from dataclasses import dataclass

from connection.websocket import WebsocketConnection
from core.dispatcher import RequestDispatcher, ResponseDispatcher
from core.events import EventBus
from core.loader import autodiscover_features
from core.registry import FeatureRegistry
from core.responses.bus import ResponseBus


@dataclass
class ClientConfig:
    name: str = os.getenv("DOZOR_AGENT_NAME", "agent")
    host: str = os.getenv("DOZOR_SERVER_HOST", "127.0.0.1")
    port: int = int(os.getenv("DOZOR_SERVER_PORT", "8888"))
    status_interval: int = int(os.getenv("DOZOR_STATUS_INTERVAL", "15"))
    reconnect_delay: float = float(os.getenv("DOZOR_RECONNECT_DELAY", "3.0"))


class ClientApp:
    def __init__(self, config: ClientConfig) -> None:
        self.config = config
        self.bus = EventBus()

        self.connection = WebsocketConnection(
            bus=self.bus,
            port=config.port,
            ip=config.host,
            name=config.name,
            reconnect_delay=config.reconnect_delay,
        )

        self._init_layers()

    def _init_layers(self):
        self.req_dispatcher = RequestDispatcher(self.bus)
        self.resp_bus = ResponseBus()
        self.resp_dispatcher = ResponseDispatcher(self.resp_bus, self.bus)

        print("[ClientApp] 🔎 Scanning features...")
        autodiscover_features(base_package="features")

        features = FeatureRegistry.get_features()

        if not features:
            print("[ClientApp] ⚠️ No features found!")

        for meta in features:
            try:
                handler_instance = meta.handler_cls(bus=self.bus)
                self.resp_dispatcher.bind(meta.command_key, meta.response_model)
                self.resp_bus.register(meta.response_model, handler_instance)
                print(
                    f"   ✅ Registered: '{meta.command_key}' -> {meta.handler_cls.__name__}"
                )
            except Exception as e:
                print(f"   ❌ Failed to register '{meta.command_key}': {e}")

        print(
            f"[ClientApp] Init complete. Total handlers: {len(self.resp_bus._handlers)}"
        )

    async def run(self) -> None:
        print(
            f"[ClientApp] 🚀 Starting agent '{self.config.name}' on {self.config.host}:{self.config.port}"
        )
        await self.connection.main_loop()


async def main() -> None:
    config = ClientConfig()
    app = ClientApp(config)
    await app.run()


if __name__ == "__main__":
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Client] Stopped.")
