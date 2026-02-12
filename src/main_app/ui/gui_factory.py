from core.abstracts import AbstractFactory
from core.events import EventBus
from ui.abstracts import UiAbstract
from ui.gui.app import DozorniyApp


class GuiFactory(AbstractFactory):
    @staticmethod
    def create_object(bus: EventBus, **kwargs) -> UiAbstract:
        types_of_ui: dict[str, UiAbstract] = {"flet": DozorniyApp(bus)}
        return types_of_ui["flet"]
