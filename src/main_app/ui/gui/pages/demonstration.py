import base64

import flet as ft

from core.events import ConsoleLogEvent, EventBus
from core.events.network import FrameData
from features.screen.request import FrameTimeOption, ScreenRequest
from ui.gui.components.feature_list import FeatureList
from ui.gui.components.output_log import OutputLog


class DemonstrationPage(ft.Container):
    def __init__(self, user_id: int, bus: EventBus):
        super().__init__(expand=True, bgcolor=ft.Colors.BLACK)
        self.user_id = user_id
        self.bus = bus
        self.demo = ft.Image(
            src="./ui/gui/assets/asset.jpg",
            fit=ft.BoxFit.CONTAIN,
            gapless_playback=True,
        )
        self.feature_list = FeatureList(
            self.bus, on_select_feature=self.open_feature_form
        )

        self.log_window = OutputLog(bus=self.bus)

        self.menu_container = ft.Container(
            content=self.feature_list,
            width=300,
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.SURFACE),
            padding=15,
            border_radius=15,
            visible=False,
        )

        stack_controls: list[ft.Control] = [
            ft.Container(content=self.demo, alignment=ft.Alignment.CENTER),
            ft.IconButton(
                icon=ft.Icons.MENU,
                icon_color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLACK45,
                top=20,
                left=20,
                on_click=self.toggle_menu,
            ),
            ft.IconButton(
                icon=ft.Icons.CLOSE,
                icon_color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLACK45,
                top=20,
                right=20,
                on_click=self.close,
            ),
            ft.Container(
                content=self.menu_container,
                top=80,
                left=20,
                bottom=250,
            ),
            ft.Container(
                content=self.log_window,
                height=200,
                left=20,
                right=20,
                bottom=20,
                padding=10,
                bgcolor=ft.Colors.BLACK45,
            ),
        ]

        self.content = ft.Stack(controls=stack_controls)

    async def close(self, _):
        await self.bus.publish(
            ScreenRequest(
                user_id=self.user_id,
                window_fullscreen=False,
                frame_time=FrameTimeOption.SLOW,
            )
        )
        self.page.go("/")

    async def start(self):
        await self.bus.publish(
            ScreenRequest(
                user_id=self.user_id,
                window_fullscreen=True,
                frame_time=FrameTimeOption.FAST,
            )
        )

    def did_mount(self):
        self.page.run_task(self.start)
        self.bus.subscribe(FrameData, self.update_frame)

    def will_unmount(self):
        self.bus.unsubscribe(FrameData, self.update_frame)

    async def toggle_menu(self, e):
        self.menu_container.visible = not self.menu_container.visible
        self.update()

    async def open_feature_form(self, meta):
        from ui.gui.components.feature_form import FeatureForm

        form = FeatureForm(
            meta, self.bus, user_id=self.user_id, on_back=self.restore_list
        )
        self.menu_container.content = form
        self.update()

    async def restore_list(self):
        self.menu_container.content = self.feature_list
        self.update()

    async def update_frame(self, event: FrameData):
        if event.user_id == self.user_id:
            b64_str = base64.b64encode(event.base64_img).decode("utf-8")
            self.demo.src = b64_str
            self.demo.update()
