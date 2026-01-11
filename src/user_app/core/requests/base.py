# Copyright (c) 2026 hackhype. SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

from uuid import UUID

from pydantic import BaseModel


class RequestBase(BaseModel):
    """
    [CLIENT->SERVER]
    """

    type: str
    event_id: UUID
