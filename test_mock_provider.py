import asyncio

from app.domain.contracts.provider_request import ProviderRequest
from app.providers.mock_provider import MockProvider


async def main() -> None:
    provider = MockProvider()

    request = ProviderRequest(
        model="mock-enterprise-model",
        prompt="Explain the purpose of an AI Gateway.",
        temperature=0.2,
        max_tokens=300,
    )

    response = await provider.generate(request)

    print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())