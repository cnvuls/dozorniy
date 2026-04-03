import asyncio

import flet as ft

from core.events import AbstractEvent, EventBus
from ui.gui.components.user_list import ListUsers


class SortUsers(AbstractEvent):
    enable: bool


class DashboardPage(ft.Container):
    # TODO: убрать такую ебейшую зависимость

    def __init__(self, output_log: ft.Control, bus: EventBus):
        super().__init__(padding=20, expand=True)
        self.user_list = ft.Column(
            [
                ft.Row(
                    [
                        ft.FilledButton(
                            icon=ft.Icons.SORT,
                            content="Сортировка",
                            expand=True,
                            width=50,
                            on_click=lambda _: self.sortuser(bus),
                        )
                    ]
                ),
                ListUsers(bus),
            ],
            expand=True,
        )

        self.content = ft.Row(expand=True, controls=[output_log, self.user_list])

    def sortuser(self, bus: EventBus):
        asyncio.gather(bus.publish(SortUsers(enable=True)))
