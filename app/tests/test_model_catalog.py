"""Tests for the model catalog."""

import pytest
from pydantic import ValidationError

from app.core.recommendation.model_catalog import (
    DuplicateModelError,
    ModelCatalog,
    ModelNotFoundError,
    model_catalog,
)
from app.domain.enums.cost_tier import CostTier
from app.domain.enums.privacy_level import PrivacyLevel
from app.domain.enums.provider_type import ProviderType
from app.domain.enums.task_type import TaskType
from app.domain.models.model_info import ModelInfo


def build_test_model() -> ModelInfo:
    return ModelInfo(
        provider=ProviderType.OPENAI,
        model_id="test-model",
        display_name="Test Model",
        supported_tasks={
            TaskType.GENERAL,
            TaskType.CHAT,
        },
        max_context_tokens=10_000,
        max_output_tokens=2_000,
        quality_score=8.0,
        speed_score=7.0,
        cost_score=9.0,
        cost_tier=CostTier.LOW,
    )


def test_model_key() -> None:
    model = build_test_model()

    assert model.key == "openai:test-model"


def test_model_supports_task() -> None:
    model = build_test_model()

    assert model.supports_task(TaskType.CHAT)
    assert model.supports_task(TaskType.SUMMARIZATION)


def test_model_rejects_invalid_token_limits() -> None:
    with pytest.raises(ValidationError):
        ModelInfo(
            provider=ProviderType.OPENAI,
            model_id="invalid",
            display_name="Invalid",
            max_context_tokens=1_000,
            max_output_tokens=2_000,
        )


def test_catalog_register_and_get() -> None:
    catalog = ModelCatalog()
    model = build_test_model()

    catalog.register(model)

    result = catalog.get(
        ProviderType.OPENAI,
        "test-model",
    )

    assert result == model


def test_catalog_rejects_duplicate_model() -> None:
    catalog = ModelCatalog()
    model = build_test_model()

    catalog.register(model)

    with pytest.raises(DuplicateModelError):
        catalog.register(model)


def test_catalog_rejects_unknown_model() -> None:
    catalog = ModelCatalog()

    with pytest.raises(ModelNotFoundError):
        catalog.get(
            ProviderType.OPENAI,
            "missing-model",
        )


def test_find_by_provider() -> None:
    models = model_catalog.find_by_provider(
        ProviderType.OPENAI
    )

    assert models
    assert all(
        model.provider == ProviderType.OPENAI
        for model in models
    )


def test_find_eligible_for_vision() -> None:
    models = model_catalog.find_eligible(
        task=TaskType.VISION,
        context_length=10_000,
        privacy=PrivacyLevel.PUBLIC,
        requires_vision=True,
    )

    assert models
    assert all(model.supports_vision for model in models)


def test_restricted_data_uses_private_models() -> None:
    models = model_catalog.find_eligible(
        task=TaskType.CHAT,
        context_length=5_000,
        privacy=PrivacyLevel.RESTRICTED,
    )

    assert models
    assert all(
        model.supports_privacy(
            PrivacyLevel.RESTRICTED
        )
        for model in models
    )


def test_disable_model() -> None:
    catalog = ModelCatalog([build_test_model()])

    catalog.disable(
        ProviderType.OPENAI,
        "test-model",
    )

    assert catalog.list_all() == []
    assert len(
        catalog.list_all(include_disabled=True)
    ) == 1