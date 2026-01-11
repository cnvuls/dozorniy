from __future__ import annotations

from typing import Dict, Type

from core.input_handler.base import BaseHandler
from core.input_handler.message import MessageHandler
from core.output_handler.base import BaseCommand
from core.output_handler.message import MessageCommand
from core.output_handler.server_command import ServerCommandRequest

IncomingHandler = Type[BaseHandler]
IncomingHandlerRegistry = Dict[str, IncomingHandler]

OutgoingHandler = Type[BaseCommand]
OutgoingHandlerRegistry = Dict[str, OutgoingHandler]

# Map incoming message types to their handlers.
INCOMING_HANDLERS: IncomingHandlerRegistry = {
    "message": MessageHandler,
}

# Map outgoing command types to their implementations.
OUTGOING_COMMANDS: OutgoingHandlerRegistry = {
    MessageCommand.type: MessageCommand,
    ServerCommandRequest.type: ServerCommandRequest,
}

__all__ = [
    "IncomingHandler",
    "IncomingHandlerRegistry",
    "INCOMING_HANDLERS",
    "OutgoingHandler",
    "OutgoingHandlerRegistry",
    "OUTGOING_COMMANDS",
]
