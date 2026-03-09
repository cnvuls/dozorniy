import flet as ft
from core.events import EventBus
from core.registry import FeatureMeta


class FeatureForm(ft.Container):
    def __init__(self, meta: FeatureMeta, bus: EventBus, on_back):
        super().__init__()
        self.page: ft.Page
        self.meta = meta
        self.bus = bus
        self.on_back = on_back

        self.content = ft.Column(
            [
                ft.Text(f"Поле ввода: {meta.name}"),
                # потом будет валидация
                ft.ElevatedButton(
                    "Назад", on_click=lambda _: self.page.run_task(self.on_back)
                ),
            ]
        )
