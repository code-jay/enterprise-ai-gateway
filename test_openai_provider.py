"""Manual OpenAI provider integration test."""

import asyncio

from app.config import settings
from app.domain.contracts.provider_request import ProviderRequest
from app.providers.openai_provider import OpenAIProvider


async def main() -> None:
    provider = OpenAIProvider()

    request = ProviderRequest(
        model=settings.openai_default_model,
        system_prompt=(
            "You are an enterprise AI architecture tutor. "
            "Answer clearly and briefly."
        ),
        prompt="What is the purpose of an AI Gateway?",
        temperature=0.2,
        max_tokens=150,
    )

    response = await provider.generate(request)

    print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())