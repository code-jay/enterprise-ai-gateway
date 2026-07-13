"""Hard eligibility rules for model recommendations."""

from app.domain.contracts.recommendation_request import (
    RecommendationRequest,
)
from app.domain.enums.model_capability import ModelCapability
from app.domain.models.model_info import ModelInfo


class RuleEngine:
    """Filters models that cannot satisfy workload requirements."""

    def evaluate(
        self,
        models: list[ModelInfo],
        request: RecommendationRequest,
    ) -> tuple[list[ModelInfo], dict[str, list[str]]]:
        eligible: list[ModelInfo] = []
        rejected: dict[str, list[str]] = {}

        for model in models:
            reasons = self._rejection_reasons(
                model,
                request,
            )

            if reasons:
                rejected[model.key] = reasons
            else:
                eligible.append(model)

        return eligible, rejected

    def _rejection_reasons(
        self,
        model: ModelInfo,
        request: RecommendationRequest,
    ) -> list[str]:
        reasons: list[str] = []

        if not model.is_available():
            reasons.append("Model is disabled or unavailable.")

        if request.provider and model.provider != request.provider:
            reasons.append(
                "Model belongs to a different provider."
            )

        if not model.supports_task(request.task):
            reasons.append(
                f"Task '{request.task.value}' is unsupported."
            )

        if request.context_length > model.max_context_tokens:
            reasons.append(
                "Requested context exceeds model capacity."
            )

        if not model.supports_privacy(request.privacy):
            reasons.append(
                f"Privacy level '{request.privacy.value}' "
                "is unsupported."
            )

        if model.quality_score < request.minimum_quality_score:
            reasons.append(
                "Model is below the minimum quality requirement."
            )

        if (
            request.requires_vision
            and ModelCapability.VISION not in model.capabilities
        ):
            reasons.append("Vision capability is required.")

        if (
            request.requires_tools
            and ModelCapability.FUNCTION_CALLING
            not in model.capabilities
        ):
            reasons.append("Tool calling capability is required.")

        if (
            request.requires_structured_output
            and ModelCapability.STRUCTURED_OUTPUT
            not in model.capabilities
        ):
            reasons.append(
                "Structured output capability is required."
            )

        return reasons