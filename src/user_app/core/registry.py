from typing import Any, TypeVar

from core.responses.base import ResponseBase, ResponseHandler

H = TypeVar("H", bound=ResponseHandler)


class FeatureRegistry:
    _registry: dict[str, tuple[type[ResponseBase], type[ResponseHandler]]] = {}

    @classmethod
    def register(cls, command_key: str, command_model: type[ResponseBase]):
        def decorator(handler_cls: type[H]) -> type[H]:
            cls._registry[command_key] = (command_model, handler_cls)
            return handler_cls

        return decorator

    @classmethod
    def get_features(
        cls,
    ) -> dict[str, tuple[type[ResponseBase], type[ResponseHandler]]]:
        return cls._registry
