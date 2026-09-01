from io import BytesIO
from pathlib import Path

from PIL import Image

from cs_medal_parser.collectibles.collectible import Collectible
from cs_medal_parser.images.normalize import ImageSize
from cs_medal_parser.images.process import process_one


class _Response:
    def __init__(self, content: bytes) -> None:
        self.content = content

    def raise_for_status(self) -> None:
        return None


class _Session:
    def __init__(self, content: bytes) -> None:
        self.content = content
        self.calls = 0

    def get(self, url: str, timeout: int) -> _Response:
        self.calls += 1
        return _Response(self.content)


def _png_bytes(width: int = 40, height: int = 20) -> bytes:
    buffer = BytesIO()
    Image.new("RGB", (width, height), (200, 10, 10)).save(buffer, format="PNG")
    return buffer.getvalue()


def _collectible() -> Collectible:
    return Collectible.model_validate(
        {
            "id": "collectible-999",
            "name": "Test Medal",
            "image": "https://example.com/medal.png",
        }
    )


def test_process_one_downloads_and_caches(tmp_path: Path) -> None:
    session = _Session(_png_bytes())
    size = ImageSize(64, 48)
    collectible = _collectible()

    first = process_one(collectible, tmp_path, session, size=size, timeout=5)
    second = process_one(collectible, tmp_path, session, size=size, timeout=5)

    assert first.success
    assert second.success
    assert session.calls == 1
    with Image.open(tmp_path / "999.png") as image:
        assert image.size == (64, 48)


def test_process_one_resizes_stale_cache(tmp_path: Path) -> None:
    path = tmp_path / "999.png"
    Image.new("RGB", (16, 8), (0, 255, 0)).save(path)
    session = _Session(_png_bytes())

    result = process_one(
        _collectible(),
        tmp_path,
        session,
        size=ImageSize(64, 48),
        timeout=5,
    )

    assert result.success
    assert session.calls == 0
    with Image.open(path) as image:
        assert image.size == (64, 48)
