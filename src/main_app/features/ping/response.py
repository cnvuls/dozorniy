from main_app.core.responses.base import \
    ResponseBase  # INFO: Смена импорта на Response


class PingResponse(ResponseBase):
    """
    [CLIENT -> SERVER]
    Входящий сигнал от агента.
    user_id и request_id наследуются от ResponseBase.
    """

    # INFO: Если хочешь передавать дополнительные данные (версию агента и т.д.)
    # agent_version: str | None = None
    pass
