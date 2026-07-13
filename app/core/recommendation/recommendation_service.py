"""Application service for model recommendations."""

from app.core.recommendation.model_catalog import model_catalog
from app.core.recommendation.recommendation_engine import (
    RecommendationEngine,
)
from app.domain.contracts.recommendation_request import (
    RecommendationRequest,
)
from app.domain.contracts.recommendation_response import (
    RecommendationResponse,
)


class RecommendationService:
    """Maps internal ranking results to API contracts."""

    def __init__(
        self,
        engine: RecommendationEngine,
    ) -> None:
        self._engine = engine

    def recommend(
        self,
        request: RecommendationRequest,
    ) -> RecommendationResponse:
        result = self._engine.recommend(request)

        winner = result.recommended

        alternative_scores = result.ranked_models[
            1 : 1 + request.alternatives_limit
        ]

        alternatives = [
            (
                f"{item.model.provider.value}:"
                f"{item.model.model_id}"
                f" ({item.total_score:.2f})"
            )
            for item in alternative_scores
        ]

        return RecommendationResponse(
            request_id=request.request_id,
            provider=winner.model.provider,
            model=winner.model.model_id,
            score=winner.total_score,
            reason=winner.reasons,
            score_breakdown=winner.breakdown,
            alternatives=alternatives,
            eligible_model_count=len(result.ranked_models),
            rejected_models=result.rejected_models,
            message="Model recommendation completed.",
        )


recommendation_service = RecommendationService(
    RecommendationEngine(model_catalog)
)