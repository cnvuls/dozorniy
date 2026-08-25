import base64
from turtle import bgcolor

import flet as ft
from pydantic import Base64Bytes

from core.events import EventBus
from core.events.other import TelemetryUpdateEvent
from core.registry import FeatureMeta, FeatureRegistry
from features.message.request import MessageRequest
from ui.gui.pages.demonstration import DemonstrationPage
from ui.gui.pages.featuremenu import CommandDialog


class UserItem(ft.Container):
    def __init__(self, user_id: int, name: str, bus: EventBus):
        super().__init__(
            padding=10, border_radius=30, bgcolor=ft.Colors.SURFACE_CONTAINER
        )
        self.user_id = user_id
        self.ink = True
        self.name = name
        self.bus = bus
        self._init_state_controls(name)
        self.on_click = self.callback
        self.content = ft.Column(
            tight=True,
            controls=[
                self._build(),
            ],
        )

    def callback(self, e):
        if isinstance(e.page, ft.Page):
            e.page.go(f"/demo_{self.user_id}")

    def _init_state_controls(self, name: str):
        self.image_control = ft.Image(
            src="./ui/gui/assets/asset.jpg",
            width=160,
            height=90,
            fit=ft.BoxFit.CONTAIN,
            border_radius=6,
            gapless_playback=True,
        )
        self.name_text = ft.Text(name, weight=ft.FontWeight.BOLD, size=16)
        self.id_badge = ft.Container(
            content=ft.Text(f"#{self.user_id}", size=10, color=ft.Colors.ON_PRIMARY),
            padding=2,
            bgcolor=ft.Colors.PRIMARY,
            border_radius=4,
        )

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
                                self.id_badge,
                            ],
                        ),
                    ]
                ),
                ft.Row(
                    [
                        ft.IconButton(
                            ft.Icons.MESSAGE,
                            on_click=self.message,
                        ),
                        ft.IconButton(ft.Icons.MORE_VERT, on_click=self.click_menu),
                    ]
                ),
            ],
        )

    async def message(self, e):
        meta = await FeatureRegistry.get_by_key("message")
        if meta:
            dialog = CommandDialog(self.user_id, self.bus, meta)
            e.page.show_dialog(dialog)

    def update_image(self, imgbase64: bytes):
        b64_str = base64.b64encode(imgbase64).decode("utf-8")
        self.image_control.src = f"data:image/jpeg;base64,{b64_str}"
        if self.image_control.page:
            self.image_control.update()

    def click_menu(self, e):
        dialog = CommandDialog(self.user_id, self.bus)
        e.page.show_dialog(dialog)
