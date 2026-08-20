from connection import web_socket
from connection.abstracts import ConnectionBase
from core.abstracts import AbstractFactory
from core.events import EventBus
from connection.web_socket import WebSocketConnection


class ConnectionFactory(AbstractFactory):
    _TYPES: dict[str, type[ConnectionBase]] = {
        "ws": WebSocketConnection,
    }

    @staticmethod
    def create_object(bus: EventBus, **kwargs) -> ConnectionBase:
        mode = kwargs.get("mode", "ws")
        connection_cls = ConnectionFactory._TYPES.get(mode)

        if connection_cls is None:
            raise ValueError(f"Неизвестный тип подключения {mode}")

        return connection_cls(bus)
