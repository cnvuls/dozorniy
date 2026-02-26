import json
from pathlib import Path

import aiofiles.os
from core.config.events import  ConfigLoaded, GetConfig, UpdateConfig
from core.events import EventBus
import aiofiles 

class ConfigLoader:
    def __init__(self, bus: EventBus) -> None:
        self._bus: EventBus = bus
        self.CONFIG_PATH = Path("default.json") 
        
    async def handle_get_config(self, event: GetConfig):
        model_cls = event.model_class
        
        section = model_cls.section_name
        
        raw_data = await self._read_json()
        section_data = raw_data.get(section, {})
        
        model_instance = model_cls.model_validate(section_data)
        response_event = ConfigLoaded(payload=model_instance)

        await self._bus.publish(response_event)
    
    async def handle_update_config(self, event: UpdateConfig):
        """
        Класс в котором отправляются изменения в файлики
        """
        current_config = await self._read_json()
        section = event.payload.section_name
        current_config[section] = event.payload.model_dump()
        
        await self._write_json(current_config) 
        await self._bus.publish(ConfigLoaded(payload=event.payload))

    async def _read_json(self) -> dict:
        try:
            async with aiofiles.open(self.CONFIG_PATH, "r") as r:
                contents = await r.read()
            return json.loads(contents)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    async def _write_json(self,data:dict) -> None:
        temp_path = self.CONFIG_PATH.with_suffix(".bak")

        try:
            async with aiofiles.open(temp_path, "w") as f:
               await f.write(json.dumps(data, indent=4, ensure_ascii=True))

            await aiofiles.os.rename(temp_path, self.CONFIG_PATH)
        except Exception as e:
            if temp_path.exists():
                import os
                os.remove(temp_path)

            raise e
