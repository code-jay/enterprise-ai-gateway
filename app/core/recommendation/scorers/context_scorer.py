"""Score models by context-window suitability."""

from app.core.recommendation.scorers.base_scorer import BaseScorer
from app.domain.contracts.recommendation_request import (
    RecommendationRequest,
)
from app.domain.models.model_info import ModelInfo
from app.domain.models.score_result import ScoreResult


class ContextScorer(BaseScorer):
    """Scores whether a model has enough context capacity."""

    name = "context"

    def score(
        self,
        model: ModelInfo,
        request: RecommendationRequest,
    ) -> ScoreResult:
        if request.context_length > model.max_context_tokens:
            return ScoreResult(
                score=0.0,
                reason="Requested context exceeds the model limit.",
            )

        utilization = (
            request.context_length
            / model.max_context_tokens
        )

        if 0.20 <= utilization <= 0.70:
            score = 10.0
            reason = (
                "Context fits comfortably within the model window."
            )

        elif utilization < 0.20:
            score = 8.0
            reason = (
                "Context fits, but the model window is larger "
                "than required."
            )

        elif utilization <= 0.85:
            score = 8.0
            reason = (
                "Context fits with moderate remaining capacity."
            )

        else:
            score = 6.0
            reason = (
                "Context fits but is close to the maximum limit."
            )

        return ScoreResult(
            score=score,
            reason=reason,
            metadata={
                "context_utilization": round(utilization, 4),
            },
        )