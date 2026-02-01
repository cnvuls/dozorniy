import flet as ft


class DashboardPage(ft.Container):
    def __init__(self, user_list: ft.Control):
        super().__init__(padding=20, expand=True)

        self.content = ft.Column(
            expand=True,
            controls=[
                user_list,
            ]
        )
