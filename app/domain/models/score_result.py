"""Result returned by an individual model scorer."""

from pydantic import BaseModel, Field


class ScoreResult(BaseModel):
    """One score component and its explanation."""

    score: float = Field(
        ...,
        ge=0.0,
        le=10.0,
    )

    reason: str

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )