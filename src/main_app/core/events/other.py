
from core.events import AbstractEvent
from core.registry import FeatureMeta


class RequestFeatureList(AbstractEvent):
    """Запрос списка для получение доступных комманд"""
    pass

class ResponseFeatureList(AbstractEvent):
    """Ответ со списком метаданных функий"""
    content: list[FeatureMeta] 
