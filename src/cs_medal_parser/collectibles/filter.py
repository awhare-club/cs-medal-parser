"""Which collectible kinds this run should keep."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CollectibleFilter:
    types: tuple[str, ...]
    require_image: bool = True

    def __post_init__(self) -> None:
        cleaned = tuple(item.lower().strip() for item in self.types if item.strip())
        if not cleaned:
            raise ValueError("Filter types cannot be empty")
        object.__setattr__(self, "types", cleaned)
