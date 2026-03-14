from pydantic import Base64Bytes

from core.requests.base import RequestBase


class ScreenRequest(RequestBase):
    img_base64: Base64Bytes
