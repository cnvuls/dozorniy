import flet as ft


class CommandDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.title = ft.Text("Комманды сервера")

        self.content = ft.ListView(
            controls=[
                ft.ListTile(title="default", trailing=ft.Icon(ft.Icons.EXTENSION), on_click=lambda _: print("hello, world!")) for _ in range(1,5)
            ],
            width=300
        )
        self.actions = [
            ft.TextButton("Закрыть", on_click=self.close_dialog)
        ]
        
    def close_dialog(self):
        self.page.pop_dialog()
