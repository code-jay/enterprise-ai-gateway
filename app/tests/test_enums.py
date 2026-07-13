"""Tests for domain enums."""

import pytest

from app.domain.enums.finish_reason import FinishReason
from app.domain.enums.model_capability import ModelCapability
from app.domain.enums.privacy_level import PrivacyLevel
from app.domain.enums.provider_status import ProviderStatus
from app.domain.enums.provider_type import ProviderType
from app.domain.enums.response_speed import ResponseSpeed
from app.domain.enums.task_type import TaskType


def test_provider_type_values() -> None:
    assert ProviderType.OPENAI.value == "openai"
    assert ProviderType.ANTHROPIC.value == "anthropic"
    assert ProviderType.GOOGLE.value == "google"


def test_task_type_values() -> None:
    assert TaskType.CHAT.value == "chat"
    assert TaskType.RAG.value == "rag"
    assert TaskType.CODE_GENERATION.value == "code_generation"


def test_privacy_levels() -> None:
    assert PrivacyLevel.PUBLIC.value == "public"
    assert PrivacyLevel.RESTRICTED.value == "restricted"


def test_response_speed_values() -> None:
    assert ResponseSpeed.FAST.value == "fast"
    assert ResponseSpeed.BEST_QUALITY.value == "best_quality"


def test_model_capability_values() -> None:
    assert ModelCapability.VISION.value == "vision"
    assert (
        ModelCapability.FUNCTION_CALLING.value
        == "function_calling"
    )


def test_provider_status_values() -> None:
    assert ProviderStatus.AVAILABLE.value == "available"
    assert ProviderStatus.UNAVAILABLE.value == "unavailable"


def test_finish_reason_values() -> None:
    assert FinishReason.STOP.value == "stop"
    assert FinishReason.TOOL_CALL.value == "tool_call"


def test_invalid_enum_value() -> None:
    with pytest.raises(ValueError):
        ProviderType("invalid-provider")