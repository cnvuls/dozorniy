# Copyright (c) 2026 hackhype. SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

from dataclasses import dataclass
from typing import Any, List, Optional, Tuple, Type

from pydantic import BaseModel


class BaseFeatureArgs(BaseModel):
    """Все фичи будут наследовать свои аргументы отсюда"""
    pass

@dataclass
class FeatureMeta:
    command_key: str 
    response_model: Type[Any] 
    handler_cls: Type[Any]  
    name: str
    version: str
    args_model: Optional[Type[BaseModel]] = None

class FeatureRegistry:
    _features: List[FeatureMeta] = []

    @classmethod
    def register(
            cls, 
            command_key: str, 
            response_model: Type[Any],       
            name: str,
            version: str,
            args_model: Optional[Type[BaseModel]] = None
        ):
        """
        Декоратор для регистрации хендлеров.
        Связывает: строку JSON -> Pydantic модель -> Класс Хендлера
        """

        def decorator(handler_cls): 
            meta = FeatureMeta(
                command_key=command_key,
                response_model=response_model,
                handler_cls=handler_cls,
                name=name,
                version=version,
                args_model=args_model
            )
            
            cls._features.append(meta)
            
            return handler_cls

        return decorator

    @classmethod
    def get_features(cls) -> List[FeatureMeta]:
        return cls._features
