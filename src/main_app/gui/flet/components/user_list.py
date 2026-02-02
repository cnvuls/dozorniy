import asyncio

import flet as ft
from gui.flet.components.user_item import UserItem


class ListUsers(ft.ListView):
    def __init__(self):
        super().__init__(expand=True, spacing=10, padding=10)

        for i in range(10):
            self.controls.append(UserItem(i, f"Dozorniy_Agent_{i}"))
