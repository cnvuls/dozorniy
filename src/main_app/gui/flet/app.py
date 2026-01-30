import flet as ft
from flet import controls

from main_app.gui.flet.views.dashboard import DashboardPage
from main_app.gui.flet.views.settings import SettingsPage

class DozorniyApp:
    def __init__(self):
        self.page: ft.Page | None = None
        self.content_area: ft.Container | None = None

        self.dashboard = DashboardPage()
        self.settings = SettingsPage()

    async def navigate(self, e):
        selected_index = e.control.selected_index

        if self.content_area:
            if selected_index == 0:
                self.content_area.content = self.dashboard
            elif selected_index == 1:
                self.content_area.content = self.settings

            self.content_area.update()

    async def main(self, page: ft.Page):
        self.page = page
        self.page.title = "Dozorniy RMM"
        self.page.theme = ft.Theme(color_scheme_seed="blue")
        self.page.padding = 0

        self.content_area = ft.Container(
            content=self.dashboard,
            expand=True,
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
        )

        main_layout_controls: list[ft.Control] = [
            self.sidebar,
            ft.VerticalDivider(width=1),
            self.content_area,
        ]

        layout = ft.Row(controls=main_layout_controls, expand=True, spacing=0)
        self.page.add(layout)


if __name__ == "__main__":
    app = DozorniyApp()
    ft.app(target=app.main)
