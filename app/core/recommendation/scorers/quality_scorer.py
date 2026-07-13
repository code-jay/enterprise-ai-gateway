"""Score models by configured quality."""

from app.core.recommendation.scorers.base_scorer import BaseScorer
from app.domain.contracts.recommendation_request import (
    RecommendationRequest,
)
from app.domain.models.model_info import ModelInfo
from app.domain.models.score_result import ScoreResult


class QualityScorer(BaseScorer):
    """Returns the quality score defined in the catalog."""

    name = "quality"

    def score(
        self,
        model: ModelInfo,
        request: RecommendationRequest,
    ) -> ScoreResult:
        if model.quality_score < request.minimum_quality_score:
            return ScoreResult(
                score=0.0,
                reason=(
                    f"Quality score {model.quality_score:.1f} "
                    "is below the requested minimum."
                ),
            )

        return ScoreResult(
            score=model.quality_score,
            reason=(
                f"Configured quality score is "
                f"{model.quality_score:.1f}/10."
            ),
        )