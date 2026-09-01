# GHCR publishing

Images are published to GitHub Container Registry. No Docker Hub account or extra secrets.

Image: `ghcr.io/awhare-club/cs-medal-parser`

## What the workflow does

- **Push**: build `linux/amd64` + `linux/arm64` and push with branch / semver / `latest` (default branch only) tags
- **Pull request to main**: build only (no login, no push)
- Auth is `GITHUB_TOKEN` with `packages: write`

The first successful push creates the package. If the repo is public and you want anonymous pulls, set the package visibility to **Public** under **Packages** → `cs-medal-parser` → **Package settings**.

## Pull and run

```bash
docker pull ghcr.io/awhare-club/cs-medal-parser:latest
docker run --rm -v "$(pwd)/data:/app/data" ghcr.io/awhare-club/cs-medal-parser:latest
```

Private package:

```bash
echo "$GITHUB_TOKEN" | docker login ghcr.io -u USERNAME --password-stdin
docker pull ghcr.io/awhare-club/cs-medal-parser:latest
```

## Tags

- `ghcr.io/awhare-club/cs-medal-parser:latest` — default branch only
- `ghcr.io/awhare-club/cs-medal-parser:main`
- `ghcr.io/awhare-club/cs-medal-parser:<branch>`
- `ghcr.io/awhare-club/cs-medal-parser:1.2.3` — when the commit is tagged
