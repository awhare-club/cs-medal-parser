from cs_medal_parser.collectibles.collectible import Collectible


def test_parses_current_catalog_shape() -> None:
    collectible = Collectible.model_validate(
        {
            "id": "collectible-874",
            "name": "5 Year Veteran Coin",
            "description": "Has been a member of the Counter-Strike community.",
            "def_index": "874",
            "rarity": {
                "id": "rarity_ancient",
                "name": "Extraordinary",
                "color": "#eb4b4b",
            },
            "type": None,
            "genuine": False,
            "market_hash_name": None,
            "image": "https://community.akamai.steamstatic.com/economy/image/example",
            "original": {"item_name": "#CSGO_CollectibleCoin_FiveYearService"},
        }
    )

    assert collectible.image_stem == "874"
    assert collectible.rarity is not None
    assert collectible.rarity.name == "Extraordinary"
    assert collectible.image is not None


def test_empty_image_becomes_none() -> None:
    collectible = Collectible.model_validate({"id": "collectible-1", "image": ""})
    assert collectible.image is None


def test_rejects_blank_id() -> None:
    try:
        Collectible.model_validate({"id": "   "})
    except Exception as exc:
        assert "empty" in str(exc).lower()
    else:
        raise AssertionError("blank id should fail validation")
