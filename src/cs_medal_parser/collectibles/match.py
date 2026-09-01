"""Match a collectible against a type filter."""

from __future__ import annotations

import re

from cs_medal_parser.collectibles.collectible import Collectible
from cs_medal_parser.collectibles.filter import CollectibleFilter


def compile_type_pattern(types: tuple[str, ...]) -> re.Pattern[str]:
    escaped = "|".join(re.escape(item) for item in types)
    return re.compile(rf"(?i)\b(?:{escaped})\b")


def matches_filter(
    collectible: Collectible,
    pattern: re.Pattern[str],
    collectible_filter: CollectibleFilter,
) -> bool:
    if collectible_filter.require_image and not collectible.image:
        return False

    if collectible.type and pattern.search(collectible.type):
        return True

    haystack = f"{collectible.name or ''} {collectible.description or ''}"
    return bool(pattern.search(haystack))
