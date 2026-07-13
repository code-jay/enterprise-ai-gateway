"""Base interface for recommendation scorers."""

from abc import ABC, abstractmethod

from app.domain.contracts.recommendation_request import (
    RecommendationRequest,
)
from app.domain.models.model_info import ModelInfo
from app.domain.models.score_result import ScoreResult


class BaseScorer(ABC):
    """Common contract implemented by every scorer."""

    name: str

    @abstractmethod
    def score(
        self,
        model: ModelInfo,
        request: RecommendationRequest,
    ) -> ScoreResult:
        """Score a model from zero to ten."""