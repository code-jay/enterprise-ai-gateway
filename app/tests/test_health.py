"""Tests for health-check endpoints."""

from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200

    body = response.json()

    assert body["service"] == settings.app_name
    assert body["status"] == "running"
    assert body["api_version"] == settings.api_version


def test_health_endpoint() -> None:
    response = client.get(
        f"{settings.api_base_url}/health"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "healthy"
    assert body["service"] == settings.app_name
    assert body["version"] == settings.app_version
    assert body["environment"] == settings.app_env
    assert "timestamp" in body


def test_unknown_endpoint_returns_404() -> None:
    response = client.get(
        f"{settings.api_base_url}/unknown"
    )

    assert response.status_code == 404