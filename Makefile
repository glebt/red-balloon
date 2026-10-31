.PHONY: help install install-dev test test-cov lint format type-check run clean

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -e ".[dev]"

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage report
	pytest --cov=red_balloon --cov-report=html --cov-report=term

lint:  ## Run linting checks
	ruff check src tests

format:  ## Format code with ruff
	ruff format src tests
	ruff check --fix src tests

type-check:  ## Run type checking with mypy
	mypy src

run:  ## Run the development server
	python -m red_balloon.main

clean:  ## Clean up generated files
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
