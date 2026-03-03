import flet as ft

from core.events import EventBus


class DashboardPage(ft.Container):
    #TODO: убрать такую ебейшую зависимость
    def __init__(self, user_list: ft.Control, output_log: ft.Control, bus:EventBus):
        super().__init__(padding=20, expand=True)

        self.content = ft.Row(
            expand=True,
            controls=[
                user_list,
                output_log
            ]
        )
