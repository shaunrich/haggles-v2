# Hagglz Negotiation Agent - Docker Configuration
# Multi-stage build for optimised production deployment

# Build stage
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Production stage
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app/src:$PYTHONPATH"

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Create app user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create application directory
WORKDIR /app

# Create data directory for persistence
RUN mkdir -p /app/data && \
    chown -R appuser:appuser /app

# Copy application code
COPY --chown=appuser:appuser . .

# Create necessary directories
RUN mkdir -p /app/chroma_db && \
    mkdir -p /app/logs && \
    chown -R appuser:appuser /app/chroma_db /app/logs

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command - Updated to use correct import path
CMD ["python", "-m", "uvicorn", "hagglz.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

# Labels for metadata
LABEL maintainer="Hagglz Team" \
      version="1.0.0" \
      description="Hagglz AI Negotiation Agent System" \
      org.opencontainers.image.title="Hagglz Negotiation Agent" \
      org.opencontainers.image.description="AI-powered bill negotiation system with specialised agents" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.vendor="Hagglz" \
      org.opencontainers.image.licenses="MIT"

