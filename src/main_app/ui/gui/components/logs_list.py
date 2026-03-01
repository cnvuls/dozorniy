from collections import deque
from datetime import datetime
import flet as ft
from core.events import ConsoleLogEvent, ErrorLogEvent, EventBus, BaseLogEvent, InfoLogEvent

LOG_STYLES = {
    ErrorLogEvent: {
        "color": ft.Colors.ERROR, 
        "icon": ft.Icons.ERROR_OUTLINE
    },
    ConsoleLogEvent: {
        "color": ft.Colors.PRIMARY, 
        "icon": ft.Icons.TERMINAL
    },
    InfoLogEvent: {
        "color": ft.Colors.SECONDARY, 
        "icon": ft.Icons.NOTIFICATIONS_OUTLINED
    },
    BaseLogEvent: {
        "color": ft.Colors.ON_SURFACE, 
        "icon": ft.Icons.INFO_OUTLINE
    },
}

class ListLog(ft.Container): 
    def __init__(self, bus: EventBus):
        super().__init__()
        self.bus = bus
        self.expand = True
        
        self.border = ft.border.all(1, ft.Colors.PRIMARY)
        self.border_radius = 5
        self.padding = 5
        self._mount = False
        self.list_view = ft.ListView(
            expand=True,
            spacing=2,
            auto_scroll=True,
        )
        self.bus.subscribe(BaseLogEvent, self.output_log_event)
        self.content = self.list_view
        # TODO: добавить в settings
        self.max_log_lines = 100
        self.max_log_ui_lines = 20
        self._log_history = deque(maxlen=self.max_log_lines)
    
    def did_mount(self):
        self._mount = True
        self.list_view.controls.clear()
        for event in self._log_history:
            self._add_to_ui(event)

    def will_unmount(self):
        self._mount = False
        self.list_view.controls.clear()
 
    def _add_to_ui(self, event: BaseLogEvent):
        style = LOG_STYLES.get(type(event), LOG_STYLES[BaseLogEvent])
        time_str = datetime.fromtimestamp(event.timestamp).strftime("%H:%M:%S")
        
        item = ft.ListTile(
            leading=ft.Icon(style["icon"], color=style["color"]),
            title=ft.Text(event.text, color=style["color"], size=14),
            subtitle=ft.Text(
                f"[{time_str}] Source: {event.source}", 
                size=12, 
                color=ft.Colors.OUTLINE
            ),
            dense=True,
        )        
        
        self.list_view.controls.append(item)
        


    async def output_log_event(self, event: BaseLogEvent):
        self._log_history.append(event)
        
        self._add_to_ui(event) 
        if len(self.list_view.controls) > self.max_log_ui_lines:
            self.list_view.controls.pop(0)
        
        if self._mount:
            self.update()
