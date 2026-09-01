"""Outcome of processing one collectible image."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProcessingResult:
    collectible_id: str
    image_name: str
    success: bool
    error_message: str | None = None
    file_path: str | None = None
