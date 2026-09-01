"""GET helpers on top of a shared session."""

from __future__ import annotations

from typing import Any

import requests
from loguru import logger


def get_json(session: requests.Session, url: str, *, timeout: int) -> Any:
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()


def get_bytes(session: requests.Session, url: str, *, timeout: int) -> bytes | None:
    try:
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
        return response.content
    except requests.RequestException as exc:
        logger.error("Network error downloading {}: {}", url, exc)
        return None
