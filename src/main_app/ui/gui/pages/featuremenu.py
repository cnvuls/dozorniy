import asyncio
from sys import version

import flet as ft
from core.events import EventBus
from core.events.other import RequestFeatureList, ResponseFeatureList
from core.registry import FeatureMeta
from ui.gui.components.feature_list import FeatureList

# TODO: Сделать раздельные классы


class CommandDialog(ft.AlertDialog):
    def __init__(self, user_id: int, bus: EventBus):
        super().__init__()
        self.user_id: int = user_id
        self.title = ft.Text(f"Комманды сервера {self.user_id}")
        self.bus = bus
        feature_list = FeatureList(self.bus)
        self.content = feature_list

        self.actions = [ft.TextButton("Закрыть", on_click=self.close_dialog)]

    def close_dialog(self):
        self.page.pop_dialog()
