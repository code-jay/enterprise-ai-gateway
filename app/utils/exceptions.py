"""Custom exceptions used across the AI Gateway."""


class GatewayError(Exception):
    """Base exception for gateway-related errors."""


class ProviderError(GatewayError):
    """Raised when an LLM provider request fails."""


class ProviderConfigurationError(ProviderError):
    """Raised when provider configuration is missing or invalid."""


class ProviderNotSupportedError(ProviderError):
    """Raised when a requested provider is unsupported."""


class ProviderTimeoutError(ProviderError):
    """Raised when a provider request exceeds its timeout."""


class ProviderUnavailableError(ProviderError):
    """Raised when a provider is unavailable."""