"""Rarity as published by the CS collectibles catalog."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Rarity(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str | None = None
    name: str | None = None
    color: str | None = Field(default=None, description="Hex color, e.g. #eb4b4b")
