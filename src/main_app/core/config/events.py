from abc import ABC
from typing import Type, ClassVar
from pydantic import BaseModel
from core.config.models import BaseSettings, NetworkSettings

class ConfigLoaded(BaseModel, ABC):
    pass

class NetworkConfigLoaded(ConfigLoaded):
    payload: NetworkSettings


class GetConfig(BaseModel, ABC):
    response_class: ClassVar[Type[ConfigLoaded]]
    model_class: ClassVar[Type[BaseSettings]]

class NetworkGetConfig(GetConfig):
    response_class = NetworkConfigLoaded
    model_class = NetworkSettings
