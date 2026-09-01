"""Fetch the collectible catalog from the CSGO API."""

from __future__ import annotations

import requests
from loguru import logger

from cs_medal_parser.catalog.parse import parse_collectibles
from cs_medal_parser.collectibles.collectible import Collectible
from cs_medal_parser.http.get import get_json


def fetch_catalog(
    session: requests.Session,
    url: str,
    *,
    timeout: int,
) -> list[Collectible]:
    logger.info("Fetching collectibles from {}", url)
    raw_items = get_json(session, url, timeout=timeout)
    if not isinstance(raw_items, list):
        raise ValueError("Catalog response must be a JSON array")

    logger.info("Fetched {} raw collectibles", len(raw_items))
    collectibles = parse_collectibles(raw_items)
    logger.info("Parsed {} collectibles", len(collectibles))
    return collectibles
