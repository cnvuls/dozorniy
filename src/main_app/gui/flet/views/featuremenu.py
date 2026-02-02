import flet as ft


class CommandDialog(ft.AlertDialog):
    def __init__(self, user_id: int):
        super().__init__()

        self.title = ft.Text("Комманды сервера")

        self.content
