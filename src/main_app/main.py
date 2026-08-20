import asyncio
import os
from dataclasses import dataclass

from connection.web_socket import WebSocketConnection
from core.dispatcher import RequestDispatcher, ResponseDispatcher
from core.events import ConsoleLogEvent, EventBus
from core.loader import autodiscover_features
from core.registry import FeatureRegistry
from core.services.feature_service import FeatureService
from ui.abstracts.base import ServerConnection
from ui.gui_factory import GuiFactory


@dataclass
class ServerConfig:
    host: str = "0.0.0.0"
    port: int = 8888


FEATURES_PATH = os.path.join(os.path.dirname(__file__), "features")
FEATURES_PACKAGE = "features"


class ServerApp:
    def __init__(self, config: ServerConfig):
        self.config = config

        self.bus = EventBus()
        self.dispatcher = ResponseDispatcher(self.bus)
        self.request_dispatcher = RequestDispatcher(self.bus)
        self.gui = GuiFactory.create_object(bus=self.bus)
        self.server = WebSocketConnection(self.bus)
        self._server_task: asyncio.Task | None = None
        self._load_and_setup_features()
        self.feature_service = FeatureService(self.bus)
        self._setup_server_subscriptions()

    def _load_and_setup_features(self):
        autodiscover_features()
        features_meta = FeatureRegistry.get_features()

        if not features_meta:
            print("⚠️ Warning: No features found in Registry!")

        for meta in features_meta:
            if meta.response_model:
                self.dispatcher.bind(meta.command_key, meta.response_model)
                handler_instance = meta.handler_cls(self.bus)
                self.bus.subscribe(meta.response_model, handler_instance.handle)

    async def _handle_server_toggle(self, event: ServerConnection):
        if event.data:
            if self._server_task is None or self._server_task.done():
                await self.bus.publish(
                    ConsoleLogEvent(
                        text="🚀 [SYSTEM]: Запуск сервера...", source="main"
                    )
                )
                self._server_task = asyncio.create_task(self.server.main())
        else:
            if self._server_task and not self._server_task.done():
                await self.bus.publish(
                    ConsoleLogEvent(
                        text="🛑 [SYSTEM]: Остановка сервера...", source="main"
                    )
                )
                await self.server.stop()

                try:
                    await self._server_task
                except asyncio.CancelledError:
                    pass
                finally:
                    self._server_task = None
                    await self.bus.publish(
                        ConsoleLogEvent(
                            text="✅ [SYSTEM]: Сервер успешно остановлен", source="main"
                        )
                    )

    def _setup_server_subscriptions(self):
        self.bus.subscribe(ServerConnection, self._handle_server_toggle)

    async def run(self):
        print("--- 🛡️ ПОДГОТОВКА ЗАПУСКА DOZORNIY ---")
        try:
            await self.gui.main_loop()
        except Exception as e:
            print(f"❌ Ошибка при работе приложения: {e}")
        finally:
            if self._server_task and not self._server_task.done():
                await self.server.stop()


async def main():
    config = ServerConfig()
    app = ServerApp(config)
    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n--- Процесс завершен ---")
