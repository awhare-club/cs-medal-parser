# syntax=docker/dockerfile:1
FROM python:3.13-alpine AS builder

COPY --from=ghcr.io/astral-sh/uv:0.12.8 /uv /uvx /bin/

RUN apk add --no-cache \
    gcc \
    musl-dev \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev --no-editable

COPY README.md pyproject.toml uv.lock ./
COPY src ./src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

FROM python:3.13-alpine

RUN apk add --no-cache \
    jpeg \
    zlib \
    freetype \
    lcms2 \
    openjpeg \
    tiff \
    && addgroup -g 1000 appgroup \
    && adduser -u 1000 -G appgroup -s /bin/sh -D appuser

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

RUN mkdir -p data/medals data/responses \
    && chown -R appuser:appgroup /app

ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1

USER appuser

CMD ["cs-medal-parser"]
