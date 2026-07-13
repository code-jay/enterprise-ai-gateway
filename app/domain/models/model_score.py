"""Aggregated recommendation score for one model."""

from pydantic import BaseModel, Field

from app.domain.models.model_info import ModelInfo


class ModelScore(BaseModel):
    """Final score and scoring details for one model."""

    model: ModelInfo

    total_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
    )

    breakdown: dict[str, float] = Field(
        default_factory=dict,
    )

    raw_scores: dict[str, float] = Field(
        default_factory=dict,
    )

    reasons: list[str] = Field(
        default_factory=list,
    )