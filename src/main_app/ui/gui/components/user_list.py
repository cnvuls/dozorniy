import base64
from ctypes import cast
from webbrowser import get

import flet as ft

from core.events import AbstractEvent, EventBus, UpdateUserEvent
from core.events.network import FrameData
from core.events.other import TelemetryUpdateEvent
from ui.gui.components.user_item import UserItem


class SortUsers(AbstractEvent):
    enable: bool


class ListUsers(ft.ListView):
    _global_user_dict: dict[int, UserItem] = {}
    _sorted: bool = False

    def __init__(self, bus: EventBus):
        super().__init__(expand=True, spacing=10, padding=10)
        self.bus = bus
        self.controls: list[UserItem]  # type: ignore[assignment]
        self.bus.subscribe(SortUsers, self.sort)

    async def sort(self, event: SortUsers):
        ListUsers._sorted = event.enable
        if event.enable:
            self.controls.sort(key=lambda card: card.name.lower())

        self.update()

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
        print(self._sorted)
        if self._sorted:
            self.controls.sort(key=lambda card: card.name.lower())

        self.update()

    def will_unmount(self):
        #TODO: В следующий раз нужно будет сделать по другому работу updateuserevent
        #self.bus.unsubscribe(UpdateUserEvent, self.update_user)
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

        if self._sorted:
            self.controls.sort(key=lambda card: card.name.lower())

        if self.page:
            self.update()
