# Build stage: use standard python image and copy uv binaries
FROM python:3.11-slim AS builder

# Copy uv and uvx from the official distroless image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy only the files needed for dependency resolution
COPY pyproject.toml uv.lock ./

# Install dependencies into a standalone virtual environment
# --frozen ensures we use the exact versions from uv.lock
# --no-dev excludes development dependencies
RUN uv sync --frozen --no-install-project --no-dev

# Final stage: use a slim python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Ensure the app uses the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application source code
# Note: This expects the build context to be the project root
COPY src /app/src
COPY resources /app/resources

# Change ownership to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose the application port
EXPOSE 5000

# Command to run the application
# We use the full path to uvicorn inside the venv to be safe
CMD ["uvicorn", "elai_intent_engine.main:app", "--host", "0.0.0.0", "--port", "5000"]