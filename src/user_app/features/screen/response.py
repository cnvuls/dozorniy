from enum import Enum

from core.responses.base import ResponseBase


class FrameTimeOption(Enum):
    FAST = 0.5
    SLOW = 30


class ScreenResponse(ResponseBase):
    window_fullscreen: bool = True
    frame_time: FrameTimeOption = FrameTimeOption.SLOW
