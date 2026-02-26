from abc import ABC
from typing import Type
from core.config.models import BaseSettings
from pydantic import BaseModel


class ConfigLoaded(BaseModel):
    payload: BaseSettings

class GetConfig(BaseModel):
    model_class: Type[BaseSettings]

class UpdateConfig(BaseModel):
    payload: BaseSettings


