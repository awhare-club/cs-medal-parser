"""Turn raw catalog JSON into collectible models."""

from __future__ import annotations

from typing import Any

from loguru import logger

from cs_medal_parser.collectibles.collectible import Collectible


def parse_collectibles(raw_items: list[dict[str, Any]]) -> list[Collectible]:
    collectibles: list[Collectible] = []
    for item in raw_items:
        try:
            collectibles.append(Collectible.model_validate(item))
        except Exception as exc:
            logger.warning(
                "Failed to parse collectible {}: {}",
                item.get("id", "unknown"),
                exc,
            )
    return collectibles
