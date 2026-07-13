"""Tests for gateway domain contracts."""

import pytest
from pydantic import ValidationError

from app.domain.contracts.gateway_request import GatewayRequest
from app.domain.contracts.gateway_response import GatewayResponse
from app.domain.contracts.provider_request import ProviderRequest
from app.domain.contracts.provider_response import ProviderResponse
from app.domain.contracts.recommendation_request import (
    RecommendationRequest,
)
from app.domain.contracts.recommendation_response import (
    RecommendationResponse,
)
from app.domain.enums.privacy_level import PrivacyLevel
from app.domain.enums.provider_type import ProviderType
from app.domain.enums.response_speed import ResponseSpeed
from app.domain.enums.task_type import TaskType
from app.domain.enums.finish_reason import FinishReason
from app.domain.enums.provider_type import ProviderType

def test_gateway_request_with_defaults() -> None:
    request = GatewayRequest(
        prompt="Explain Enterprise AI."
    )

    assert request.prompt == "Explain Enterprise AI."
    assert request.task == TaskType.GENERAL
    assert request.privacy == PrivacyLevel.PUBLIC
    assert request.response_speed == ResponseSpeed.BALANCED
    assert request.provider is None
    assert request.temperature == 0.2
    assert request.max_tokens == 1024
    assert request.stream is False
    assert request.request_id is not None


def test_gateway_request_with_all_fields() -> None:
    request = GatewayRequest(
        prompt="Review this Python code.",
        task=TaskType.CODE_REVIEW,
        provider=ProviderType.OPENAI,
        privacy=PrivacyLevel.INTERNAL,
        response_speed=ResponseSpeed.BEST_QUALITY,
        temperature=0.1,
        max_tokens=2048,
        stream=True,
        user_id="user-101",
        tenant_id="tenant-1",
    )

    assert request.provider == ProviderType.OPENAI
    assert request.task == TaskType.CODE_REVIEW
    assert request.user_id == "user-101"
    assert request.tenant_id == "tenant-1"


def test_gateway_request_rejects_empty_prompt() -> None:
    with pytest.raises(ValidationError):
        GatewayRequest(prompt="")


def test_gateway_request_rejects_invalid_temperature() -> None:
    with pytest.raises(ValidationError):
        GatewayRequest(
            prompt="Test",
            temperature=3.0,
        )


def test_gateway_request_rejects_invalid_provider() -> None:
    with pytest.raises(ValidationError):
        GatewayRequest(
            prompt="Test",
            provider="unknown-provider",
        )


def test_recommendation_request() -> None:
    request = RecommendationRequest(
        task=TaskType.DOCUMENT_ANALYSIS,
        context_length=50_000,
        budget="medium",
        privacy=PrivacyLevel.INTERNAL,
        response_speed=ResponseSpeed.BALANCED,
    )

    assert request.context_length == 50_000
    assert request.task == TaskType.DOCUMENT_ANALYSIS


def test_provider_request() -> None:
    request = ProviderRequest(
        model="gpt-4o-mini",
        prompt="Explain RAG.",
        temperature=0.2,
        max_tokens=512,
        stream=False,
    )

    assert request.model == "gpt-4o-mini"
    assert request.max_tokens == 512


def test_provider_response() -> None:
    response = ProviderResponse(
        provider=ProviderType.OPENAI,
        model="gpt-4o-mini",
        content="RAG combines retrieval and generation.",
        finish_reason=FinishReason.STOP,
        latency_ms=450.5,
        input_tokens=25,
        output_tokens=40,
        total_tokens=65,
    )

    assert response.success is True
    assert response.provider == ProviderType.OPENAI
    assert response.model == "gpt-4o-mini"
    assert response.content == "RAG combines retrieval and generation."
    assert response.finish_reason == FinishReason.STOP
    assert response.input_tokens == 25
    assert response.output_tokens == 40
    assert response.total_tokens == 65


def test_gateway_response() -> None:
    response = GatewayResponse(
        provider=ProviderType.OPENAI,
        model="gpt-4o-mini",
        response="Enterprise AI is...",
        latency_ms=600.25,
        input_tokens=100,
        output_tokens=150,
        total_tokens=250,
        estimated_cost=0.0012,
    )

    assert response.success is True
    assert response.total_tokens == 250
    assert response.provider == ProviderType.OPENAI


def test_recommendation_response() -> None:
    response = RecommendationResponse(
        provider=ProviderType.ANTHROPIC,
        model="claude-sonnet",
        score=92.5,
        reason=[
            "Strong document analysis",
            "Supports long context",
        ],
        alternatives=[
            "openai:gpt-4o",
            "google:gemini-pro",
        ],
    )

    assert response.score == 92.5
    assert len(response.reason) == 2
    assert len(response.alternatives) == 2