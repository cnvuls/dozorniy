from typing import Optional
import flet as ft


class UserItem(ft.Container):
    def __init__(self, user_id:int, name:str):
        super().__init__(
            padding=10,
            border_radius=8,
            border=ft.border.all(1, ft.Colors.PRIMARY)
        )
        self.user_id = user_id
        self.image_control = ft.Image(
            src=f"https://picsum.photos/320/200?random={user_id}",
            width=160,
            height=90,
            fit=ft.BoxFit.COVER,
            border_radius=6,
            gapless_playback=True,
        )
        
        self.preview_container = ft.Container(
            content=self.image_control,
            border_radius=10
        )
        self.name_text = ft.Text(name, weight=ft.FontWeight.BOLD, size=16)
        self.id_badge = ft.Container(
            content=ft.Text(f"#{user_id}", size=10, color=ft.Colors.ON_PRIMARY),
            padding=ft.padding.symmetric(horizontal=6, vertical=2),
            border_radius=4,
            bgcolor=ft.Colors.PRIMARY
        )
        self.content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    controls=[
                        self.preview_container,
                        ft.Row([self.name_text, self.id_badge], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(
                            ft.Icons.MORE_VERT,
                            on_click=lambda _: print("Menu: ")
                        )
                    ],
                )
            ] 
        )
    async def set_image(self, base64_str: Optional[str]):
        if base64_str:
            self.image_control.src = f"data:image/png;base64,{base64_str}"
        else:
            self.image_control.src = f"https://picsum.photos/320/200?random={self.user_id}"
        
        self.image_control.update()



