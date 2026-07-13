"""Mock provider used for local development and tests."""

import asyncio
from time import perf_counter
from uuid import uuid4

from app.domain.contracts.provider_request import ProviderRequest
from app.domain.contracts.provider_response import ProviderResponse
from app.domain.enums.finish_reason import FinishReason
from app.domain.enums.provider_type import ProviderType
from app.providers.base_provider import BaseProvider


class MockProvider(BaseProvider):
    """Deterministic provider that does not call an external API."""

    provider_type = ProviderType.CUSTOM

    async def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        start = perf_counter()

        await asyncio.sleep(0.01)

        content = (
            f"Mock response generated for model '{request.model}': "
            f"{request.prompt}"
        )

        input_tokens = max(1, len(request.prompt.split()))
        output_tokens = max(1, len(content.split()))

        latency_ms = round(
            (perf_counter() - start) * 1000,
            2,
        )

        return ProviderResponse(
            provider=self.provider_type,
            model=request.model,
            content=content,
            finish_reason=FinishReason.STOP,
            latency_ms=latency_ms,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            raw_response_id=str(uuid4()),
            metadata={
                "mock": True,
            },
        )

    def supports_streaming(self) -> bool:
        return False