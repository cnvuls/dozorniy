from uuid import UUID

from pydantic import BaseModel


class RequestBase(BaseModel):
    """
    [CLIENT->SERVER]
    """

    type: str
    event_id: UUID
