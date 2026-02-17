from pydantic import Field
import time
from typing import Optional
from core.events.base import AbstractEvent

class BaseLogEvent(AbstractEvent):
    text:str
    source:str
    timestamp:float = Field(default_factory=time.time)


class InfoLogEvent(BaseLogEvent):
    pass

class ErrorLogEvent(BaseLogEvent):
    details: Optional[str] = None

class ConsoleLogEvent(BaseLogEvent):
    pass
