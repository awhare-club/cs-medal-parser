"""Runtime settings for a parse run."""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_TYPES = (
    "pick",
    "coin",
    "medal",
    "pin",
    "trophy",
    "badge",
    "pass",
    "stars",
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CS_MEDAL_",
        extra="ignore",
    )

    collectibles_url: str = (
        "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/collectibles.json"
    )
    output_folder: Path = Path("data/medals")
    dump_folder: Path = Path("data/responses")
    collectible_types: tuple[str, ...] = Field(default=DEFAULT_TYPES)
    require_image: bool = True
    max_workers: int = 10
    request_timeout: int = 30
    max_retries: int = 3
    target_width: int = 256
    target_height: int = 192
