from abc import ABC
from typing import Type, ClassVar
from pydantic import BaseModel
from core.config.models import BaseSettings, NetworkSettings

class ConfigRecieveData(BaseModel, ABC):
    pass

class NetworkConfigRecieveData(ConfigRecieveData):
    payload: NetworkSettings

class GetConfig(BaseModel, ABC):
    response_class: ClassVar[Type[ConfigRecieveData]]
    model_class: ClassVar[Type[BaseSettings]]

class NetworkGetConfig(GetConfig):
    response_class = NetworkConfigRecieveData
    model_class = NetworkSettings

class LoadConfigData(BaseModel,ABC):
    pass

class NetworkLoadConfigData(LoadConfigData):
    payload: NetworkSettings

class UpdateConfig(BaseModel, ABC):
    response_class: ClassVar[Type[LoadConfigData]]
    model_class: ClassVar[Type[BaseSettings]]

class NetworkUpdateConfig(UpdateConfig):
    response_class = NetworkLoadConfigData
    model_class = NetworkSettings


