"""Weighted model scoring engine."""

from app.core.recommendation.scorers.base_scorer import BaseScorer
from app.core.recommendation.scorers.capability_scorer import (
    CapabilityScorer,
)
from app.core.recommendation.scorers.context_scorer import (
    ContextScorer,
)
from app.core.recommendation.scorers.cost_scorer import CostScorer
from app.core.recommendation.scorers.privacy_scorer import (
    PrivacyScorer,
)
from app.core.recommendation.scorers.quality_scorer import (
    QualityScorer,
)
from app.core.recommendation.scorers.speed_scorer import SpeedScorer
from app.core.recommendation.scorers.task_scorer import TaskScorer
from app.core.recommendation.weights import (
    DEFAULT_WEIGHTS,
    ScoringWeights,
)
from app.domain.contracts.recommendation_request import (
    RecommendationRequest,
)
from app.domain.models.model_info import ModelInfo
from app.domain.models.model_score import ModelScore


class ScoringEngine:
    """Combines individual model scores into a weighted result."""

    def __init__(
        self,
        weights: ScoringWeights = DEFAULT_WEIGHTS,
    ) -> None:
        self._weights = weights.as_dict()

        scorers: list[BaseScorer] = [
            TaskScorer(),
            QualityScorer(),
            SpeedScorer(),
            CostScorer(),
            PrivacyScorer(),
            ContextScorer(),
            CapabilityScorer(),
        ]

        self._scorers = {
            scorer.name: scorer
            for scorer in scorers
        }

    def score_model(
        self,
        model: ModelInfo,
        request: RecommendationRequest,
    ) -> ModelScore:
        raw_scores: dict[str, float] = {}
        breakdown: dict[str, float] = {}
        reasons: list[str] = []

        weighted_total = 0.0

        for name, scorer in self._scorers.items():
            result = scorer.score(model, request)
            weight = self._weights[name]

            # Raw score is 0–10.
            raw_scores[name] = result.score

            # Weighted contribution is represented on a 0–100 scale.
            contribution = result.score * weight * 10

            breakdown[name] = round(contribution, 2)
            weighted_total += contribution

            if result.reason:
                reasons.append(
                    f"{name.title()}: {result.reason}"
                )

        return ModelScore(
            model=model,
            total_score=round(weighted_total, 2),
            breakdown=breakdown,
            raw_scores=raw_scores,
            reasons=reasons,
        )

    def rank_models(
        self,
        models: list[ModelInfo],
        request: RecommendationRequest,
    ) -> list[ModelScore]:
        results = [
            self.score_model(model, request)
            for model in models
        ]

        return sorted(
            results,
            key=lambda item: item.total_score,
            reverse=True,
        )