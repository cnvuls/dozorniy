import asyncio
from gui.flet.components.user_item import UserItem
import flet as ft

class ListUsers(ft.ListView):
    def __init__(self):
        super().__init__(
            expand=True,
            spacing=10,
            padding=10
        )
  
        for i in range(100):
            self.controls.append(UserItem(i, f"Dozorniy_Agent_{i}"))
