"""Tests for application configuration."""

from app.config import Settings


def test_default_settings() -> None:
    settings = Settings(_env_file=None)

    assert settings.app_name == "Enterprise AI Gateway"
    assert settings.app_version == "0.1.0"
    assert settings.api_prefix == "/api"
    assert settings.api_version == "v1"


def test_api_base_url() -> None:
    settings = Settings(
        api_prefix="/api",
        api_version="v1",
        _env_file=None,
    )

    assert settings.api_base_url == "/api/v1"


def test_prefix_normalization() -> None:
    settings = Settings(
        api_prefix="/api/",
        api_version="/v1/",
        _env_file=None,
    )

    assert settings.api_base_url == "/api/v1"


def test_environment_overrides(monkeypatch) -> None:
    monkeypatch.setenv("APP_NAME", "Test AI Gateway")
    monkeypatch.setenv("API_PREFIX", "/platform")
    monkeypatch.setenv("API_VERSION", "v2")

    settings = Settings(_env_file=None)

    assert settings.app_name == "Test AI Gateway"
    assert settings.api_base_url == "/platform/v2"