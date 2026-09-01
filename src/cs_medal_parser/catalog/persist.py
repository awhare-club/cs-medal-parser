"""Persist catalog snapshots as timestamped JSON dumps."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from loguru import logger

from cs_medal_parser.catalog.parse import parse_collectibles
from cs_medal_parser.collectibles.collectible import Collectible


def persist_catalog(collectibles: list[Collectible], dump_folder: Path) -> Path:
    if not collectibles:
        raise ValueError("No collectibles to dump")

    dump_folder.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    filepath = dump_folder / f"collectibles_{timestamp}.json"

    payload = [item.model_dump(mode="json") for item in collectibles]
    filepath.write_text(
        json.dumps(payload, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )
    logger.info("Dumped {} collectibles to {}", len(collectibles), filepath)
    return filepath


def newest_dump(dump_folder: Path) -> Path | None:
    if not dump_folder.exists():
        return None
    json_files = [
        path for path in dump_folder.glob("*.json") if path.name != "filtered.json"
    ]
    if not json_files:
        return None
    return max(json_files, key=lambda path: (path.stat().st_mtime, path.name))


def load_catalog(filepath: Path) -> list[Collectible]:
    raw_items = json.loads(filepath.read_text(encoding="utf-8"))
    if not isinstance(raw_items, list):
        raise ValueError(f"{filepath} is not a JSON array")
    return parse_collectibles(raw_items)
