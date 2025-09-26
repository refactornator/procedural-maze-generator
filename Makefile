# Makefile for Procedural Maze Generator

.PHONY: help install install-dev test test-coverage lint format clean build upload docs

# Default target
help:
	@echo "Available targets:"
	@echo "  install      - Install the package"
	@echo "  install-dev  - Install in development mode with dev dependencies"
	@echo "  test         - Run tests"
	@echo "  test-coverage- Run tests with coverage report"
	@echo "  lint         - Run linting (flake8, mypy)"
	@echo "  format       - Format code with black"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build distribution packages"
	@echo "  upload       - Upload to PyPI (requires credentials)"
	@echo "  docs         - Generate documentation"
	@echo "  demo         - Run demo examples"

# Installation
install:
	pip install .

install-dev:
	pip install -e ".[dev]"

# Testing
test:
	pytest tests/ -v

test-coverage:
	pytest tests/ --cov=maze_generator --cov-report=html --cov-report=term-missing

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

# Code quality
lint:
	flake8 src/maze_generator tests examples
	mypy src/maze_generator

format:
	black src/maze_generator tests examples

format-check:
	black --check src/maze_generator tests examples

# Build and distribution
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

upload: build
	python -m twine upload dist/*

upload-test: build
	python -m twine upload --repository testpypi dist/*

# Documentation
docs:
	@echo "Documentation is in README.md and examples/"
	@echo "API documentation can be generated with sphinx if needed"

# Demo and examples
demo:
	python examples/basic_usage.py

benchmark:
	python examples/performance_comparison.py

# Development helpers
setup-dev: install-dev
	pre-commit install

check-all: format-check lint test

# CI/CD helpers
ci-test: install-dev test-coverage lint

# Release helpers
version-patch:
	bump2version patch

version-minor:
	bump2version minor

version-major:
	bump2version major

# Docker (if needed)
docker-build:
	docker build -t maze-generator .

docker-run:
	docker run -it --rm maze-generator

# Jupyter notebook setup (if examples use notebooks)
jupyter-setup:
	pip install jupyter
	jupyter notebook --generate-config

# Performance profiling
profile:
	python -m cProfile -o profile.stats examples/performance_comparison.py
	python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(20)"

# Security check
security-check:
	pip install safety bandit
	safety check
	bandit -r src/maze_generator/
