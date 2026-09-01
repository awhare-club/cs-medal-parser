"""Reuse already-normalized medal images when the canvas size matches."""

from __future__ import annotations

from pathlib import Path

from loguru import logger
from PIL import Image

from cs_medal_parser.images.normalize import ImageSize, normalize


def is_cached(path: Path, size: ImageSize) -> bool:
    if not path.exists():
        return False
    try:
        with Image.open(path) as image:
            return image.size == size.as_tuple
    except Exception:
        return False


def renormalize_existing(path: Path, size: ImageSize) -> bool:
    try:
        with Image.open(path) as image:
            image.load()
            processed = normalize(image, size)
        processed.save(path, "PNG", optimize=True)
        logger.info("Resized existing image {}", path.name)
        return True
    except Exception as exc:
        logger.warning("Image {} corrupted, re-downloading: {}", path.name, exc)
        return False
