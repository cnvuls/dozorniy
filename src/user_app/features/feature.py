# Copyright (c) 2026 hackhype. SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

from abc import ABC, abstractmethod

from core.dispatcher import RequestDispatcher
from core.events import EventBus
from core.responses.bus import ResponseBus


class AbstractFeature(ABC):
    """
    Контракт для любой фичи (Shell, Ping, SysInfo).
    Фича сама знает, какие у неё Хендлеры и Респонсы.
    """

    @abstractmethod
    def setup(
        self, dispatcher: RequestDispatcher, resp_bus: ResponseBus, event_bus: EventBus
    ):
        pass
