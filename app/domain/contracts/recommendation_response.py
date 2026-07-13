"""Unified response returned by the Enterprise AI Gateway."""

from pydantic import Field, model_validator

from app.domain.contracts.base_response import BaseResponse
from app.domain.enums.finish_reason import FinishReason
from app.domain.enums.provider_type import ProviderType


class GatewayResponse(BaseResponse):
    provider: ProviderType

    model: str = Field(..., min_length=1)

    content: str

    finish_reason: FinishReason = FinishReason.STOP

    latency_ms: float = Field(default=0.0, ge=0.0)

    input_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)

    estimated_cost: float = Field(default=0.0, ge=0.0)

    recommendation_score: float | None = Field(
        default=None,
        ge=0.0,
        le=100.0,
    )

    routing_reason: list[str] = Field(default_factory=list)

    request_id: str | None = None
    raw_response_id: str | None = None

    metadata: dict[str, object] = Field(default_factory=dict)

    @model_validator(mode="after")
    def calculate_total_tokens(self) -> "GatewayResponse":
        if self.total_tokens == 0:
            self.total_tokens = (
                self.input_tokens + self.output_tokens
            )

        return self