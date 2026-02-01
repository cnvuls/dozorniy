import time

# INFO: Импорты изменены согласно новой логике именования
from features.ping.response import PingResponse  # Входящий (от агента)

from core.events import EventBus
from core.registry import FeatureRegistry
from core.responses.base import \
    ResponseHandler  # INFO: Наследуемся от ResponseHandler
from features.ping.request import \
    PingRequest  # Исходящий (от сервера)


@FeatureRegistry.register(command_key="ping", response_model=PingResponse)
class PingHandler(ResponseHandler):
    def __init__(self, event_bus: EventBus) -> None:
        self.event_bus = event_bus

    async def handle(self, response: PingResponse) -> None:

        # 1. Логика (получаем текущее время)
        current_time = time.time()

        # 2. Создаем исходящую команду (Request), которая полетит агенту
        # INFO: Передаем user_id из входящего сообщения
        pong_request = PingRequest(user_id=response.user_id, server_time=current_time)

        # 3. Вывод в консоль
        # TODO: Интегрировать с шиной событий для реальной отправки через WebSocket
        print(f"--- 🏓 PONG! User ID: {response.user_id} ---")
        print(f"Server Time: {pong_request.server_time}")
        print(f"Full JSON for Client: {pong_request.model_dump_json()}")
