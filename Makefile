.PHONY: all lint test

all: lint

lint:
	uv run ruff format
	uv run ruff check src
	uv run mypy src

test:
	uv run pytest
