.PHONY: clean install install-dev build lint test help

help:
	@echo "Available commands:"
	@echo "  make clean      - Remove build, test, coverage, and Python artifacts"
	@echo "  make install    - Install package in production mode"
	@echo "  make install-dev- Install package in development mode with dev dependencies"
	@echo "  make build      - Build package distribution"
	@echo "  make lint       - Check style with flake8"
	@echo "  make test       - Run tests with pytest"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .tox/
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

install:
	pip install .

install-dev:
	pip install -e ".[dev]"
	pip install pytest flake8 build

build:
	python -m build

lint:
	flake8 src/ragazza

test:
	pytest tests/
