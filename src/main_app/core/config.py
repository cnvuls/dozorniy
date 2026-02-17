from abc import ABC
from pydantic import BaseModel
from core.events import EventBus

# Requests
class BaseConfigRequest(ABC, BaseModel):
    section: str

class NetworkConfigRequest(BaseConfigRequest):
    section: str = "network"

class NetworkSettings(BaseModel):
    port:int = 8888

class ConfigLoader:
    def __init__(self, bus: EventBus) -> None:
        self._bus: EventBus = bus
        self._bus.subscribe(BaseConfigRequest, self.handle_request)

        self._models = {
            "network":NetworkSettings 
        }

    #TODO: Прикрутить json сюда
    async def handle_request(self, event: BaseConfigRequest):
        section = event.section

        if section not in self._models:
            print("Неизвестная секция")

        model_cls = self._models[section]
        
        await self._bus.publish(model_cls)
