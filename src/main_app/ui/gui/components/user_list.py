import base64

import flet as ft

from core.events import EventBus, UpdateUserEvent
from core.events.network import FrameData
from core.events.other import TelemetryUpdateEvent
from ui.gui.components.user_item import UserItem


class ListUsers(ft.ListView):
    def __init__(self, bus: EventBus):
        super().__init__(expand=True, spacing=10, padding=10)
        self.bus = bus
        self.bus.subscribe(UpdateUserEvent, self.update_user)
        self.bus.subscribe(FrameData, self.screenupdate)
        self.user_dict: dict[int, UserItem] = {}

    async def screenupdate(self, event: FrameData):
        if not self.page:
            return
        card = self.user_dict[event.user_id]
        if card in self.controls:
            card.update_image(event.base64_img)

    def stop_screen_updates(self):
        self.bus.unsubscribe(FrameData, self.screenupdate)

    def start_screen_updates(self):
        self.bus.subscribe(FrameData, self.screenupdate)

    async def update_user(self, event: UpdateUserEvent):
        if event.action == "disconnect":
            card = self.user_dict.pop(event.user_id, None)
            if card in self.controls:
                self.controls.remove(card)
        elif event.action == "connect":
            if event.user_id not in self.user_dict:
                new_card = UserItem(event.user_id, event.user_name, bus=self.bus)
                self.user_dict[event.user_id] = new_card
                self.controls.append(new_card)

        if self.page:
            self.page.update()
