import asyncio
from typing import Literal
import flet as ft

class UiAbstract: pass 

class MessageItem(ft.Container):
    def __init__(self, text: str, type: Literal['error', 'info', 'warning']):
        super().__init__()
        
        if type == 'error':
            color = ft.Colors.ERROR 
            icon = ft.Icons.ERROR_OUTLINE
        elif type == 'warning':
            color = ft.Colors.AMBER
            icon = ft.Icons.WARNING_AMBER
        else:
            color = ft.Colors.PRIMARY 
            icon = ft.Icons.INFO_OUTLINE

        self.content = ft.Row(
            controls=[
                ft.Icon(icon, color=color, size=16),
                ft.Text(text, color=color, font_family="Consolas", size=12, selectable=True, expand=True)
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
        self.padding = ft.Padding(left=0, top=0, right=0, bottom=5)

class OutputList(ft.Column):
    def __init__(self):
        super().__init__()
        self.spacing = 5
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True 
        self.auto_scroll = True 
        
        self.controls.append(MessageItem("System initialized", "info"))
        self.controls.append(MessageItem("Waiting for agents...", "warning"))
        self.controls.append(MessageItem("Waiting for agents...", "error"))
        
    def add_message(self, text: str, type: Literal['error', 'info', 'warning'] = "info"):
        item = MessageItem(text, type)
        self.controls.append(item)
        try:
            if self.page: self.update()
        except: pass 

class FeatureStoreDialog(ft.AlertDialog):
    def __init__(self, agent_name):
        super().__init__()
        self.title = ft.Text(f"📦 Repository: {agent_name}")

        self.content = ft.Container(
            content=ft.Column([
                ft.Row([ft.ProgressRing(width=16, height=16), ft.Text("Fetching manifests...")]),
                ft.Divider(),
                ft.Text("No local modules found.", italic=True, color=ft.Colors.OUTLINE),
                ft.ElevatedButton("Browse Community Store", icon=ft.Icons.CLOUD_DOWNLOAD, width=200)
            ])
        )
        
        self.actions = [
            ft.TextButton("Cancel", on_click=self.close_dialog)
        ]

    def close_dialog(self, e):
        self.page.pop_dialog()

class AgentItem(ft.Container): 
    def __init__(self, agent_name: str, agent_id: int, on_delete_callback):
        super().__init__()
        self.agent_name = agent_name
        self.agent_id = agent_id
        self.on_delete_callback = on_delete_callback
        
        self.padding = 10
        self.border_radius = 10 
      
        self.btn_demonstration = ft.IconButton(
            icon=ft.Icons.MONITOR_OUTLINED, 
            tooltip="Демонстрация экрана",
            icon_color=ft.Colors.ON_SURFACE_VARIANT, 
            on_click=self.message_clicked
        )

        self.btn_delete = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            tooltip="Удалить агента",
            icon_color=ft.Colors.ERROR, 
            on_click=self.delete_clicked
        )

        self.btn_manage = ft.IconButton(
            icon=ft.Icons.EXTENSION_OUTLINED, 
            tooltip="Другие комманды",
            icon_color=ft.Colors.ON_SURFACE_VARIANT, 
            on_click=self.open_store
        )

        self.txt_name = ft.Text(
            agent_name, 
            weight=ft.FontWeight.BOLD,
            size=14,
            color=ft.Colors.ON_SURFACE_VARIANT 
        )

        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row([
                    ft.Icon(ft.Icons.COMPUTER, size=20, color=ft.Colors.PRIMARY), 
                    self.txt_name
                ]),
                ft.Row(spacing=0, controls=[self.btn_demonstration, self.btn_delete, self.btn_manage]),
            ],
        )
    
    def open_store(self, e):
        dialog = FeatureStoreDialog(self.agent_name)
        self.page.show_dialog(dialog)

    async def message_clicked(self, e):
        print(f"[{self.agent_name}] Msg...")
        
    async def delete_clicked(self, e):
        self.btn_delete.disabled = True
        self.update()
        await self.on_delete_callback(self)


class AgentList(ft.Column):
    def __init__(self):
        super().__init__()
        self.spacing = 10
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True
        for i in range(1, 8):
            self.add_agent(f"Student-PC-{i}", 192+i)

    def add_agent(self, name: str, uid: int):
        agent = AgentItem(agent_name=name, agent_id=uid, on_delete_callback=self.delete_agent)
        self.controls.append(agent)

    async def delete_agent(self, agent_item):
        try:
            if agent_item in self.controls:
                self.controls.remove(agent_item)
                self.update()
        except: pass

class MainPage(ft.Container): 
    def __init__(self):
        super().__init__(padding=10, expand=True)
        
        self.output_list = OutputList() 
        self.agents_list = AgentList()  
        
        panel_bg = ft.Colors.SURFACE 
        border_col = ft.Colors.OUTLINE_VARIANT

        left_panel = ft.Container(
            content=ft.Column([
                ft.Text("SYSTEM LOGS", weight=ft.FontWeight.BOLD, color=ft.Colors.OUTLINE),
                ft.Divider(color=border_col),
                self.output_list
            ]),
            expand=2,
            bgcolor=panel_bg,
            border_radius=10,
            padding=10,
            border=ft.border.all(1, border_col)
        )

        right_panel = ft.Container(
            content=ft.Column([
                ft.Text("ONLINE AGENTS", weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
                ft.Divider(color=ft.Colors.PRIMARY),
                self.agents_list
            ]),
            expand=3,
            bgcolor=panel_bg,
            border_radius=10,
            padding=10,
            border=ft.border.all(1, border_col)
        )

        self.content = ft.Row(
            controls=[left_panel, right_panel],
            expand=True,
            spacing=10
        )


class FletUi(UiAbstract):
    def __init__(self):
        self.page: ft.Page | None = None
        self.content_area = ft.Container(expand=True, padding=10) 

    async def _build_page(self, page: ft.Page):
        self.page = page
        page.title = "Dozorniy RMM"
        self.page.theme = ft.Theme(color_scheme_seed=ft.Colors.ORANGE)
        page.update()
        page.padding = 0 
        
        self.pages = [MainPage(), ft.Text("Settings"), ft.Text("Info")]
        self.content_area.content = self.pages[0]

        def navigate(e):
            idx = e.control.selected_index
            self.content_area.content = self.pages[idx]
            self.content_area.update()

        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD, label="Dashboard"),
                ft.NavigationRailDestination(icon=ft.Icons.SETTINGS, label="Settings"),
                ft.NavigationRailDestination(icon=ft.Icons.INFO, label="Info"),
            ],
            on_change=navigate,
            bgcolor=ft.Colors.SURFACE
        )

        layout = ft.Row([rail, self.content_area], expand=True, spacing=0)
        page.add(layout)

    async def main_loop(self):
       await ft.app_async(target=self._build_page)

if __name__ == "__main__":
    flet_app = FletUi()
    asyncio.run(flet_app.main_loop())
