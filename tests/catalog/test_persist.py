from pathlib import Path

from cs_medal_parser.catalog.persist import load_catalog, newest_dump, persist_catalog
from cs_medal_parser.collectibles.collectible import Collectible


def test_persist_and_reload_roundtrip(tmp_path: Path) -> None:
    collectible = Collectible.model_validate(
        {
            "id": "collectible-874",
            "name": "5 Year Veteran Coin",
            "image": "https://example.com/coin.png",
            "rarity": {"id": "rarity_ancient", "name": "Extraordinary"},
        }
    )

    path = persist_catalog([collectible], tmp_path)
    loaded = load_catalog(path)

    assert path.name.startswith("collectibles_")
    assert len(loaded) == 1
    assert loaded[0].id == "collectible-874"
    assert loaded[0].rarity is not None
    assert loaded[0].rarity.name == "Extraordinary"


def test_newest_dump_ignores_filtered_json(tmp_path: Path) -> None:
    older = tmp_path / "collectibles_01_01_2020_00_00_00.json"
    newer = tmp_path / "collectibles_01_01_2024_00_00_00.json"
    older.write_text("[]", encoding="utf-8")
    newer.write_text("[]", encoding="utf-8")
    older.touch()
    newer.touch()
    (tmp_path / "filtered.json").write_text("[]", encoding="utf-8")

    assert newest_dump(tmp_path) == newer
