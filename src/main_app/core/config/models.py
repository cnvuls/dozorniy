from abc import ABC
from typing import ClassVar
from pydantic import BaseModel

class BaseSettings(BaseModel, ABC):
    section_name: ClassVar[str]

class NetworkSettings(BaseSettings):
    section_name: ClassVar[str] = "network"
    port: int = 8888
