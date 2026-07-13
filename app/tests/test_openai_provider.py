"""Unit tests for the OpenAI provider."""

from types import SimpleNamespace

import pytest

from app.domain.contracts.provider_request import ProviderRequest
from app.domain.enums.finish_reason import FinishReason
from app.domain.enums.provider_type import ProviderType
from app.providers.openai_provider import OpenAIProvider


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_openai_provider_normalizes_response(
    monkeypatch,
) -> None:
    provider = OpenAIProvider()

    mock_response = SimpleNamespace(
        id="resp-test-123",
        output_text="AI Gateways centralize model access.",
        status="completed",
        usage=SimpleNamespace(
            input_tokens=12,
            output_tokens=18,
            total_tokens=30,
        ),
        _request_id="req-test-123",
    )

    async def mock_create(**kwargs):
        assert kwargs["model"] == "gpt-4o-mini"
        assert kwargs["input"] == "Explain an AI Gateway."
        return mock_response

    monkeypatch.setattr(
        provider._client.responses,
        "create",
        mock_create,
    )

    request = ProviderRequest(
        model="gpt-4o-mini",
        prompt="Explain an AI Gateway.",
    )

    response = await provider.generate(request)

    assert response.provider == ProviderType.OPENAI
    assert response.model == "gpt-4o-mini"
    assert response.content == (
        "AI Gateways centralize model access."
    )
    assert response.finish_reason == FinishReason.STOP
    assert response.input_tokens == 12
    assert response.output_tokens == 18
    assert response.total_tokens == 30
    assert response.raw_response_id == "resp-test-123"