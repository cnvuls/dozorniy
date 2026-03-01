import asyncio
import os
import sys
from dataclasses import dataclass

from connection.web_socket import WebSocketConnection
from core.dispatcher import ResponseDispatcher
from core.events import (
    ConsoleLogEvent,
    EventBus,
    InfoLogEvent,
    SendingCommand,
    UpdateUserEvent,
)
from core.loader import autodiscover_features
from core.registry import FeatureRegistry
from core.responses.responsebus import ResponseBus
from features.shell.request import ShellRequest
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
        self.resp_bus = ResponseBus()
        self.dispatcher = ResponseDispatcher(self.resp_bus, self.bus)
        self.gui = GuiFactory.create_object(bus=self.bus)
        self.server = WebSocketConnection(self.bus)
        self._server_task: asyncio.Task | None = None
        self._load_and_setup_features()

        self._setup_server_subscriptions()

    
    def _load_and_setup_features(self):
        autodiscover_features()
        features_meta = FeatureRegistry.get_features()

        if not features_meta:
            print("⚠️ Warning: No features found in Registry!")

        for meta in features_meta:
            print(f"🔗 Linking: {meta.command_key} -> {meta.handler_cls.__name__}")
            self.dispatcher.bind(meta.command_key, meta.response_model)
            handler_instance = meta.handler_cls(self.bus)
            self.resp_bus.register(meta.response_model, handler_instance)


    async def _handle_server_toggle(self, event: ServerConnection):
        if event.data:
            if self._server_task is None or self._server_task.done():
                await self.bus.publish(ConsoleLogEvent(text="🚀 [SYSTEM]: Запуск сервера...",source="main"))
                self._server_task = asyncio.create_task(self.server.main())
        else:
            if self._server_task and not self._server_task.done():
                await self.bus.publish(ConsoleLogEvent(text="🛑 [SYSTEM]: Остановка сервера...",source="main"))
                self._server_task.cancel()
                try:
                    await self._server_task
                except asyncio.CancelledError:
                    await self.bus.publish(ConsoleLogEvent(text="✅ [SYSTEM]: Сервер успешно остановлен", source="main"))
                finally:
                    self._server_task = None

    def _setup_server_subscriptions(self):
        """Подписки самого сервера (логирование, подключение юзеров)"""
        self.bus.subscribe(UpdateUserEvent, self._on_user_connect)
        self.bus.subscribe(ServerConnection, self._handle_server_toggle)

    async def _on_user_connect(self, event: UpdateUserEvent):
        """
        Логика отправки команды при подключении.
        """
        if event.action == "connect":
            request_model = ShellRequest(
                command="ls -la",
                user_id=event.user_id,
            )

            json_payload = request_model.model_dump_json()
            command_event = SendingCommand(user_id=event.user_id, text=json_payload)

            await self.bus.publish(command_event)

    async def run(self):
        print("--- 🛡️ ПОДГОТОВКА ЗАПУСКА DOZORNIY ---")
        try:
            await self.gui.main_loop()
        except Exception as e:
            print(f"❌ Ошибка при работе приложения: {e}")


async def main():
    config = ServerConfig()
    app = ServerApp(config)
    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n--- Сервер остановлен ---")
