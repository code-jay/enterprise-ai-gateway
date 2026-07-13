"""Tests for the provider factory."""

import pytest

from app.domain.enums.provider_type import ProviderType
from app.providers.mock_provider import MockProvider
from app.providers.provider_factory import ProviderFactory
from app.utils.exceptions import ProviderNotSupportedError


def test_factory_creates_mock_provider() -> None:
    factory = ProviderFactory()

    provider = factory.create(ProviderType.CUSTOM)

    assert isinstance(provider, MockProvider)
    assert provider.provider_type == ProviderType.CUSTOM


def test_factory_lists_supported_providers() -> None:
    factory = ProviderFactory()

    providers = factory.supported_providers()

    assert ProviderType.CUSTOM in providers


def test_factory_rejects_unregistered_provider() -> None:
    factory = ProviderFactory()

    with pytest.raises(ProviderNotSupportedError):
        factory.create(ProviderType.OPENAI)