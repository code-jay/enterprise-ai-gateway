"""Version 1 API router."""

from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.providers import router as providers_router
from app.api.v1.models import router as models_router
from app.api.v1.recommendation import (
    router as recommendation_router,
)

router = APIRouter()

router.include_router(health_router)
router.include_router(providers_router)
router.include_router(models_router)
router.include_router(recommendation_router)