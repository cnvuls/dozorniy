from core.requests.base import RequestBase  # INFO: Смена импорта на Request


class PingRequest(RequestBase):
    """
    [SERVER -> CLIENT]
    Исходящий ответ сервера (Pong).
    Для Агента это является входящей командой (Request).
    """

    type: str = "ping"

    message: str = "pong"

    # INFO: Поле reply_to (ID исходного пинга) уже есть в RequestBase?
    # Если нет, лучше добавить его здесь или в базе.
