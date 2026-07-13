"""Tests for the GatewayService."""

import pytest

from app.core.gateway.gateway_service import GatewayService
from app.domain.contracts.gateway_request import GatewayRequest
from app.domain.contracts.gateway_response import GatewayResponse
from app.domain.enums.finish_reason import FinishReason
from app.domain.enums.provider_type import ProviderType
from app.domain.enums.task_type import TaskType


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


class FakeModelRouter:
    """Test router that avoids external provider calls."""

    async def route(
        self,
        request: GatewayRequest,
    ) -> GatewayResponse:
        return GatewayResponse(
            provider=ProviderType.OPENAI,
            model="gpt-4o-mini",
            content="Mock gateway response.",
            finish_reason=FinishReason.STOP,
            latency_ms=100.0,
            input_tokens=10,
            output_tokens=20,
            total_tokens=30,
            estimated_cost=0.001,
            recommendation_score=90.5,
            routing_reason=[
                "Fast and cost-effective model.",
            ],
            request_id=request.request_id,
        )


@pytest.mark.anyio
async def test_gateway_service_generates_response() -> None:
    service = GatewayService(
        model_router=FakeModelRouter(),
    )

    request = GatewayRequest(
        prompt="Explain Enterprise AI.",
        task=TaskType.CHAT,
    )

    response = await service.generate(request)

    assert response.provider == ProviderType.OPENAI
    assert response.model == "gpt-4o-mini"
    assert response.content == "Mock gateway response."
    assert response.total_tokens == 30
    assert response.recommendation_score == 90.5
    assert "gateway_latency_ms" in response.metadata