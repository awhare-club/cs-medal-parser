"""Download and normalize collectible images concurrently."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from loguru import logger

from cs_medal_parser.collectibles.collectible import Collectible
from cs_medal_parser.http.get import get_bytes
from cs_medal_parser.images.cache import is_cached, renormalize_existing
from cs_medal_parser.images.normalize import ImageSize, normalize_bytes
from cs_medal_parser.images.result import ProcessingResult


def process_one(
    collectible: Collectible,
    output_folder: Path,
    session: requests.Session,
    *,
    size: ImageSize,
    timeout: int,
) -> ProcessingResult:
    image_name = f"{collectible.image_stem}.png"
    image_path = output_folder / image_name

    if not collectible.image:
        return ProcessingResult(
            collectible_id=collectible.image_stem,
            image_name=image_name,
            success=False,
            error_message="No image URL provided",
        )

    try:
        if is_cached(image_path, size):
            return ProcessingResult(
                collectible_id=collectible.image_stem,
                image_name=image_name,
                success=True,
                file_path=str(image_path),
            )

        if image_path.exists() and renormalize_existing(image_path, size):
            return ProcessingResult(
                collectible_id=collectible.image_stem,
                image_name=image_name,
                success=True,
                file_path=str(image_path),
            )

        data = get_bytes(session, str(collectible.image), timeout=timeout)
        if not data:
            return ProcessingResult(
                collectible_id=collectible.image_stem,
                image_name=image_name,
                success=False,
                error_message="Image download failed",
            )

        processed = normalize_bytes(data, size)
        processed.save(image_path, "PNG", optimize=True)
        return ProcessingResult(
            collectible_id=collectible.image_stem,
            image_name=image_name,
            success=True,
            file_path=str(image_path),
        )
    except Exception as exc:
        logger.error("Error processing image for {}: {}", collectible.image_stem, exc)
        return ProcessingResult(
            collectible_id=collectible.image_stem,
            image_name=image_name,
            success=False,
            error_message=str(exc),
        )


def process_images(
    collectibles: list[Collectible] | tuple[Collectible, ...],
    output_folder: Path,
    session: requests.Session,
    *,
    size: ImageSize,
    timeout: int,
    max_workers: int,
) -> list[ProcessingResult]:
    with_images = [item for item in collectibles if item.image]
    if not with_images:
        logger.warning("No collectibles to process")
        return []

    output_folder.mkdir(parents=True, exist_ok=True)
    logger.info("Processing {} images with {} workers", len(with_images), max_workers)

    results: list[ProcessingResult] = []
    succeeded = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                process_one,
                collectible,
                output_folder,
                session,
                size=size,
                timeout=timeout,
            )
            for collectible in with_images
        ]
        for index, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            results.append(result)
            if result.success:
                succeeded += 1
                logger.debug("Processed {}", result.image_name)
            else:
                failed += 1
                logger.warning("Failed {}", result.image_name)

            if index % 10 == 0 or index == len(with_images):
                logger.info("Progress: {}/{} processed", index, len(with_images))

    logger.info(
        "Image processing complete: {} successful, {} failed",
        succeeded,
        failed,
    )
    return results
