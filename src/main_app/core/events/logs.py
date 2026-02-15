from dataclasses import dataclass, field
import time
from typing import Optional
from core.events.base import AbstractEvent

@dataclass
class BaseLogEvent(AbstractEvent):
    text:str
    source:str
    timestamp:float = field(default_factory=time.time)


@dataclass
class InfoLogEvent(BaseLogEvent):
    pass

@dataclass
class ErrorLogEvent(BaseLogEvent):
    details: Optional[str] = None

@dataclass
class ConsoleLogEvent(BaseLogEvent):
    pass
