from abc import ABC
from pydantic import BaseModel
from core.config.events import ConfigLoaded, GetConfig
from core.events import EventBus


class ConfigLoader:
    def __init__(self, bus: EventBus) -> None:
        self._bus: EventBus = bus
        
    async def handle_get_config(self, event: GetConfig):
        # 1. Берем классы прямо из пришедшего события
        model_cls = event.model_class
        resp_cls = event.response_class
        
        section = model_cls.section_name
        
        raw_data = self._read_json()
        section_data = raw_data.get(section, {})
        
        model_instance = model_cls.model_validate(section_data)
        response_event = resp_cls.model_validate({"payload": model_instance})
        
        await self._bus.publish(response_event)
    
    #TODO: сделать не заглушку
    def _read_json(self):
        return {}

