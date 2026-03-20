import flet as ft

from core.events import EventBus
from ui.gui.components import user_list
from ui.gui.components.user_list import ListUsers


class DashboardPage(ft.Container):
    # TODO: убрать такую ебейшую зависимость
    def __init__(self, output_log: ft.Control, bus: EventBus):
        super().__init__(padding=20, expand=True)
        self.user_list = ListUsers(bus)
        self.content = ft.Row(expand=True, controls=[output_log, self.user_list])
