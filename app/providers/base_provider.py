"""Abstract interface implemented by every LLM provider."""

from abc import ABC, abstractmethod

from app.domain.contracts.provider_request import ProviderRequest
from app.domain.contracts.provider_response import ProviderResponse
from app.domain.enums.provider_status import ProviderStatus
from app.domain.enums.provider_type import ProviderType


class BaseProvider(ABC):
    """Provider-independent LLM interface."""

    provider_type: ProviderType

    @abstractmethod
    async def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        """
        Generate a non-streaming LLM response.

        Every provider adapter must normalize its native response into
        ProviderResponse.
        """

    async def health_check(self) -> ProviderStatus:
        """
        Return the current provider status.

        Providers may override this with a real health check.
        """
        return ProviderStatus.AVAILABLE

    def supports_streaming(self) -> bool:
        """Return whether this provider supports streaming."""
        return False

    def supports_model(self, model: str) -> bool:
        """
        Return whether this provider supports the supplied model.

        Override this when maintaining an explicit model catalog.
        """
        return bool(model.strip())