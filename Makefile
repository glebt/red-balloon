.PHONY: help test test-cov lint format type-check serve clean

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

test:  ## Run tests
	uv run pytest

test-cov:  ## Run tests with coverage report
	uv run pytest --cov=red_balloon --cov-report=html --cov-report=term

lint:  ## Run linting checks
	uv run ruff check src tests

format:  ## Format code with ruff
	uv run ruff format src tests
	uv run ruff check --fix src tests

type-check:  ## Run type checking with mypy
	uv run mypy src

serve:  ## Run the development server
	uv run python -m red_balloon.main

clean:  ## Clean up generated files
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
