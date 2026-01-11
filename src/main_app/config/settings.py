from typing import Literal

from pydantic import BaseModel, field_validator


class Config(BaseModel):
    port: int = 8888
    gui_type: Literal["cli"] = "cli"
    connection_mode: Literal["ws"] = "ws"
    log_level: str = "INFO"
    gui_state_depth: int = 50
    video_enabled: bool = True
    video_host: str = "192.168.0.109"
    video_port: int = 9999

    @field_validator("port", "video_port")
    @classmethod
    def force_port_positive(cls, port: int) -> int:
        assert 1024 <= port <= 65535
        return port

    @field_validator("gui_state_depth")
    @classmethod
    def validate_gui_depth(cls, value: int) -> int:
        return max(10, min(500, value))
