"""Tests for the mock provider."""

import pytest

from app.domain.contracts.provider_request import ProviderRequest
from app.domain.enums.finish_reason import FinishReason
from app.domain.enums.provider_status import ProviderStatus
from app.domain.enums.provider_type import ProviderType
from app.providers.mock_provider import MockProvider


@pytest.mark.anyio
async def test_mock_provider_generates_response() -> None:
    provider = MockProvider()

    request = ProviderRequest(
        model="mock-model",
        prompt="Explain RAG.",
    )

    response = await provider.generate(request)

    assert response.provider == ProviderType.CUSTOM
    assert response.model == "mock-model"
    assert "Explain RAG." in response.content
    assert response.finish_reason == FinishReason.STOP
    assert response.latency_ms >= 0
    assert response.input_tokens > 0
    assert response.output_tokens > 0
    assert (
        response.total_tokens
        == response.input_tokens + response.output_tokens
    )


@pytest.mark.anyio
async def test_mock_provider_health_check() -> None:
    provider = MockProvider()

    status = await provider.health_check()

    assert status == ProviderStatus.AVAILABLE