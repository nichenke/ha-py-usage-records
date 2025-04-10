# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	POETRY_VERSION=1.7.1 \
	POETRY_NO_INTERACTION=1 \
	POETRY_VIRTUALENVS_CREATE=false

# Install poetry and dependencies
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Copy pyproject.toml and poetry.lock (if exists)
COPY pyproject.toml ./
# Copy the rest of the application
COPY . .

# Install dependencies
RUN poetry install --no-dev

# Create records directory and set permissions
RUN mkdir -p /app/records && chmod 777 /app/records

# Define a volume for persistent storage of records
VOLUME ["/app/records"]

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["uvicorn", "ha_usage_records.main:app", "--host", "0.0.0.0", "--port", "8080"]