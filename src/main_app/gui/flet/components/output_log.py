import flet as ft
from core.events import EventBus, OutputConnection 

class OutputLog(ft.Container): 
    def __init__(self, bus: EventBus):
        super().__init__()
        self.bus = bus
        self.expand = True
        
        self.border = ft.border.all(1, ft.Colors.PRIMARY)
        self.border_radius = 5
        self.padding = 5

        self.list_view = ft.ListView(
            expand=True,
            spacing=2,
            auto_scroll=True,
        )
        
        self.content = self.list_view 

    def did_mount(self):
        self.bus.subscribe(OutputConnection, self.handle_output_event)

    async def handle_output_event(self, event: OutputConnection):
        line = ft.Text(
            f"> {event.text}", 
            color=ft.Colors.PRIMARY,
            selectable=True,
            font_family="Consolas"
        )
        
        self.list_view.controls.append(line)
        self.update() 
