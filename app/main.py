"""FastAPI entry point."""

from fastapi import FastAPI

from app.api.v1.router import router as v1_router
from app.config import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)


app.include_router(
    v1_router,
    prefix="/api/v1",
)


@app.get("/", tags=["Root"])
async def root() -> dict:
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "status": "running",
        "api_version": settings.api_version,
        "api_base_url": settings.api_base_url,
        "health_endpoint": f"{settings.api_base_url}/health",
        "documentation": "/docs",
    }