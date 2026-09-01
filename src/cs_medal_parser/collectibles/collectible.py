"""A single Counter-Strike collectible from the catalog."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

from cs_medal_parser.collectibles.rarity import Rarity


class Collectible(BaseModel):
    model_config = ConfigDict(extra="ignore", validate_assignment=True)

    id: str = Field(description="Unique catalog identifier")
    name: str | None = None
    description: str | None = None
    type: str | None = None
    image: HttpUrl | None = None
    def_index: str | None = None
    rarity: Rarity | None = None
    genuine: bool = False
    market_hash_name: str | None = None

    @field_validator("id")
    @classmethod
    def _id_must_be_present(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Collectible ID cannot be empty")
        return cleaned

    @field_validator("image", mode="before")
    @classmethod
    def _empty_image_is_none(cls, value: object) -> object:
        if value == "" or value is None:
            return None
        return value

    @property
    def image_stem(self) -> str:
        return self.id.removeprefix("collectible-")
