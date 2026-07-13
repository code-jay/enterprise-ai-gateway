from pydantic import Field, field_validator

from app.domain.contracts.base_request import BaseRequest
from app.domain.enums.privacy_level import PrivacyLevel
from app.domain.enums.provider_type import ProviderType
from app.domain.enums.response_speed import ResponseSpeed
from app.domain.enums.task_type import TaskType


class GatewayRequest(BaseRequest):
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=100_000,
    )

    task: TaskType = TaskType.GENERAL
    provider: ProviderType | None = None
    privacy: PrivacyLevel = PrivacyLevel.PUBLIC
    response_speed: ResponseSpeed = ResponseSpeed.BALANCED

    max_tokens: int = Field(default=1024, ge=1, le=100_000)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    stream: bool = False

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Prompt must not be empty.")

        return cleaned