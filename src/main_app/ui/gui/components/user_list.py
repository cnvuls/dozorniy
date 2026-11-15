import asyncio
import base64
from ctypes import cast
from webbrowser import get

import flet as ft

from core.events import AbstractEvent, EventBus, UpdateUserEvent
from core.events.network import FrameData, PullUserList, PushUserList
from core.events.other import TelemetryUpdateEvent
from ui.gui.components.user_item import UserItem


class SortUsers(AbstractEvent):
    enable: bool


class ListUsers(ft.ListView):
    _sorted: bool = False

    def __init__(self, bus: EventBus):
        super().__init__(expand=True, spacing=10, padding=10)
        self.bus = bus
        self.controls: list[UserItem]  # type: ignore[assignment]
        self.cards: dict[int, UserItem] = {}

    async def sort(self, event: SortUsers):
        ListUsers._sorted = event.enable
        if event.enable:
            self.controls.sort(key=lambda card: card.name.lower())

        self.update()

    async def screenupdate(self, event: FrameData):
        if self.cards.get(event.user_id):
            self.cards[event.user_id].update_image(event.base64_img)

    def did_mount(self):
        self.bus.subscribe(UpdateUserEvent, self.update_user)
        self.bus.subscribe(FrameData, self.screenupdate)
        self.bus.subscribe(PushUserList, self.update_userlist)
        self.bus.subscribe(SortUsers, self.sort)

        asyncio.create_task(self.bus.publish(PullUserList()))
        self.update()

    def will_unmount(self):
        self.bus.unsubscribe(UpdateUserEvent, self.update_user)
        self.bus.unsubscribe(FrameData, self.screenupdate)
        self.bus.unsubscribe(PushUserList, self.update_userlist)
        self.bus.unsubscribe(SortUsers, self.sort)

    async def update_userlist(self, event: PushUserList):

        self.controls.clear()
        self.cards.clear()

        for id, name in event.users:
            new_card = UserItem(id, name, self.bus)
            self.cards[id] = new_card
            self.controls.append(new_card)

        self.update()

    async def update_user(self, event: UpdateUserEvent):
        if event.action == "disconnect":
            card = self.cards.pop(event.user_id, None)
            if card and card in self.controls:
                self.controls.remove(card)
        elif event.action == "connect":
            if event.user_id not in self.cards:
                new_card = UserItem(event.user_id, event.user_name, bus=self.bus)
                self.cards[event.user_id] = new_card
                self.controls.append(new_card)

        if self._sorted:
            self.controls.sort(key=lambda card: card.name.lower())

        self.update()
