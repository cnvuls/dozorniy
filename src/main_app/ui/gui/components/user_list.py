import base64
from webbrowser import get

import flet as ft

from core.events import EventBus, UpdateUserEvent
from core.events.network import FrameData
from core.events.other import TelemetryUpdateEvent
from ui.gui.components.user_item import UserItem


class ListUsers(ft.ListView):
    _global_user_dict: dict[int, UserItem] = {}

    def __init__(self, bus: EventBus):
        super().__init__(expand=True, spacing=10, padding=10)
        self.bus = bus

    async def screenupdate(self, event: FrameData):
        if not self.page:
            return
        card = self._global_user_dict.get(event.user_id)
        if card and card in self.controls:
            card.update_image(event.base64_img)

    def did_mount(self):
        self.bus.subscribe(UpdateUserEvent, self.update_user)
        self.bus.subscribe(FrameData, self.screenupdate)
        for i in self._global_user_dict:
            if self._global_user_dict[i] not in self.controls:
                self.controls.append(self._global_user_dict[i])

        self.update()

    def will_unmount(self):
        self.bus.unsubscribe(UpdateUserEvent, self.update_user)
        self.bus.unsubscribe(FrameData, self.screenupdate)

    async def update_user(self, event: UpdateUserEvent):
        if event.action == "disconnect":
            card = self._global_user_dict.pop(event.user_id, None)
            if card and card in self.controls:
                self.controls.remove(card)
        elif event.action == "connect":
            if event.user_id not in self._global_user_dict:
                new_card = UserItem(event.user_id, event.user_name, bus=self.bus)
                self._global_user_dict[event.user_id] = new_card
                self.controls.append(new_card)

        if self.page:
            self.update()
