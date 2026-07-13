"""Score models by response-speed requirements."""

from app.core.recommendation.scorers.base_scorer import BaseScorer
from app.domain.contracts.recommendation_request import (
    RecommendationRequest,
)
from app.domain.enums.response_speed import ResponseSpeed
from app.domain.models.model_info import ModelInfo
from app.domain.models.score_result import ScoreResult


class SpeedScorer(BaseScorer):
    """Scores speed while considering the user's preference."""

    name = "speed"

    def score(
        self,
        model: ModelInfo,
        request: RecommendationRequest,
    ) -> ScoreResult:
        if request.response_speed == ResponseSpeed.FAST:
            score = model.speed_score
            reason = (
                f"Fast response requested; model speed is "
                f"{model.speed_score:.1f}/10."
            )

        elif request.response_speed == ResponseSpeed.BEST_QUALITY:
            score = (
                model.speed_score * 0.30
                + model.quality_score * 0.70
            )
            reason = (
                "Quality is prioritized over raw response speed."
            )

        else:
            score = (
                model.speed_score * 0.60
                + model.quality_score * 0.40
            )
            reason = (
                "Model provides a balanced quality and speed profile."
            )

        return ScoreResult(
            score=round(score, 2),
            reason=reason,
        )