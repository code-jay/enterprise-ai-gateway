"""Registry of models available to the Enterprise AI Gateway."""

from collections.abc import Iterable

from app.domain.enums.cost_tier import CostTier
from app.domain.enums.model_capability import ModelCapability
from app.domain.enums.model_status import ModelStatus
from app.domain.enums.privacy_level import PrivacyLevel
from app.domain.enums.provider_type import ProviderType
from app.domain.enums.task_type import TaskType
from app.domain.models.model_info import ModelInfo
from app.utils.exceptions import GatewayError


class ModelNotFoundError(GatewayError):
    """Raised when a model cannot be found in the catalog."""


class DuplicateModelError(GatewayError):
    """Raised when registering an existing catalog key."""


class ModelCatalog:
    """In-memory model metadata registry."""

    def __init__(
        self,
        models: Iterable[ModelInfo] | None = None,
    ) -> None:
        self._models: dict[str, ModelInfo] = {}

        if models:
            for model in models:
                self.register(model)

    def register(
        self,
        model: ModelInfo,
        *,
        replace: bool = False,
    ) -> None:
        """Register a model in the catalog."""

        if model.key in self._models and not replace:
            raise DuplicateModelError(
                f"Model '{model.key}' is already registered."
            )

        self._models[model.key] = model

    def get(
        self,
        provider: ProviderType,
        model_id: str,
    ) -> ModelInfo:
        """Return one model by provider and model ID."""

        key = f"{provider.value}:{model_id}"

        model = self._models.get(key)

        if model is None:
            raise ModelNotFoundError(
                f"Model '{key}' was not found."
            )

        return model

    def get_by_key(self, key: str) -> ModelInfo:
        """Return one model using its full catalog key."""

        model = self._models.get(key)

        if model is None:
            raise ModelNotFoundError(
                f"Model '{key}' was not found."
            )

        return model

    def list_all(
        self,
        *,
        include_disabled: bool = False,
    ) -> list[ModelInfo]:
        """Return catalog models."""

        models = list(self._models.values())

        if include_disabled:
            return models

        return [
            model
            for model in models
            if model.is_available()
        ]

    def find_by_provider(
        self,
        provider: ProviderType,
    ) -> list[ModelInfo]:
        """Return available models for one provider."""

        return [
            model
            for model in self.list_all()
            if model.provider == provider
        ]

    def find_by_task(
        self,
        task: TaskType,
    ) -> list[ModelInfo]:
        """Return models supporting a task."""

        return [
            model
            for model in self.list_all()
            if model.supports_task(task)
        ]

    def find_eligible(
        self,
        *,
        task: TaskType,
        context_length: int,
        privacy: PrivacyLevel,
        provider: ProviderType | None = None,
        requires_vision: bool = False,
        requires_tools: bool = False,
    ) -> list[ModelInfo]:
        """Return models satisfying workload constraints."""

        candidates: list[ModelInfo] = []

        for model in self.list_all():
            if provider and model.provider != provider:
                continue

            if not model.supports_task(task):
                continue

            if context_length > model.max_context_tokens:
                continue

            if not model.supports_privacy(privacy):
                continue

            if requires_vision and not model.supports_vision:
                continue

            if requires_tools and not model.supports_tools:
                continue

            candidates.append(model)

        return candidates

    def disable(
        self,
        provider: ProviderType,
        model_id: str,
    ) -> None:
        """Disable one catalog model."""

        model = self.get(provider, model_id)

        self._models[model.key] = model.model_copy(
            update={"enabled": False}
        )

    def enable(
        self,
        provider: ProviderType,
        model_id: str,
    ) -> None:
        """Enable one catalog model."""

        model = self.get(provider, model_id)

        self._models[model.key] = model.model_copy(
            update={
                "enabled": True,
                "status": ModelStatus.ACTIVE,
            }
        )

