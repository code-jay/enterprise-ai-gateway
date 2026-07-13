"""Score models by budget and cost efficiency."""

from app.core.recommendation.scorers.base_scorer import BaseScorer
from app.domain.contracts.recommendation_request import (
    RecommendationRequest,
)
from app.domain.enums.cost_tier import CostTier
from app.domain.models.model_info import ModelInfo
from app.domain.models.score_result import ScoreResult


class CostScorer(BaseScorer):
    """Scores model affordability against the requested budget."""

    name = "cost"

    _LOW_BUDGET_SCORES = {
        CostTier.LOW: 10.0,
        CostTier.MEDIUM: 6.0,
        CostTier.HIGH: 2.0,
    }

    _MEDIUM_BUDGET_SCORES = {
        CostTier.LOW: 9.0,
        CostTier.MEDIUM: 8.0,
        CostTier.HIGH: 5.0,
    }

    _HIGH_BUDGET_SCORES = {
        CostTier.LOW: 8.0,
        CostTier.MEDIUM: 9.0,
        CostTier.HIGH: 10.0,
    }

    def score(
        self,
        model: ModelInfo,
        request: RecommendationRequest,
    ) -> ScoreResult:
        if request.budget == "low":
            tier_score = self._LOW_BUDGET_SCORES[model.cost_tier]

        elif request.budget == "high":
            tier_score = self._HIGH_BUDGET_SCORES[model.cost_tier]

        else:
            tier_score = self._MEDIUM_BUDGET_SCORES[model.cost_tier]

        # Combine the catalog's cost efficiency with budget matching.
        score = (
            tier_score * 0.60
            + model.cost_score * 0.40
        )

        return ScoreResult(
            score=round(score, 2),
            reason=(
                f"Model cost tier '{model.cost_tier.value}' "
                f"was evaluated against a '{request.budget}' budget."
            ),
        )