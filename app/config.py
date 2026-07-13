from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "Enterprise AI Gateway"
    app_version: str = "0.1.0"

    app_env: Literal[
        "development",
        "testing",
        "staging",
        "production",
    ] = "development"

    debug: bool = False

    api_prefix: str = Field(default="/api")
    api_version: str = Field(default="v1")

    default_provider: str = "openai"
    default_model: str = "gpt-4o-mini"

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def api_base_url(self) -> str:
        return (
            f"{self.api_prefix.rstrip('/')}/"
            f"{self.api_version.strip('/')}"
        )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()