DEFAULT_MODELS = [
    ModelInfo(
        provider=ProviderType.OPENAI,
        model_id="gpt-4o-mini",
        display_name="OpenAI Fast Model",
        description=(
            "General-purpose, cost-conscious model profile."
        ),
        supported_tasks={
            TaskType.GENERAL,
            TaskType.CHAT,
            TaskType.QA,
            TaskType.SUMMARIZATION,
            TaskType.CLASSIFICATION,
            TaskType.EXTRACTION,
            TaskType.CODE_GENERATION,
            TaskType.RAG,
        },
        capabilities={
            ModelCapability.CHAT,
            ModelCapability.CODING,
            ModelCapability.VISION,
            ModelCapability.FUNCTION_CALLING,
            ModelCapability.STRUCTURED_OUTPUT,
        },
        max_context_tokens=128_000,
        max_output_tokens=16_000,
        quality_score=8.0,
        speed_score=9.0,
        cost_score=9.0,
        cost_tier=CostTier.LOW,
        supports_tools=True,
        supports_structured_output=True,
        supports_vision=True,
    ),
    ModelInfo(
        provider=ProviderType.ANTHROPIC,
        model_id="claude-sonnet",
        display_name="Anthropic Reasoning Model",
        description=(
            "Reasoning and long-document workload profile."
        ),
        supported_tasks={
            TaskType.GENERAL,
            TaskType.CHAT,
            TaskType.QA,
            TaskType.SUMMARIZATION,
            TaskType.CODE_GENERATION,
            TaskType.CODE_REVIEW,
            TaskType.DOCUMENT_ANALYSIS,
            TaskType.REASONING,
            TaskType.RAG,
        },
        capabilities={
            ModelCapability.CHAT,
            ModelCapability.REASONING,
            ModelCapability.CODING,
            ModelCapability.LONG_CONTEXT,
            ModelCapability.FUNCTION_CALLING,
        },
        max_context_tokens=200_000,
        max_output_tokens=16_000,
        quality_score=9.5,
        speed_score=7.5,
        cost_score=6.0,
        cost_tier=CostTier.HIGH,
        supports_tools=True,
        supports_vision=True,
    ),
    ModelInfo(
        provider=ProviderType.GOOGLE,
        model_id="gemini-pro",
        display_name="Google Multimodal Model",
        description=(
            "Long-context and multimodal workload profile."
        ),
        supported_tasks={
            TaskType.GENERAL,
            TaskType.CHAT,
            TaskType.QA,
            TaskType.SUMMARIZATION,
            TaskType.DOCUMENT_ANALYSIS,
            TaskType.VISION,
            TaskType.RAG,
        },
        capabilities={
            ModelCapability.CHAT,
            ModelCapability.VISION,
            ModelCapability.LONG_CONTEXT,
            ModelCapability.FUNCTION_CALLING,
            ModelCapability.STRUCTURED_OUTPUT,
        },
        max_context_tokens=1_000_000,
        max_output_tokens=16_000,
        quality_score=9.0,
        speed_score=8.0,
        cost_score=7.0,
        cost_tier=CostTier.MEDIUM,
        supports_tools=True,
        supports_structured_output=True,
        supports_vision=True,
    ),
    ModelInfo(
        provider=ProviderType.OLLAMA,
        model_id="llama-private",
        display_name="Private Self-Hosted Model",
        description=(
            "Private deployment profile for restricted workloads."
        ),
        supported_tasks={
            TaskType.GENERAL,
            TaskType.CHAT,
            TaskType.QA,
            TaskType.SUMMARIZATION,
            TaskType.RAG,
        },
        capabilities={
            ModelCapability.CHAT,
        },
        max_context_tokens=32_000,
        max_output_tokens=8_000,
        quality_score=7.0,
        speed_score=6.0,
        cost_score=8.0,
        cost_tier=CostTier.MEDIUM,
        supported_privacy_levels={
            PrivacyLevel.PUBLIC,
            PrivacyLevel.INTERNAL,
            PrivacyLevel.CONFIDENTIAL,
            PrivacyLevel.RESTRICTED,
        },
        supports_tools=False,
        supports_vision=False,
    ),
]


model_catalog = ModelCatalog(DEFAULT_MODELS)