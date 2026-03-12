from enum import IntEnum

import flet as ft
from core.events import EventBus
from ui.abstracts import UiAbstract
from ui.abstracts.base import ServerConnection
from ui.gui.components.logs_list import ListLog
from ui.gui.components.output_log import OutputLog
from ui.gui.components.user_list import ListUsers
from ui.gui.pages.dashboard import DashboardPage
from ui.gui.pages.logs import LogsPage
from ui.gui.pages.settings import SettingsPage


class Routes(IntEnum):
    DASHBOARD = 0
    LOGS = 1
    SETTINGS = 2


class DozorniyApp(UiAbstract):
    def __init__(self, bus: EventBus):
        self.page: ft.Page | None = None
        self.bus: EventBus = bus
        self.user_list_view = ListUsers(bus=self.bus)
        self.log_window = OutputLog(bus=self.bus)
        self.list_log = ListLog(bus=self.bus)

        self.dashboard = DashboardPage(
            user_list=self.user_list_view, output_log=self.log_window
        )
        self.settings = SettingsPage()
        self.logs = LogsPage(self.list_log)

        self.content_holder = ft.Container(expand=True, padding=20)

        self.pages: dict[int, ft.Container] = {
            Routes.DASHBOARD: ft.Container(
                content=self.dashboard, visible=True, expand=True
            ),
            Routes.LOGS: ft.Container(
                content=ft.Container(content=self.logs), visible=False, expand=True
            ),
            Routes.SETTINGS: ft.Container(
                content=self.settings, visible=False, expand=True
            ),
        }

    async def navigate(self, e):
        selected_index = int(e.data)
        if self.page is None:
            return
        new_page = self.pages[selected_index]

        new_page.visible = True

        self.content_holder.content = new_page
        self.content_holder.update()

    async def _toggle_switch(self, e):
        print(e)
        await self.bus.publish(ServerConnection(data=e.data))

    async def main(self, page: ft.Page):
        self.page = page
        self.page.title = "Dozorniy RMM"
        self.page.theme = ft.Theme(color_scheme_seed="red")
        self.page.padding = 0
        self.server_switch = ft.Switch(
            value=False,
            active_color=ft.Colors.PRIMARY,
            on_change=self._toggle_switch,
        )

        self.content_holder.content = self.dashboard

        self.sidebar = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD, label="Монитор"),
                ft.NavigationRailDestination(icon=ft.Icons.MONITOR_HEART, label="Логи"),
                ft.NavigationRailDestination(icon=ft.Icons.SETTINGS, label="Опции"),
            ],
            on_change=self.navigate,
            trailing=self.server_switch,
        )

        layout = ft.Row(
            controls=[self.sidebar, ft.VerticalDivider(width=1), self.content_holder],
            expand=True,
            spacing=0,
        )

        self.page.add(layout)

    async def main_loop(self):
        await ft.app_async(main=self.main, assets_dir="gui/flet/assets")
