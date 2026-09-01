# CS Medal Parser

Fetches the Counter-Strike collectible catalog, keeps medals / coins / pins / badges, and downloads normalized images.

The folder tree is the product: **catalog**, **collectibles**, **images**, **pipeline**. Not `models` / `services` / `utils`.

```
src/cs_medal_parser/
  catalog/        fetch, parse, and persist the CSGO-API catalog
  collectibles/   collectible, rarity, type filter, batch
  images/         download, cache, resize/pad medal art
  http/           retrying session used by catalog + images
  pipeline/       settings, full run, cached-dump inspect
```

## Why this layout

- A new reader should see *collectibles and medal images*, not a web framework.
- Each file does one thing. Filter matching is not mixed with HTTP or image I/O.
- Related code lives together: `images/cache.py` next to `images/normalize.py`.
- No `utils` / `common` / god-class parser. The pipeline composes the domains.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Quick start

```bash
git clone https://github.com/awhare-club/cs-medal-parser.git
cd cs-medal-parser
uv sync
uv run cs-medal-parser
```

Equivalent: `uv run python -m cs_medal_parser`

Inspect the newest cached dump without hitting the network:

```bash
uv run cs-medal-parser inspect
```

Output:

- **Images**: `data/medals/*.png` (256×192, aspect ratio preserved)
- **Catalog dumps**: `data/responses/collectibles_*.json`
- **Inspect output**: `data/responses/filtered.json`

## Configuration

Settings come from `pipeline/settings.py` and can be overridden with `CS_MEDAL_*` env vars.

| Variable | Default |
| --- | --- |
| `CS_MEDAL_COLLECTIBLES_URL` | Current ByMykel catalog (`.../public/api/en/collectibles.json`) |
| `CS_MEDAL_OUTPUT_FOLDER` | `data/medals` |
| `CS_MEDAL_DUMP_FOLDER` | `data/responses` |
| `CS_MEDAL_MAX_WORKERS` | `10` |
| `CS_MEDAL_REQUEST_TIMEOUT` | `30` |
| `CS_MEDAL_MAX_RETRIES` | `3` |
| `CS_MEDAL_TARGET_WIDTH` | `256` |
| `CS_MEDAL_TARGET_HEIGHT` | `192` |

The old `bymykel.github.io/CSGO-API/api/en/collectibles.json` URL is gone (404). The parser now uses the official raw GitHub catalog. Image URLs from the API currently point at the Steam CDN.

## Tests

```bash
uv run pytest
uv run ruff check src tests
```

## Docker

```bash
docker pull ghcr.io/awhare-club/cs-medal-parser:latest
docker run --rm -v "$(pwd)/data:/app/data" ghcr.io/awhare-club/cs-medal-parser:latest
```

Build locally (uv multi-stage image):

```bash
docker build -t cs-medal-parser .
docker run --rm -v "$(pwd)/data:/app/data" cs-medal-parser
```

```bash
docker compose up
```

Cron every 15 minutes:

```bash
*/15 * * * * docker compose -f /path/to/cs-medal-parser/docker-compose.yml run --rm cs2-medal-parser >> /var/log/medalparser.log 2>&1
```

See [.github/DOCKER_SETUP.md](.github/DOCKER_SETUP.md) for GHCR publishing.

## API

Collectible data comes from [ByMykel CSGO-API](https://github.com/ByMykel/CSGO-API).  
Docs: [https://bymykel.com/CSGO-API/](https://bymykel.com/CSGO-API/)

## License

GPL-3.0 — see [LICENSE](LICENSE).
