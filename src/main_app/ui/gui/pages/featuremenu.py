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
        self.feature_list = FeatureList(
            self.bus, on_select_feature=self.open_feature_form
        )
        self.content = self.feature_list

    def close_dialog(self):
        self.page.pop_dialog()

    async def open_feature_form(self, meta: FeatureMeta):
        from ui.gui.components.feature_form import FeatureForm

        form = FeatureForm(meta, self.bus, on_back=self.restore_list)

        self.content = form

        self.update()

    async def restore_list(self):
        self.content = self.feature_list
        self.update()
