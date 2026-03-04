# Copyright (c) 2026 hackhype. SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

from dataclasses import dataclass
from typing import Any, List, Optional, Tuple, Type

from pydantic import BaseModel

@dataclass
class FeatureMeta:
    command_key: str 
    response_model: Type[Any]
    request_model: Type[Any]
    handler_cls: Type[Any]  
    name: str
    version: str
    args_model: Optional[Type[BaseModel]] = None
    is_hidden: bool = False




class FeatureRegistry:
    _features: List[FeatureMeta] = []

    @classmethod
    def register(
            cls, 
            command_key: str, 
            response_model: Type[Any],
            request_model: Type[Any],
            name: str,
            version: str,
            args_model: Optional[Type[BaseModel]] = None,
            is_hidden: bool = False
        ):
        """
        Декоратор для регистрации хендлеров.
        Связывает: строку JSON -> Pydantic модель -> Класс Хендлера
        """

        def decorator(handler_cls): 
            meta = FeatureMeta(
                command_key=command_key,
                response_model=response_model,
                request_model=request_model,
                handler_cls=handler_cls,
                name=name,
                version=version,
                args_model=args_model,
                is_hidden=is_hidden
            )
            
            cls._features.append(meta)
            
            return handler_cls

        return decorator

    @classmethod
    def get_features(cls) -> List[FeatureMeta]:
        return cls._features
