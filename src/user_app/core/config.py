import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    AGENT_NAME: str = "agent"
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8888
    TELEMETRY_INTERVAL: int = 1
    SCREEN_INTERVAL: int = 10
    RECONNECT_DELAY: float = 3.0
    VERSION: str = "0.0.0"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


config = Config()
