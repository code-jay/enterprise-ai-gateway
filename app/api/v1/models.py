"""Model catalog endpoints."""

from fastapi import APIRouter, HTTPException, Query

from app.core.recommendation.model_catalog import model_catalog
from app.domain.enums.provider_type import ProviderType


router = APIRouter(
    prefix="/models",
    tags=["Models"],
)


@router.get("")
async def list_models(
    provider: ProviderType | None = Query(default=None),
) -> dict[str, object]:
    if provider:
        models = model_catalog.find_by_provider(provider)
    else:
        models = model_catalog.list_all()

    return {
        "count": len(models),
        "models": [
            model.model_dump(mode="json")
            for model in models
        ],
    }


@router.get("/{provider}/{model_id}")
async def get_model(
    provider: ProviderType,
    model_id: str,
) -> dict[str, object]:
    try:
        model = model_catalog.get(
            provider,
            model_id,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return model.model_dump(mode="json")