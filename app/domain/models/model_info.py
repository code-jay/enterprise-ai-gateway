"""Domain model describing an LLM available to the gateway."""

from pydantic import BaseModel, Field, model_validator

from app.domain.enums.cost_tier import CostTier
from app.domain.enums.model_capability import ModelCapability
from app.domain.enums.model_status import ModelStatus
from app.domain.enums.privacy_level import PrivacyLevel
from app.domain.enums.provider_type import ProviderType
from app.domain.enums.task_type import TaskType


class ModelInfo(BaseModel):
    """Provider-independent metadata for one model."""

    model_id: str = Field(
        ...,
        min_length=1,
        description="Model identifier understood by the provider.",
    )

    display_name: str = Field(
        ...,
        min_length=1,
    )

    provider: ProviderType

    description: str | None = None

    supported_tasks: set[TaskType] = Field(
        default_factory=set,
    )

    capabilities: set[ModelCapability] = Field(
        default_factory=set,
    )

    max_context_tokens: int = Field(
        ...,
        gt=0,
    )

    max_output_tokens: int = Field(
        ...,
        gt=0,
    )

    quality_score: float = Field(
        default=5.0,
        ge=0.0,
        le=10.0,
    )

    speed_score: float = Field(
        default=5.0,
        ge=0.0,
        le=10.0,
    )

    cost_score: float = Field(
        default=5.0,
        ge=0.0,
        le=10.0,
        description=(
            "Higher score means more cost-efficient."
        ),
    )

    cost_tier: CostTier = CostTier.MEDIUM

    supported_privacy_levels: set[PrivacyLevel] = Field(
        default_factory=lambda: {
            PrivacyLevel.PUBLIC,
            PrivacyLevel.INTERNAL,
        }
    )

    status: ModelStatus = ModelStatus.ACTIVE

    enabled: bool = True

    supports_streaming: bool = True
    supports_tools: bool = False
    supports_structured_output: bool = False
    supports_vision: bool = False

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )

    @model_validator(mode="after")
    def validate_token_limits(self) -> "ModelInfo":
        if self.max_output_tokens > self.max_context_tokens:
            raise ValueError(
                "max_output_tokens cannot exceed max_context_tokens."
            )

        return self

    @property
    def key(self) -> str:
        """Return a stable catalog key."""

        return f"{self.provider.value}:{self.model_id}"

    def supports_task(self, task: TaskType) -> bool:
        """Return whether this model supports the requested task."""

        return (
            task in self.supported_tasks
            or TaskType.GENERAL in self.supported_tasks
        )

    def supports_privacy(
        self,
        privacy: PrivacyLevel,
    ) -> bool:
        """Return whether the model is approved for a privacy level."""

        return privacy in self.supported_privacy_levels

    def is_available(self) -> bool:
        """Return whether the model can currently be selected."""

        return (
            self.enabled
            and self.status == ModelStatus.ACTIVE
        )