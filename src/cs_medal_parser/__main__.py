"""CLI entry for the CS medal parser."""

from __future__ import annotations

import argparse
import sys

from loguru import logger

from cs_medal_parser.pipeline.inspect import inspect_latest_dump
from cs_medal_parser.pipeline.run import run


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cs-medal-parser",
        description="Fetch, filter, and download Counter-Strike collectible medals.",
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["inspect"],
        help="Optional: inspect the newest cached catalog dump instead of fetching.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    try:
        ok = inspect_latest_dump() if args.command == "inspect" else run()
        return 0 if ok else 1
    except KeyboardInterrupt:
        logger.warning("Cancelled")
        return 1
    except Exception as exc:
        logger.exception("Unexpected error: {}", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
