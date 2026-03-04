import asyncio
from sys import version
import flet as ft

from core.events import EventBus
from core.events.other import RequestFeatureList, ResponseFeatureList
from core.registry import FeatureMeta

class CommandDialog(ft.AlertDialog):
    def __init__(self, user_id:int, bus: EventBus):
        super().__init__()
        self.user_id:int=user_id
        self.title = ft.Text(f"Комманды сервера {self.user_id}")
        self.bus = bus
        self.bus.subscribe(ResponseFeatureList, self.render_features)
        self.command_list=ft.ListView(
            width=300,
            height=400,
            spacing=5
        )
        self.content = self.command_list
        self.actions = [
            ft.TextButton("Закрыть", on_click=self.close_dialog)
        ]
        asyncio.create_task(self.bus.publish(RequestFeatureList()))

    async def render_features(self, event: ResponseFeatureList):
        self.command_list.controls.clear()
        for meta in event.content:
            self.command_list.controls.append(
                ft.ListTile(
                    title=ft.Text(meta.name),
                    subtitle=ft.Text(f"{meta.version}, {meta.command_key}"),
                    on_click=lambda e, m=meta: asyncio.create_task(self._handle_click(m)))
            )
        self.command_list.update()
    
    async def _handle_click(self, meta: FeatureMeta):
        if not meta.args_model: 
            print(meta.args_model)
            await self.bus.publish(meta.request_model)
        self.page.pop_dialog()
        
    def close_dialog(self):
        self.page.pop_dialog()
