from main_app.gui.flet.components.user_item import UserItem
import flet as ft

class ListUsers(ft.ListView):
    def __init__(self):
        super().__init__(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
        for i in range(100):
            l = UserItem(i,"hui")
            print(i)
            self.controls.append(l)
        

    async def adduser(self, user_id: int, user_name: str):
        pass
