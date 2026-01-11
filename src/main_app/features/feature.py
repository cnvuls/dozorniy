from abc import ABC, abstractmethod

from main_app.core.dispatcher import ResponseDispatcher
from main_app.core.events import EventBus
from main_app.core.responses.responsebus import ResponseBus


class AbstractFeature(ABC):
    """
    Контракт для любой фичи (Shell, Ping, SysInfo).
    Фича сама знает, какие у неё Хендлеры и Респонсы.
    """

    @abstractmethod
    def setup(
        self, dispatcher: ResponseDispatcher, resp_bus: ResponseBus, event_bus: EventBus
    ):
        pass
