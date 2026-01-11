from dataclasses import dataclass
from typing import Any, List, Tuple, Type


@dataclass
class FeatureMeta:
    command_key: str  # Например: "shell_result"
    response_model: Type[Any]  # Например: ShellResponse
    handler_cls: Type[Any]  # Например: ShellHandler (сам класс, не инстанс)


class FeatureRegistry:
    _features: List[FeatureMeta] = []

    @classmethod
    def register(cls, command_key: str, response_model: Type[Any]):
        """
        Декоратор для регистрации хендлеров.
        Связывает: строку JSON -> Pydantic модель -> Класс Хендлера
        """

        def decorator(handler_cls):
            cls._features.append(
                FeatureMeta(
                    command_key=command_key,
                    response_model=response_model,
                    handler_cls=handler_cls,
                )
            )
            return handler_cls

        return decorator

    @classmethod
    def get_features(cls) -> List[FeatureMeta]:
        return cls._features
