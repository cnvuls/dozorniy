import flet as ft

from core.events import EventBus
from ui.abstracts import UiAbstract
from ui.abstracts.base import ServerConnection
from ui.gui.components import output_log
from ui.gui.components.logs_list import ListLog
from ui.gui.components.output_log import OutputLog
from ui.gui.components.user_list import ListUsers
from ui.gui.pages.dashboard import DashboardPage
from ui.gui.pages.logs import LogsPage
from ui.gui.utils.catppuccin import get_catppuccin_theme


class DozorniyApp(UiAbstract):
    def __init__(self, bus: EventBus):
        self.page: ft.Page
        self.bus: EventBus = bus
        self.user_list_view = ListUsers(bus=self.bus)
        self.log_window = OutputLog(bus=self.bus)
        self.list_log = ListLog(bus=self.bus)

        self.content_holder = ft.Container(expand=True, padding=20)

    async def route_change(self, e: ft.RouteChangeEvent):
        if not self.page:
            return
        new_content: ft.Container
        if e.route == "/":
            new_content = DashboardPage(
                user_list=self.user_list_view, output_log=self.log_window
            )
        elif e.route == "/logs":
            new_content = LogsPage(list_log=self.list_log)
        else:
            return
        layout = ft.Row(
            controls=[self.sidebar, self.divider, new_content],
            expand=True,
            spacing=0,
        )
        self.page.views.clear()
        self.page.views.append(ft.View(route=self.page.route, controls=[layout]))
        self.page.update()

    def back_to_dashboard(self):
        self.user_list_view.start_screen_updates()

        self.sidebar.visible = True
        self.divider.visible = True

        if self.page:
            self.page.update()

    def toggle_fullscreen(self, show: bool, control: ft.Control):
        self.user_list_view.stop_screen_updates()

        self.sidebar.visible = not show
        self.divider.visible = not show
        if control:
            self.content_holder.content = control

        if self.page:
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
        self.page.data = self
        self.page.on_route_change = self.route_change
        self.page.title = "Dozorniy RMM"
        self.page.theme = ft.Theme(
            color_scheme=get_catppuccin_theme(),
            page_transitions=ft.PageTransitionsTheme(
                linux=ft.PageTransitionTheme.OPEN_UPWARDS
            ),
        )

        self.page.padding = 0
        self.server_switch = ft.Switch(
            value=False,
            active_color=ft.Colors.PRIMARY,
            on_change=self._toggle_switch,
        )
        self.divider = ft.VerticalDivider(width=1)
        self.content_holder.content = DashboardPage(
            user_list=self.user_list_view, output_log=self.log_window
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

        layout = ft.Row(
            controls=[self.sidebar, self.divider, self.content_holder],
            expand=True,
            spacing=0,
        )

        self.page.add(layout)

    async def main_loop(self):
        await ft.app_async(main=self.main, assets_dir="gui/flet/assets")
