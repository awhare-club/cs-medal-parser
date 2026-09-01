from cs_medal_parser.pipeline.settings import Settings


def test_default_catalog_url_is_current_api() -> None:
    settings = Settings()
    assert settings.collectibles_url.endswith("/public/api/en/collectibles.json")
    assert "raw.githubusercontent.com/ByMykel/CSGO-API" in settings.collectibles_url


def test_env_overrides(monkeypatch) -> None:
    monkeypatch.setenv("CS_MEDAL_MAX_WORKERS", "3")
    monkeypatch.setenv("CS_MEDAL_TARGET_WIDTH", "128")
    settings = Settings()
    assert settings.max_workers == 3
    assert settings.target_width == 128
