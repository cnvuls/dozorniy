import asyncio

import flet as ft
from core.events import EventBus
from core.events.other import RequestFeatureList, ResponseFeatureList
from core.registry import FeatureMeta


class FeatureList(ft.Column):  # 1. Наследуемся от Column, у него есть .controls
    def __init__(self, bus: EventBus):
        super().__init__()
        self.page: ft.Page
        self.bus = bus
        self.width = 300
        self.height = 400

        self.command_list = ft.ListView(expand=True, spacing=5)
        self.controls = [self.command_list]

        self.bus.subscribe(ResponseFeatureList, self.render_features)

    def did_mount(self):
        self.page.run_task(self._initial_load)

    async def _initial_load(self):
        await self.bus.publish(RequestFeatureList())

    async def render_features(self, event: ResponseFeatureList):
        if not self.page:
            return

        self.command_list.controls.clear()
        for meta in event.content:
            self.command_list.controls.append(
                ft.ListTile(
                    title=ft.Text(meta.name),
                    subtitle=ft.Text(f"{meta.version}, {meta.command_key}"),
                    on_click=lambda e, m=meta: self.page.run_task(
                        self._handle_click, m
                    ),
                )
            )

        self.command_list.update()

    async def _handle_click(self, meta: FeatureMeta):
        if not meta.args_model:
            await self.bus.publish(event=meta.request_model)
