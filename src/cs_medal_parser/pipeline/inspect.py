"""Inspect the newest cached catalog dump against the type filter."""

from __future__ import annotations

import json
from pathlib import Path

from loguru import logger

from cs_medal_parser.catalog.persist import load_catalog, newest_dump
from cs_medal_parser.collectibles.batch import CollectibleBatch, filter_collectibles
from cs_medal_parser.collectibles.collectible import Collectible
from cs_medal_parser.collectibles.filter import CollectibleFilter
from cs_medal_parser.pipeline.settings import Settings


def inspect_latest_dump(settings: Settings | None = None) -> bool:
    settings = settings or Settings()
    logger.info("Inspecting newest catalog dump")

    dump_path = newest_dump(settings.dump_folder)
    if dump_path is None:
        logger.error("No JSON dumps found in {}", settings.dump_folder)
        return False

    logger.info("Using newest file: {}", dump_path.name)
    collectibles = load_catalog(dump_path)
    if not collectibles:
        logger.error("Failed to load collectibles from file")
        return False

    logger.info("Loaded {} collectibles from {}", len(collectibles), dump_path.name)
    batch = filter_collectibles(
        collectibles,
        CollectibleFilter(
            types=settings.collectible_types,
            require_image=settings.require_image,
        ),
    )
    if not batch.items:
        logger.warning("No collectibles matched the filter criteria")
        return False

    output = settings.dump_folder / "filtered.json"
    _write_filtered(batch.items, output)
    _log_sample(batch)
    return True


def _write_filtered(items: tuple[Collectible, ...], output: Path) -> None:
    payload = [
        {"id": item.id, "image": str(item.image) if item.image else None}
        for item in items
    ]
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )
    logger.success("Filtered results saved to {}", output)


def _log_sample(batch: CollectibleBatch) -> None:
    sample = batch.items[:5]
    logger.info("Filter matched {} collectibles", batch.filtered_count)
    logger.info("Sample of first {} filtered results:", len(sample))
    for index, item in enumerate(sample, start=1):
        preview = f"{item.image}"[:50] + "..." if item.image else "N/A"
        logger.info("  {}. ID: {}, Image: {}", index, item.id, preview)

    with_images = sum(1 for item in batch.items if item.image)
    logger.info("Statistics:")
    logger.info("  • Total collectibles: {}", batch.total_count)
    logger.info("  • Matched filter: {}", batch.filtered_count)
    logger.info("  • With images: {}", with_images)
