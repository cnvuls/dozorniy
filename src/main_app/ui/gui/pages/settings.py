import flet as ft

class SettingsPage(ft.Container):
    def __init__(self):
        super().__init__(padding=20, alignment=ft.alignment.Alignment.TOP_LEFT)

        self.port_input = ft.TextField(label="Server Port", value="8000")

        settings_controls: list[ft.Control] = [
            ft.Text("Global Settings", size=25),
            self.port_input,
            ft.ElevatedButton(
                "Save Config", icon=ft.Icons.SAVE, on_click=self.save_config
            ),
        ]

        self.content = ft.Column(controls=settings_controls)

    async def save_config(self):
        print(f"Saving config: Port {self.port_input.value}")







