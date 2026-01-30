import flet as ft


class UserItem(ft.Container):
    def __init__(self, user_id:int):
        super().__init__(
            padding=10,
            border_radius=8,
            border=ft.border.all(1, ft.Colors.PRIMARY)
        )
        self.preview = ft.Container(
            ft.Image(
                src=f"https://picsum.photos/320/200?random={user_id}",
                width=160,
                height=90,
                fit=ft.BoxFit.COVER,
                border_radius=10
            ),
            
        )
        self.content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    controls=[
                        self.preview,
                        ft.Text(f"Индекс : {user_id}",color=ft.Colors.PRIMARY)
                    ],

                ),
                ft.Row(
                    controls=[
                        ft.IconButton(ft.Icons.EXTENSION)
                    ],

                )
            ] 
        )



