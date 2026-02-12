from collections import deque
import flet as ft
from core.events import EventBus, OutputConnection 

class ListLog(ft.Container): 
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
        #TODO: добавить в settings
        self.max_log_lines = 100
        self.max_log_ui_lines = 20
        self._log_history = deque(maxlen=self.max_log_lines)

    def did_mount(self):
        self.bus.subscribe(OutputConnection, self.output_log_event)
    
    #TODO: сделать unsubscribe
    # def will_unmount(self):
    #     self.bus.unsubscribe(OutputConnection, self.output_log_event)
    
    async def output_log_event(self, event: OutputConnection):
        self._log_history.append(event.text)
        
        item = ft.ListTile(
            title=ft.Text(event.text),
            trailing=ft.Icons.INFO,
        )
        
        self.list_view.controls.append(item)

        if len(self.list_view.controls) > self.max_log_ui_lines:
            self.list_view.controls.pop(0)

        self.update() 
