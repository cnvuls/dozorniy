import os

import flet as ft
from core.events import EventBus
from gui.abstracts import UiAbstract
from gui.abstracts.base import ServerConnection
from gui.flet.components.user_list import ListUsers
from gui.flet.views.dashboard import DashboardPage
from gui.flet.views.settings import SettingsPage
from gui.flet.components.output_log import OutputLog


class DozorniyApp(UiAbstract):
    def __init__(self, bus: EventBus):
        self.page: ft.Page | None = None
        self.bus: EventBus = bus
        self.user_list_view = ListUsers()
        self.log_window = OutputLog(bus=self.bus)

        self.dashboard = DashboardPage(user_list=self.user_list_view, output_log=self.log_window)
        self.settings = SettingsPage()

        self.pages: dict[int, ft.Container] = {
            0: ft.Container(content=self.dashboard, visible=True, expand=True),
            1: ft.Container(
                content=ft.Text("Плагины в разработке"), visible=False, expand=True
            ),
            2: ft.Container(content=self.settings, visible=False, expand=True),
        }

    async def navigate(self, e):
        selected_index = int(e.data)
        if self.page is None:
            return
        for index, page_container in self.pages.items():
            page_container.visible = index == selected_index
        self.page.update()

    async def _toggle_switch(self, e):
        await self.bus.publish(ServerConnection(e.data))

    async def main(self, page: ft.Page):
        self.page = page
        self.page.title = "Dozorniy RMM"
        self.page.theme = ft.Theme(color_scheme_seed="green")
        self.page.padding = 0
        self.server_switch = ft.Switch(
            value=False,
            active_color=ft.Colors.PRIMARY,
            on_change=self._toggle_switch,
        )

        self.sidebar = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD, label="Монитор"),
                ft.NavigationRailDestination(icon=ft.Icons.EXTENSION, label="Плагины"),
                ft.NavigationRailDestination(icon=ft.Icons.SETTINGS, label="Опции"),
            ],
            on_change=self.navigate,
            trailing=self.server_switch,
        )

        self.main_stack = ft.Stack(controls=list(self.pages.values()), expand=True)

        layout = ft.Row(
            controls=[
                self.sidebar,
                ft.VerticalDivider(width=1),
                self.main_stack,
            ],
            expand=True,
            spacing=0,
        )

        self.page.add(layout)

    async def main_loop(self):
        await ft.app_async(main=self.main, assets_dir="gui/flet/assets")
