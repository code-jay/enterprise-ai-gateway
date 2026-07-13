"""Custom exceptions used across the Enterprise AI Gateway."""


class GatewayError(Exception):
    """Base exception for all gateway errors."""


class ProviderError(GatewayError):
    """Base exception for provider-related errors."""


class ProviderConfigurationError(ProviderError):
    """Raised when provider configuration is missing or invalid."""


class ProviderAuthenticationError(ProviderError):
    """Raised when provider authentication fails."""


class ProviderRateLimitError(ProviderError):
    """Raised when a provider rate limit is exceeded."""


class ProviderTimeoutError(ProviderError):
    """Raised when a provider request times out."""


class ProviderUnavailableError(ProviderError):
    """Raised when a provider is temporarily unavailable."""


class ProviderRequestError(ProviderError):
    """Raised when a provider rejects a request."""


class ProviderNotSupportedError(ProviderError):
    """Raised when the requested provider is not registered."""