from ast import literal_eval
from enum import Enum
from typing import Literal

from core.requests.base import RequestBase


class FrameTimeOption(Enum):
    FAST = 0.5
    SLOW = 30


class ScreenRequest(RequestBase):
    window: tuple[int, int] = (120, 80)
    frame_time: FrameTimeOption = FrameTimeOption.SLOW
