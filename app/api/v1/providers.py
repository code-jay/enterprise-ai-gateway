"""Provider discovery endpoints."""

from fastapi import APIRouter

from app.providers.provider_factory import provider_factory


router = APIRouter(
    prefix="/providers",
    tags=["Providers"],
)


@router.get("")
async def list_providers() -> dict[str, list[str]]:
    providers = [
        provider.value
        for provider in provider_factory.supported_providers()
    ]

    return {
        "providers": providers,
    }