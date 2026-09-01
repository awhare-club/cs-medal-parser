from pathlib import Path

from PIL import Image

from cs_medal_parser.images.cache import is_cached, renormalize_existing
from cs_medal_parser.images.normalize import ImageSize


def test_is_cached_when_dimensions_match(tmp_path: Path) -> None:
    path = tmp_path / "medal.png"
    Image.new("RGBA", (256, 192)).save(path)
    assert is_cached(path, ImageSize(256, 192))
    assert not is_cached(path, ImageSize(128, 96))


def test_renormalize_existing_wrong_size(tmp_path: Path) -> None:
    path = tmp_path / "medal.png"
    Image.new("RGB", (32, 16), (10, 20, 30)).save(path)

    assert renormalize_existing(path, ImageSize(64, 48))
    with Image.open(path) as image:
        assert image.size == (64, 48)
