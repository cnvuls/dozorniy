import flet as ft

from core.events import EventBus
from ui.abstracts import UiAbstract
from ui.abstracts.base import ServerConnection
from ui.gui.components import output_log, user_list
from ui.gui.components.logs_list import ListLog
from ui.gui.components.output_log import OutputLog
from ui.gui.components.user_list import ListUsers
from ui.gui.pages.dashboard import DashboardPage
from ui.gui.pages.demonstration import DemonstrationPage
from ui.gui.pages.logs import LogsPage
from ui.gui.utils.catppuccin import get_catppuccin_theme


class DozorniyApp(UiAbstract):
    def __init__(self, bus: EventBus):
        self.page: ft.Page
        self.bus: EventBus = bus
        self.log_window = OutputLog(bus=self.bus)
        self.list_log = ListLog(bus=self.bus)

        self.content_holder = ft.Container(expand=True, padding=20)

    async def route_change(self, e: ft.RouteChangeEvent | None = None):
        route = e.route if e else self.page.route
        fullscreen = False
        print(route)
        new_content: ft.Container
        if route == "/":
            new_content = DashboardPage(output_log=self.log_window, bus=self.bus)
        elif route == "/logs":
            new_content = LogsPage(list_log=self.list_log)
        elif route.startswith("/demo"):
            print(route.split("_"))
            new_content = DemonstrationPage(
                user_id=int(route.split("_")[1]), bus=self.bus
            )
            fullscreen = True
        else:
            return
        if fullscreen:
            layout = ft.Row(controls=[new_content], expand=True, spacing=0)
        else:
            layout = ft.Row(
                controls=[self.sidebar, new_content], expand=True, spacing=0
            )
        self.page.views.clear()
        self.page.views.append(
            ft.View(
                route=route,
                controls=[layout],
                bgcolor=ft.Colors.SURFACE_DIM,
                spacing=0,
            )
        )
        self.page.update()

    async def navigate(self, e):
        if self.page is None:
            return

        if e.data is None:
            return

        routes = ["/", "/logs"]
        self.page.go(routes[int(e.data)])

    async def _toggle_switch(self, e):
        await self.bus.publish(ServerConnection(data=e.data))

    async def main(self, page: ft.Page):
        self.page = page
        self.page.on_route_change = self.route_change
        self.page.data = self
        self.page.title = "Dozorniy RMM"
        self.page.theme = ft.Theme(
            color_scheme=get_catppuccin_theme(),
            page_transitions=ft.PageTransitionsTheme(
                linux=ft.PageTransitionTheme.OPEN_UPWARDS
            ),
        )
        self.page.bgcolor = ft.Colors.SURFACE_DIM
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
                ft.NavigationRailDestination(icon=ft.Icons.MONITOR_HEART, label="Логи"),
            ],
            on_change=self.navigate,
            trailing=self.server_switch,
        )

        await self.route_change()

    async def main_loop(self):
        await ft.app_async(
            main=self.main,
            assets_dir="gui/flet/assets",
        )
