"""Orchestrates filtering and model ranking."""

from app.core.recommendation.model_catalog import ModelCatalog
from app.core.recommendation.rule_engine import RuleEngine
from app.core.recommendation.scoring_engine import ScoringEngine
from app.domain.contracts.recommendation_request import (
    RecommendationRequest,
)
from app.domain.models.model_score import ModelScore


class NoEligibleModelError(Exception):
    """Raised when no model satisfies the request."""


class RecommendationResult:
    """Internal recommendation result."""

    def __init__(
        self,
        ranked_models: list[ModelScore],
        rejected_models: dict[str, list[str]],
    ) -> None:
        self.ranked_models = ranked_models
        self.rejected_models = rejected_models

    @property
    def recommended(self) -> ModelScore:
        return self.ranked_models[0]


class RecommendationEngine:
    """Filters and ranks models from the model catalog."""

    def __init__(
        self,
        catalog: ModelCatalog,
        rule_engine: RuleEngine | None = None,
        scoring_engine: ScoringEngine | None = None,
    ) -> None:
        self._catalog = catalog
        self._rule_engine = rule_engine or RuleEngine()
        self._scoring_engine = (
            scoring_engine or ScoringEngine()
        )

    def recommend(
        self,
        request: RecommendationRequest,
    ) -> RecommendationResult:
        models = self._catalog.list_all(
            include_disabled=True,
        )

        eligible, rejected = self._rule_engine.evaluate(
            models,
            request,
        )

        if not eligible:
            raise NoEligibleModelError(
                "No eligible model satisfies the workload requirements."
            )

        ranked = self._scoring_engine.rank_models(
            eligible,
            request,
        )

        return RecommendationResult(
            ranked_models=ranked,
            rejected_models=rejected,
        )