"""Score models by privacy suitability."""

from app.core.recommendation.scorers.base_scorer import BaseScorer
from app.domain.contracts.recommendation_request import (
    RecommendationRequest,
)
from app.domain.enums.privacy_level import PrivacyLevel
from app.domain.enums.provider_type import ProviderType
from app.domain.models.model_info import ModelInfo
from app.domain.models.score_result import ScoreResult


class PrivacyScorer(BaseScorer):
    """Scores privacy compatibility and deployment suitability."""

    name = "privacy"

    def score(
        self,
        model: ModelInfo,
        request: RecommendationRequest,
    ) -> ScoreResult:
        if not model.supports_privacy(request.privacy):
            return ScoreResult(
                score=0.0,
                reason="Model is not approved for this privacy level.",
            )

        private_providers = {
            ProviderType.OLLAMA,
            ProviderType.CUSTOM,
        }

        if request.privacy in {
            PrivacyLevel.CONFIDENTIAL,
            PrivacyLevel.RESTRICTED,
        }:
            if model.provider in private_providers:
                return ScoreResult(
                    score=10.0,
                    reason=(
                        "Private/self-hosted provider is suitable "
                        "for sensitive data."
                    ),
                )

            return ScoreResult(
                score=7.0,
                reason=(
                    "Model is approved, but it is not a "
                    "private/self-hosted provider."
                ),
            )

        return ScoreResult(
            score=9.0,
            reason=(
                f"Model supports the '{request.privacy.value}' "
                "privacy classification."
            ),
        )