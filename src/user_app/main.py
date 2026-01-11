# Copyright (c) 2026 hackhype. SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

import asyncio
import os
from dataclasses import dataclass
from typing import Optional

from connection.websocket import WebsocketConnection
from core.dispatcher import RequestDispatcher, ResponseDispatcher
from core.events import EventBus
from core.responses.bus import ResponseBus
from features.shell.handler import ShellHandler
from features.shell.responses import ShellCommand


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
        self._status_task: Optional[asyncio.Task] = None

    def _init_layers(self):
        """Сборка архитектуры"""

        self.req_dispatcher = RequestDispatcher(self.bus)

        self.resp_bus = ResponseBus()
        self.resp_dispatcher = ResponseDispatcher(self.resp_bus, self.bus)

        shell_handler = ShellHandler(dispatcher=self.req_dispatcher)
        self.resp_dispatcher.bind("shell", ShellCommand)
        self.resp_bus.register(ShellCommand, shell_handler)

        print(
            f"[ClientApp] Init complete. Handlers: {list(self.resp_bus._handlers.keys())}"
        )

    async def run(self) -> None:
        await self.connection.main_loop()


async def main() -> None:
    config = ClientConfig()
    app = ClientApp(config)
    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Client] Stopped.")
