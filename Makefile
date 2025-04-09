.PHONY: test lint format check clean

# Default target
all: lint test

# Run tests
test:
	python -m pytest tests/ -v

# Run linting checks
lint:
	python -m black --check ha_usage_records/ tests/

# Format code
format:
	python -m black ha_usage_records/ tests/

# Type checking (install mypy first)
check:
	@echo "Type checking not configured yet. To enable:"
	@echo "1. Add 'mypy' to your dev dependencies"
	@echo "2. Run 'python -m mypy ha_usage_records tests'

# Clean up cache files
clean:
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf */*/__pycache__
	rm -rf .mypy_cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

# Run a local development server
serve:
	python -m uvicorn ha_usage_records.main:app --reload