"""
Supported LLM Providers.
"""

from enum import Enum


class ProviderType(str, Enum):

    OPENAI = "openai"

    ANTHROPIC = "anthropic"

    GOOGLE = "google"

    AZURE_OPENAI = "azure_openai"

    AWS_BEDROCK = "bedrock"

    OLLAMA = "ollama"

    MISTRAL = "mistral"

    OPENROUTER = "openrouter"

    CUSTOM = "custom"