"""Provider-independent request contract."""

from pydantic import Field

from app.domain.contracts.base_request import BaseRequest


class ProviderRequest(BaseRequest):
    """Request sent internally to an LLM provider."""

    model: str = Field(
        ...,
        min_length=1,
        description="Provider-specific model identifier.",
    )

    prompt: str = Field(
        ...,
        min_length=1,
        max_length=100_000,
    )

    system_prompt: str | None = None

    temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
    )

    max_tokens: int = Field(
        default=1024,
        ge=1,
        le=100_000,
    )

    stream: bool = False

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )