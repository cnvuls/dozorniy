from config.settings import Config
from core.abstracts import AbstractFactory
from core.events import EventBus
from gui.abstracts import UiAbstract
from gui.cli import Cli


class GuiFactory(AbstractFactory):
    @staticmethod
    def create_object(bus: EventBus, config: Config, **kwargs) -> UiAbstract:
        state_store = kwargs.get("state_store")
        types_of_ui: dict[str, UiAbstract] = {"cli": Cli(bus, state_store=state_store)}
        return types_of_ui[config.gui_type]
