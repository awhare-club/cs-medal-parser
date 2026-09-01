from io import BytesIO

from PIL import Image

from cs_medal_parser.images.normalize import ImageSize, normalize, normalize_bytes


def test_normalize_pads_to_target_canvas() -> None:
    source = Image.new("RGBA", (100, 50), (255, 0, 0, 255))
    size = ImageSize(width=256, height=192)

    result = normalize(source, size)

    assert result.size == (256, 192)
    assert result.mode == "RGBA"
    assert result.getpixel((0, 0)) == (0, 0, 0, 0)
    assert result.getpixel((128, 96))[0] == 255


def test_normalize_bytes_roundtrip() -> None:
    buffer = BytesIO()
    Image.new("RGB", (40, 40), (0, 128, 255)).save(buffer, format="PNG")

    result = normalize_bytes(buffer.getvalue(), ImageSize(64, 64))

    assert result.size == (64, 64)
    assert result.mode == "RGBA"
