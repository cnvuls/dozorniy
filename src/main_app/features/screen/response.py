from pydantic import Base64Bytes

from core.responses.base import ResponseBase


class ScreenResponse(ResponseBase):
    img_base64: Base64Bytes
