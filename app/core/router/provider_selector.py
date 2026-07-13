from app.domain.enums.provider_type import ProviderType
from app.providers.base_provider import BaseProvider
from app.providers.provider_factory import provider_factory


class ProviderSelector:

    def select(
        self,
        provider_type: ProviderType,
    ) -> BaseProvider:

        return provider_factory.create(provider_type)