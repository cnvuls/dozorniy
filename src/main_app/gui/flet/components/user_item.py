import flet as ft

from gui.flet.views.featuremenu import CommandDialog 


class UserItem(ft.Container):
    def __init__(self, user_id: int, name: str):
        super().__init__(
            padding=10,
            border_radius=8,
            border=ft.border.all(1, ft.Colors.PRIMARY),
        )
        self.user_id = user_id
        self.telemetry_cache = {"window": "учит пайтон"}
        self.ink = True
        self.on_click = lambda x: x
        self._init_state_controls(name)

        self.content = ft.Column(
            tight=True,
            controls=[
                self._build_upper_section(),
                self._build_lower_section(),
            ],
        )

    def _init_state_controls(self, name: str):
        self.image_control = ft.Image(
            src="images/asset.jpg",
            width=160,
            height=90,
            fit=ft.BoxFit.COVER,
            border_radius=6,
        )
        self.name_text = ft.Text(name, weight=ft.FontWeight.BOLD, size=16)
        self.info_text = ft.Text(size=12, italic=True, color=ft.Colors.OUTLINE)
        self.refresh_info_text()

    def _build_upper_section(self):
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Row(
                    [
                        ft.Container(content=self.image_control, border_radius=6),
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        self.name_text,
                                        self._build_id_badge(),
                                    ],
                                    spacing=10,
                                ),
                                ft.Text("Онлайн", size=12, color="green"),
                            ],
                            spacing=5,
                        ),
                    ],
                    spacing=15,
                ),
                ft.IconButton(ft.Icons.MORE_VERT, on_click=self.click_menu),
            ],
        )
    
    def click_menu(self,e):
        dialog = CommandDialog(self.user_id)
        self.page.show_dialog(dialog)

    def _build_id_badge(self):
        return ft.Container(
            content=ft.Text(f"#{self.user_id}", size=10, color=ft.Colors.ON_PRIMARY),
            padding=2,
            bgcolor=ft.Colors.PRIMARY,
            border_radius=4,
        )

    def _build_lower_section(self):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.MONITOR_HEART, size=12, color=ft.Colors.OUTLINE),
                    self.info_text,
                ],
                spacing=5,
            ),
            padding=8,
            bgcolor=ft.Colors.BLACK26,
            border_radius=4,
        )
    

    def refresh_info_text(self):
        self.info_text.value = (
            f"Активность: {self.telemetry_cache.get('window', 'N/A')}"
        )
        try:
            self.update()
        except Exception:
            pass
