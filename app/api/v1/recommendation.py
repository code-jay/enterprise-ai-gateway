"""Model recommendation endpoints."""

from fastapi import APIRouter, HTTPException

from app.core.recommendation.recommendation_engine import (
    NoEligibleModelError,
)
from app.core.recommendation.recommendation_service import (
    recommendation_service,
)
from app.domain.contracts.recommendation_request import (
    RecommendationRequest,
)
from app.domain.contracts.recommendation_response import (
    RecommendationResponse,
)


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.post(
    "",
    response_model=RecommendationResponse,
)
async def recommend_model(
    request: RecommendationRequest,
) -> RecommendationResponse:
    try:
        return recommendation_service.recommend(request)

    except NoEligibleModelError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc