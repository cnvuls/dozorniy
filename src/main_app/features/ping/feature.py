from main_app.core.dispatcher import ResponseDispatcher
from main_app.core.events import EventBus
from main_app.core.responses.responsebus import ResponseBus
from main_app.features.feature import AbstractFeature
from main_app.features.ping.handler import PingHandler
from main_app.features.ping.response import PingResponse


class ShellFeature(AbstractFeature):
    def setup(
        self, dispatcher: ResponseDispatcher, resp_bus: ResponseBus, event_bus: EventBus
    ):
        print("🔧 Setting feature: Shell")
        dispatcher.bind("shell_result", PingResponse)
        handler = PingHandler(event_bus)
        resp_bus.register(PingResponse, handler)
