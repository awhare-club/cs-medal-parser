"""Orchestrate fetch → persist → filter → image processing."""

from __future__ import annotations

import time

from loguru import logger

from cs_medal_parser.catalog.fetch import fetch_catalog
from cs_medal_parser.catalog.persist import persist_catalog
from cs_medal_parser.collectibles.batch import filter_collectibles
from cs_medal_parser.collectibles.filter import CollectibleFilter
from cs_medal_parser.http.session import create_session
from cs_medal_parser.images.normalize import ImageSize
from cs_medal_parser.images.process import process_images
from cs_medal_parser.pipeline.settings import Settings
from cs_medal_parser.pipeline.summary import log_summary


def run(settings: Settings | None = None) -> bool:
    settings = settings or Settings()
    started = time.perf_counter()
    logger.info("Starting CS medal parser")

    collectible_filter = CollectibleFilter(
        types=settings.collectible_types,
        require_image=settings.require_image,
    )
    size = ImageSize(width=settings.target_width, height=settings.target_height)

    try:
        with create_session(
            max_retries=settings.max_retries,
            pool_size=max(settings.max_workers, 10),
        ) as session:
            collectibles = fetch_catalog(
                session,
                settings.collectibles_url,
                timeout=settings.request_timeout,
            )
            if not collectibles:
                logger.error("No collectibles fetched from API")
                return False

            persist_catalog(collectibles, settings.dump_folder)

            batch = filter_collectibles(collectibles, collectible_filter)
            if not batch.items:
                logger.warning("No collectibles matched the filter criteria")
                return False

            results = process_images(
                batch.items,
                settings.output_folder,
                session,
                size=size,
                timeout=settings.request_timeout,
                max_workers=settings.max_workers,
            )
    except Exception as exc:
        logger.error("Fatal error in main execution: {}", exc)
        return False

    log_summary(results, time.perf_counter() - started)
    return True
