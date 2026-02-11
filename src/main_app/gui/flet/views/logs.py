import flet as ft


class LogsPage(ft.Container):
    def __init__(self, list_log: ft.Container):
        super().__init__(padding=20, expand=True)
        
        self.content=list_log

