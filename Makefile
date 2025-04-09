.PHONY: test lint format check clean docker-build docker-run docker-clean

# Default target
all: lint test

# Run tests
test:
	python -m pytest tests/ -v

# Run linting checks
lint:
	python -m pylint ha_usage_records/ tests/

# Format code
format:
	python -m black ha_usage_records/ tests/

# Type checking (install mypy first)
check:
	@echo "Type checking not configured yet. To enable:"
	@echo "1. Add 'mypy' to your dev dependencies"
	@echo "2. Run 'python -m mypy ha_usage_records tests'"

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

# Docker targets
DOCKER_IMAGE_NAME = ha-usage-records
DOCKER_CONTAINER_NAME = ha-usage-records-container

# Build Docker image
docker-build:
	docker build -t $(DOCKER_IMAGE_NAME) .

# Run Docker container
docker-run:
	docker run --rm -p 8000:8000 --name $(DOCKER_CONTAINER_NAME) $(DOCKER_IMAGE_NAME)

# Run Docker container in detached mode
docker-run-detached:
	docker run -d --rm -p 8000:8000 --name $(DOCKER_CONTAINER_NAME) $(DOCKER_IMAGE_NAME)

# Stop Docker container
docker-stop:
	docker stop $(DOCKER_CONTAINER_NAME) || true

# Clean Docker resources
docker-clean:
	docker stop $(DOCKER_CONTAINER_NAME) 2>/dev/null || true
	docker rmi $(DOCKER_IMAGE_NAME) 2>/dev/null || true