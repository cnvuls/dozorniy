from turtle import bgcolor

import flet as ft
from core.events import EventBus
from core.events.other import TelemetryUpdateEvent
from ui.gui.pages.featuremenu import CommandDialog





# TODO: Переделать в listitem
class UserItem(ft.Container):
    def __init__(self, user_id: int, name: str, bus: EventBus):
        super().__init__(
            padding=10,
            border_radius=8,
            border=ft.border.all(1, ft.Colors.PRIMARY),
        )
        self.user_id = user_id

        # TODO: Переделать телеметрию
        self.ink = True
        self.bus = bus
        self.on_click = lambda x: x
        self._init_state_controls(name)

        self.content = ft.Column(
            tight=True,
            controls=[
                self._build(),
            ],
        )

    def _init_state_controls(self, name: str):
        self.image_control = ft.Image(
            src="./ui/gui/assets/asset.jpg",
            width=160,
            height=90,
            fit=ft.BoxFit.COVER,
            border_radius=6,
        )
        self.name_text = ft.Text(name, weight=ft.FontWeight.BOLD, size=16)

    def _build(self):
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
            controls=[
                ft.Row(
                    [
                        ft.Container(content=self.image_control, border_radius=6),
                        ft.Column(
                            [
                                self.name_text,
                                self._build_id_badge(),
                            ],
                        ),
                    ]
                ),
                ft.IconButton(ft.Icons.MORE_VERT, on_click=self.click_menu),
            ],
        )

    def click_menu(self, _):
        dialog = CommandDialog(self.user_id, self.bus)
        self.page.show_dialog(dialog)

    def _build_id_badge(self):
        return ft.Container(
            content=ft.Text(f"#{self.user_id}", size=10, color=ft.Colors.ON_PRIMARY),
            padding=2,
            bgcolor=ft.Colors.PRIMARY,
            border_radius=4,
        )
