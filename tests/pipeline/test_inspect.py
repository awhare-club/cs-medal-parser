from pathlib import Path

from cs_medal_parser.catalog.persist import persist_catalog
from cs_medal_parser.collectibles.collectible import Collectible
from cs_medal_parser.pipeline.inspect import inspect_latest_dump
from cs_medal_parser.pipeline.settings import Settings


def test_inspect_writes_filtered_dump(tmp_path: Path) -> None:
    persist_catalog(
        [
            Collectible.model_validate(
                {
                    "id": "collectible-1",
                    "name": "Gold Medal",
                    "image": "https://example.com/medal.png",
                }
            ),
            Collectible.model_validate(
                {
                    "id": "collectible-2",
                    "name": "Team Sticker",
                    "image": "https://example.com/sticker.png",
                }
            ),
        ],
        tmp_path,
    )

    settings = Settings(dump_folder=tmp_path, collectible_types=("medal",))
    assert inspect_latest_dump(settings) is True
    assert (tmp_path / "filtered.json").exists()
    assert "collectible-1" in (tmp_path / "filtered.json").read_text(encoding="utf-8")
