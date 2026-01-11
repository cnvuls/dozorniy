import asyncio
import json
import sys
from typing import Any, Dict, Optional, Tuple

import aioconsole
from core.events import (
    EventBus,
    OutgoingRawMessage,
    OutputConnection,
    ReceivingMessage,
)
from gui.abstracts import UiAbstract
from gui.state import GuiStateStore
from rich.console import Console


class Cli(UiAbstract):
    def __init__(self, bus: EventBus, state_store: Optional[GuiStateStore] = None):
        self.incoming = asyncio.Queue()
        self.bus: EventBus = bus
        self.Console = Console()
        self.default_user_id = 1
        self.state_store = state_store

        self.bus.subscribe(OutputConnection, self.recieve_message)
        self.bus.subscribe(ReceivingMessage, self.recieve_message)

    async def recieve_message(self, event):
        await self.incoming.put(event.text)

    async def send_message(self, *args, **kwargs):
        text = kwargs.get("text")
        if text is None:
            text = args[0] if args else ""
        try:
            payload, override_user = self._build_payload(str(text))
        except ValueError as exc:
            self.Console.print(f"[yellow][CLI] {exc}[/yellow]")
            return

        user_id = kwargs.get("user_id", override_user or self.default_user_id)
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            self.Console.print("[yellow][CLI] Некорректный user_id[/yellow]")
            return

        local_command = payload.pop("__cli_cmd__", None)
        if local_command:
            await self._handle_local_command(local_command)
            return

        await self.bus.publish(OutgoingRawMessage(data=payload, user_id=user_id))

    async def input_loop(self):
        while True:
            user_input = await aioconsole.ainput("> ")  # В будущем заменить
            await self.send_message(user_input)

    async def display_incoming(self):
        while True:
            msg = await self.incoming.get()
            sys.stdout.write("\x1b[2K\r")
            self.Console.print("[red][CLI] Получено сообщение:[/red]", msg)
            sys.stdout.flush()

    async def main_loop(self):
        await asyncio.gather(self.input_loop(), self.display_incoming())

    def _build_payload(self, raw_text: str) -> Tuple[Dict[str, Any], Optional[int]]:
        text = raw_text.strip()
        if not text:
            return {"type": "message", "data": ""}, None

        parsed = self._try_parse_json(text)
        if isinstance(parsed, dict):
            return parsed, None

        if text.startswith("/"):
            return self._parse_slash_command(text[1:].strip())

        return {"type": "message", "data": text}, None

    @staticmethod
    def _split_command(command_line: str) -> Tuple[str, str]:
        parts = command_line.split(maxsplit=1)
        name = parts[0]
        payload = parts[1] if len(parts) > 1 else ""
        return name, payload

    @staticmethod
    def _normalize_payload(text: str) -> Dict[str, Any]:
        if not text.strip():
            return {}
        parsed = Cli._try_parse_json(text)
        if isinstance(parsed, dict):
            return parsed
        return {"value": parsed if parsed is not None else text}

    @staticmethod
    def _try_parse_json(text: str) -> Optional[Any]:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None

    def _parse_slash_command(self, command_line: str) -> Tuple[Dict[str, Any], Optional[int]]:
        if not command_line:
            raise ValueError("Введите название команды после '/'.")
        name, rest = self._split_command(command_line)
        if name == "message":
            return self._parse_message_command(rest)
        if name == "command":
            return self._parse_command_command(rest), None
        if name == "state":
            return {"__cli_cmd": "state"}, None
        raise ValueError(f"Неизвестная команда '/{name}'")

    def _parse_message_command(self, rest: str) -> Tuple[Dict[str, Any], Optional[int]]:
        if not rest:
            raise ValueError("После /message укажите текст сообщения.")
        user_override: Optional[int] = None
        parts = rest.split(maxsplit=1)
        text_part = rest
        if parts and parts[0].isdigit():
            user_override = int(parts[0])
            text_part = parts[1] if len(parts) > 1 else ""
        return {"type": "message", "data": text_part}, user_override

    def _parse_command_command(self, rest: str) -> Dict[str, Any]:
        if not rest:
            raise ValueError("После /command укажите имя команды.")
        command_name, payload_text = self._split_command(rest)
        payload = self._normalize_payload(payload_text)
        return {
            "type": "command",
            "command": command_name,
            "payload": payload,
        }

    async def _handle_local_command(self, name: str) -> None:
        if name == "state":
            if not self.state_store:
                self.Console.print("[yellow][CLI] Хранилище состояния GUI отключено[/yellow]")
                return
            snapshot = self.state_store.snapshot()
            self.Console.print("[cyan][CLI] Подключённые клиенты:[/cyan]", snapshot.users)
            self.Console.print(
                "[cyan][CLI] Последние сообщения:[/cyan]",
                "\n".join(snapshot.last_messages) or "—",
            )
            self.Console.print(
                "[cyan][CLI] Последние события:[/cyan]",
                "\n".join(snapshot.last_logs) or "—",
            )
            return
        self.Console.print(f"[yellow][CLI] Неизвестная локальная команда '{name}'[/yellow]")
