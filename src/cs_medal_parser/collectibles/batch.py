"""A filtered slice of the collectible catalog."""

from __future__ import annotations

from dataclasses import dataclass

from loguru import logger

from cs_medal_parser.collectibles.collectible import Collectible
from cs_medal_parser.collectibles.filter import CollectibleFilter
from cs_medal_parser.collectibles.match import compile_type_pattern, matches_filter


@dataclass(frozen=True, slots=True)
class CollectibleBatch:
    items: tuple[Collectible, ...]
    total_count: int

    @property
    def filtered_count(self) -> int:
        return len(self.items)


def filter_collectibles(
    collectibles: list[Collectible],
    collectible_filter: CollectibleFilter,
) -> CollectibleBatch:
    if not collectibles:
        logger.warning("No collectibles provided for filtering")
        return CollectibleBatch(items=(), total_count=0)

    logger.info(
        "Filtering {} items for types: {}",
        len(collectibles),
        collectible_filter.types,
    )
    pattern = compile_type_pattern(collectible_filter.types)
    matched: list[Collectible] = []

    for collectible in collectibles:
        try:
            if matches_filter(collectible, pattern, collectible_filter):
                matched.append(collectible)
        except Exception as exc:
            logger.warning("Error filtering collectible {}: {}", collectible.id, exc)

    logger.info("Found {} matching collectibles", len(matched))
    return CollectibleBatch(items=tuple(matched), total_count=len(collectibles))
