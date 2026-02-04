import flet as ft


class DashboardPage(ft.Container):
    def __init__(self, user_list: ft.Control, output_log: ft.Control):
        super().__init__(padding=20, expand=True)

        self.content = ft.Row(
            expand=True,
            controls=[
                user_list,
                output_log
            ]
        )
