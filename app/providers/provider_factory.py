"""Factory responsible for creating provider adapters."""

from collections.abc import Callable

from app.domain.enums.provider_type import ProviderType
from app.providers.base_provider import BaseProvider
from app.providers.mock_provider import MockProvider
from app.utils.exceptions import ProviderNotSupportedError


ProviderBuilder = Callable[[], BaseProvider]


class ProviderFactory:
    """Registry-based provider factory."""

    def __init__(self) -> None:
        self._providers: dict[
            ProviderType,
            ProviderBuilder,
        ] = {
            ProviderType.CUSTOM: MockProvider,
        }

    def register(
        self,
        provider_type: ProviderType,
        builder: ProviderBuilder,
    ) -> None:
        """Register or replace a provider adapter."""
        self._providers[provider_type] = builder

    def create(
        self,
        provider_type: ProviderType,
    ) -> BaseProvider:
        """Create an adapter for the requested provider."""
        builder = self._providers.get(provider_type)

        if builder is None:
            raise ProviderNotSupportedError(
                f"Provider '{provider_type.value}' is not registered."
            )

        return builder()

    def supported_providers(self) -> list[ProviderType]:
        """Return all registered provider types."""
        return list(self._providers.keys())


provider_factory = ProviderFactory()