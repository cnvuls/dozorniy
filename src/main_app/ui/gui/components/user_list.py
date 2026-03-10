import flet as ft
from core.events import EventBus, UpdateUserEvent
from ui.gui.components.user_item import UserItem


class ListUsers(ft.ListView):
    def __init__(self, bus: EventBus):
        super().__init__(expand=True, spacing=10, padding=10)
        self.bus = bus
        self.bus.subscribe(UpdateUserEvent, self.update_user)

    async def update_user(self, event: UpdateUserEvent):
        if event.action == "disconnect":
            for control in self.controls:
                if getattr(control, "user_id", None) == event.user_id:
                    self.controls.remove(control)
                    break
        elif event.action == "connect":
            self.controls.append(UserItem(event.user_id, event.user_name, bus=self.bus))

        if self.page:
            self.page.update()
