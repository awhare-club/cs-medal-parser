"""Resize a medal image and pad it to a fixed canvas."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

from PIL import Image


@dataclass(frozen=True, slots=True)
class ImageSize:
    width: int = 256
    height: int = 192

    @property
    def as_tuple(self) -> tuple[int, int]:
        return (self.width, self.height)


def normalize(image: Image.Image, size: ImageSize) -> Image.Image:
    resized = image.copy()
    if resized.mode != "RGBA":
        resized = resized.convert("RGBA")
    resized.thumbnail(size.as_tuple, Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", size.as_tuple, (0, 0, 0, 0))
    left = (size.width - resized.width) // 2
    top = (size.height - resized.height) // 2
    canvas.paste(resized, (left, top))
    return canvas


def normalize_bytes(data: bytes, size: ImageSize) -> Image.Image:
    with Image.open(BytesIO(data)) as image:
        image.load()
        return normalize(image, size)
