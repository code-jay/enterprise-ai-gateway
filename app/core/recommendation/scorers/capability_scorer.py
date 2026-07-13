"""Score models by required AI capabilities."""

from app.core.recommendation.scorers.base_scorer import BaseScorer
from app.domain.contracts.recommendation_request import (
    RecommendationRequest,
)
from app.domain.enums.model_capability import ModelCapability
from app.domain.enums.task_type import TaskType
from app.domain.models.model_info import ModelInfo
from app.domain.models.score_result import ScoreResult


class CapabilityScorer(BaseScorer):
    """Scores required model features."""

    name = "capability"

    def score(
        self,
        model: ModelInfo,
        request: RecommendationRequest,
    ) -> ScoreResult:
        required: set[ModelCapability] = set()

        if request.requires_vision or request.task == TaskType.VISION:
            required.add(ModelCapability.VISION)

        if request.requires_tools or request.task == TaskType.AGENT:
            required.add(ModelCapability.FUNCTION_CALLING)

        if request.requires_structured_output:
            required.add(ModelCapability.STRUCTURED_OUTPUT)

        if request.task in {
            TaskType.CODE_GENERATION,
            TaskType.CODE_REVIEW,
        }:
            required.add(ModelCapability.CODING)

        if request.task == TaskType.REASONING:
            required.add(ModelCapability.REASONING)

        if not required:
            return ScoreResult(
                score=8.0,
                reason="No specialized capabilities are required.",
            )

        supported = required.intersection(model.capabilities)
        missing = required.difference(model.capabilities)

        if missing:
            return ScoreResult(
                score=0.0,
                reason=(
                    "Missing required capabilities: "
                    + ", ".join(sorted(item.value for item in missing))
                ),
            )

        return ScoreResult(
            score=10.0,
            reason=(
                "Supports all required capabilities: "
                + ", ".join(
                    sorted(item.value for item in supported)
                )
            ),
        )