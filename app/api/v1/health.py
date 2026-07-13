"""Health-check endpoints for the Enterprise AI Gateway."""

from datetime import datetime, timezone

from fastapi import APIRouter

from app.config import settings


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
async def health_check() -> dict[str, str]:
    """Return the current health status of the service."""

    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }