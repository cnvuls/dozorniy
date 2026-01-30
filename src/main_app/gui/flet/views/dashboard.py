import flet as ft
from main_app.gui.flet.components.user_list import ListUsers


class DashboardPage(ft.Container):
    def __init__(self):
        super().__init__(padding=20, alignment=ft.Alignment.TOP_LEFT)

        self.status_text = ft.Text("System Status: ONLINE", color=ft.Colors.GREEN)
        self.logs_view = ft.Column(scroll=ft.ScrollMode.AUTO)
        listuser = ListUsers()
        dashboard_controls: list[ft.Control] = [
            ft.Row(
                [
                    ft.OutlinedButton(content="Запустить", expand=True),
                    ft.OutlinedButton(content="Остановить", expand=True),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            self.status_text,
            ft.Divider(),
            listuser,
        ]
        self.content = ft.Column(controls=dashboard_controls)

    async def update_status(self, new_status: str):
        self.status_text.value = new_status
        self.update()
