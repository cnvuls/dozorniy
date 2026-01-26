import flet as ft


class UserList(ft.Column):
    def __init__(self):
        pass

class DashboardPage(ft.Container):
    def __init__(self):
        super().__init__(padding=20, alignment=ft.Alignment.TOP_LEFT)
        
        self.status_text = ft.Text("System Status: ONLINE", color=ft.Colors.GREEN)
        self.logs_view = ft.Column(scroll=ft.ScrollMode.AUTO)

        dashboard_controls: list[ft.Control] = [
            ft.Row(
                [ft.OutlinedButton(content="Запустить",expand=True), ft.OutlinedButton(content="Остановить",expand=True)],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            self.status_text,
            ft.Divider(),
            ft.Row(
                controls=[ 
                    ft.Icon(ft.Icons.INFO_OUTLINE, color=ft.Colors.BLUE),
                    ft.Text("Waiting for agents to connect...")
                ]
            ),
        ]
        self.content = ft.Column(controls=dashboard_controls)

    def update_status(self, new_status: str):
        self.status_text.value = new_status
        self.update()


class SettingsPage(ft.Container):
    def __init__(self):
        super().__init__(padding=20, alignment=ft.alignment.Alignment.TOP_LEFT)
        
        self.port_input = ft.TextField(label="Server Port", value="8000")
        
        settings_controls: list[ft.Control] = [
            ft.Text("Global Settings", size=25),
            self.port_input,
            ft.ElevatedButton("Save Config", icon=ft.Icons.SAVE, on_click=self.save_config)
        ]

        self.content = ft.Column(controls=settings_controls)

    def save_config(self, e):
        print(f"Saving config: Port {self.port_input.value}")


class DozorniyApp:
    def __init__(self):
        self.page: ft.Page | None = None
        self.content_area: ft.Container | None = None 
        
        self.dashboard = DashboardPage()
        self.settings = SettingsPage()

    def navigate(self, e):
        selected_index = e.control.selected_index
        
        if self.content_area: 
            if selected_index == 0:
                self.content_area.content = self.dashboard
            elif selected_index == 1:
                self.content_area.content = self.settings
            
            self.content_area.update()

    def main(self, page: ft.Page):
        self.page = page
        self.page.title = "Dozorniy RMM [OOP Edition]"
        self.page.theme = ft.Theme(color_scheme_seed="orange")
        self.page.padding = 0

        self.content_area = ft.Container(
            content=self.dashboard, 
            expand=True, 
            
        )

        self.sidebar = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD, label="Монитор"),
                ft.NavigationRailDestination(icon=ft.Icons.EXTENSION, label="Плагины"),
                ft.NavigationRailDestination(icon=ft.Icons.SETTINGS, label="Опции"),
            ],
            on_change=self.navigate
        )

        main_layout_controls: list[ft.Control] = [
            self.sidebar, 
            ft.VerticalDivider(width=1), 
            self.content_area
        ]

        layout = ft.Row(controls=main_layout_controls, expand=True, spacing=0)
        self.page.add(layout)

if __name__ == "__main__":
    app = DozorniyApp()
    ft.app(target=app.main)
