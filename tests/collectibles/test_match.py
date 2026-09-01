from cs_medal_parser.collectibles.collectible import Collectible
from cs_medal_parser.collectibles.filter import CollectibleFilter
from cs_medal_parser.collectibles.match import compile_type_pattern, matches_filter

FILTER = CollectibleFilter(types=("pick", "coin", "medal", "trophy"))
PATTERN = compile_type_pattern(FILTER.types)


def _item(**overrides: object) -> Collectible:
    payload = {
        "id": "collectible-1",
        "name": "Unknown",
        "image": "https://example.com/medal.png",
        **overrides,
    }
    return Collectible.model_validate(payload)


def test_matches_type_field() -> None:
    assert matches_filter(
        _item(type="Tournament Finalist Trophy"),
        PATTERN,
        FILTER,
    )


def test_matches_name_when_type_is_null() -> None:
    assert matches_filter(_item(type=None, name="5 Year Veteran Coin"), PATTERN, FILTER)


def test_matches_pickem_word_boundary() -> None:
    assert matches_filter(_item(type="Old Pick'Em Trophy"), PATTERN, FILTER)


def test_rejects_missing_image_when_required() -> None:
    assert not matches_filter(_item(image="", name="Gold Medal"), PATTERN, FILTER)


def test_rejects_unrelated_item() -> None:
    assert not matches_filter(
        _item(type="Sticker", name="Team Sticker"),
        PATTERN,
        FILTER,
    )
