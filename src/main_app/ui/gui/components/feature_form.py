import flet as ft
from pydantic_core import PydanticUndefined

from core.events import EventBus, SendingCommand
from core.registry import FeatureMeta
from core.requests.base import RequestBase


class FeatureForm(ft.Container):
    def __init__(self, meta: FeatureMeta, bus: EventBus, user_id, on_back):
        super().__init__()
        self.page: ft.Page
        self.meta = meta
        self.bus = bus
        self.width = 300
        self.height = 400
        self.user_id: int = user_id
        self.on_back = on_back
        self.inputs = {}

        field_controls = []
        if self.meta.args_model:
            for name, field in self.meta.args_model.model_fields.items():
                if name in RequestBase.__annotations__.keys():
                    continue

                is_required = field.default is PydanticUndefined
                ctrl: ft.Control
                if field.annotation is bool:
                    val_bool = False if is_required else bool(field.default)
                    ctrl = ft.Checkbox(
                        label=name,
                        value=val_bool,
                    )
                else:
                    val_str = "" if is_required else str(field.default)
                    ctrl = ft.TextField(
                        label=name, hint_text=field.description or "", value=val_str
                    )
                self.inputs[name] = ctrl
                field_controls.append(ctrl)

        self.content = ft.Column(
            controls=[
                ft.Text(f"Параметры: {meta.name}", size=20),
                *field_controls,
                ft.Row(
                    [
                        ft.ElevatedButton("Отправить", on_click=self.send_command),
                        ft.TextButton(
                            "Назад", on_click=lambda _: self.page.run_task(self.on_back)
                        ),
                    ]
                ),
            ]
        )

    async def send_command(self, e):
        if not self.meta.args_model:
            return

        data = {name: ctrl.value for name, ctrl in self.inputs.items()}
        data["user_id"] = self.user_id

        try:
            validated = self.meta.args_model(**data)
            payload = validated.model_dump_json()
            await self.bus.publish(SendingCommand(user_id=self.user_id, text=payload))

            await self.on_back()
        except Exception as ex:
            print(f"❌ Ошибка валидации: {ex}")
