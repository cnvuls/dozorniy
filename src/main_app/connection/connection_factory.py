from config.settings import Config
from connection import web_socket
from connection.abstracts import ConnectionBase
from core.abstracts import AbstractFactory
from core.events import EventBus


class ConnectionFactory(AbstractFactory):
    @staticmethod
    def create_object(bus: EventBus, config: Config, **_) -> ConnectionBase:
        types_of_connection: dict[str, ConnectionBase] = {
            "ws": web_socket.WebSocketConnection(bus)
        }
        return types_of_connection[config.connection_mode]
