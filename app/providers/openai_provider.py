"""OpenAI provider adapter."""

from time import perf_counter

import openai
from openai import AsyncOpenAI

from app.config import settings
from app.domain.contracts.provider_request import ProviderRequest
from app.domain.contracts.provider_response import ProviderResponse
from app.domain.enums.finish_reason import FinishReason
from app.domain.enums.provider_status import ProviderStatus
from app.domain.enums.provider_type import ProviderType
from app.providers.base_provider import BaseProvider
from app.utils.exceptions import (
    ProviderAuthenticationError,
    ProviderConfigurationError,
    ProviderError,
    ProviderRateLimitError,
    ProviderRequestError,
    ProviderTimeoutError,
    ProviderUnavailableError,
)


class OpenAIProvider(BaseProvider):
    """Adapter for OpenAI models using the Responses API."""

    provider_type = ProviderType.OPENAI

    def __init__(self) -> None:
        if settings.openai_api_key is None:
            raise ProviderConfigurationError(
                "OPENAI_API_KEY is not configured."
            )

        api_key = settings.openai_api_key.get_secret_value()

        if not api_key.strip():
            raise ProviderConfigurationError(
                "OPENAI_API_KEY is empty."
            )

        self._client = AsyncOpenAI(
            api_key=api_key,
            timeout=settings.openai_timeout_seconds,
            max_retries=settings.openai_max_retries,
        )

    async def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        """Send a request to OpenAI and normalize the response."""

        if request.stream:
            raise ProviderRequestError(
                "Streaming is not implemented in generate()."
            )

        start = perf_counter()

        try:
            response = await self._client.responses.create(
                model=request.model,
                instructions=request.system_prompt,
                input=request.prompt,
                temperature=request.temperature,
                max_output_tokens=request.max_tokens,
            )

        except openai.AuthenticationError as exc:
            raise ProviderAuthenticationError(
                "OpenAI authentication failed."
            ) from exc

        except openai.RateLimitError as exc:
            raise ProviderRateLimitError(
                "OpenAI rate limit exceeded."
            ) from exc

        except openai.APITimeoutError as exc:
            raise ProviderTimeoutError(
                "OpenAI request timed out."
            ) from exc

        except openai.APIConnectionError as exc:
            raise ProviderUnavailableError(
                "Unable to connect to OpenAI."
            ) from exc

        except openai.BadRequestError as exc:
            raise ProviderRequestError(
                f"OpenAI rejected the request: {exc}"
            ) from exc

        except openai.APIStatusError as exc:
            if exc.status_code >= 500:
                raise ProviderUnavailableError(
                    f"OpenAI service error: HTTP {exc.status_code}"
                ) from exc

            raise ProviderRequestError(
                f"OpenAI API error: HTTP {exc.status_code}"
            ) from exc

        except openai.APIError as exc:
            raise ProviderError(
                f"Unexpected OpenAI API error: {exc}"
            ) from exc

        latency_ms = round(
            (perf_counter() - start) * 1000,
            2,
        )

        usage = response.usage

        input_tokens = usage.input_tokens if usage else 0
        output_tokens = usage.output_tokens if usage else 0
        total_tokens = usage.total_tokens if usage else (
            input_tokens + output_tokens
        )

        return ProviderResponse(
            provider=self.provider_type,
            model=request.model,
            content=response.output_text or "",
            finish_reason=self._map_finish_reason(response.status),
            latency_ms=latency_ms,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            raw_response_id=response.id,
            metadata={
                "openai_request_id": response._request_id,
                "response_status": response.status,
            },
        )

    async def health_check(self) -> ProviderStatus:
        """
        Validate that the provider can serve a minimal request.

        This consumes a small amount of API usage. Later, cache the result
        instead of calling it for every gateway health check.
        """

        try:
            await self._client.responses.create(
                model=settings.openai_default_model,
                input="Reply with OK.",
                max_output_tokens=5,
            )
            return ProviderStatus.AVAILABLE

        except (
            openai.AuthenticationError,
            openai.BadRequestError,
        ):
            return ProviderStatus.UNAVAILABLE

        except (
            openai.RateLimitError,
            openai.APITimeoutError,
            openai.APIConnectionError,
            openai.APIStatusError,
        ):
            return ProviderStatus.DEGRADED

    def supports_streaming(self) -> bool:
        return True

    @staticmethod
    def _map_finish_reason(
        response_status: str | None,
    ) -> FinishReason:
        """Normalize an OpenAI response status."""

        if response_status == "completed":
            return FinishReason.STOP

        if response_status == "incomplete":
            return FinishReason.LENGTH

        if response_status == "failed":
            return FinishReason.ERROR

        return FinishReason.STOP