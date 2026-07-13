"""Provider-independent response contract."""

from pydantic import Field

from app.domain.contracts.base_response import BaseResponse
from app.domain.enums.finish_reason import FinishReason
from app.domain.enums.provider_type import ProviderType


class ProviderResponse(BaseResponse):
    """Normalized response returned by every provider adapter."""

    provider: ProviderType

    model: str

    content: str

    finish_reason: FinishReason = FinishReason.STOP

    latency_ms: float = Field(
        default=0.0,
        ge=0.0,
    )

    input_tokens: int = Field(
        default=0,
        ge=0,
    )

    output_tokens: int = Field(
        default=0,
        ge=0,
    )

    total_tokens: int = Field(
        default=0,
        ge=0,
    )

    raw_response_id: str | None = None

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )