from cs_medal_parser.collectibles.batch import filter_collectibles
from cs_medal_parser.collectibles.collectible import Collectible
from cs_medal_parser.collectibles.filter import CollectibleFilter


def test_filter_returns_immutable_batch() -> None:
    items = [
        Collectible.model_validate(
            {
                "id": "collectible-1",
                "name": "Gold Medal",
                "image": "https://example.com/a.png",
            }
        ),
        Collectible.model_validate(
            {
                "id": "collectible-2",
                "name": "Team Sticker",
                "image": "https://example.com/b.png",
            }
        ),
        Collectible.model_validate({"id": "collectible-3", "name": "Silver Coin"}),
    ]

    batch = filter_collectibles(
        items,
        CollectibleFilter(types=("medal", "coin"), require_image=True),
    )

    assert batch.total_count == 3
    assert batch.filtered_count == 1
    assert batch.items[0].id == "collectible-1"


def test_empty_input_is_empty_batch() -> None:
    batch = filter_collectibles([], CollectibleFilter(types=("medal",)))
    assert batch.total_count == 0
    assert batch.filtered_count == 0
