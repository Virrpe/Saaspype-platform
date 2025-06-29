# SaaSpype Discovery Engine 2.1 - Optimized Multi-stage Docker Build
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app/src:/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with timeout and retries
RUN pip install --no-cache-dir --timeout=300 --retries=3 -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories with proper permissions
RUN mkdir -p logs working-memory data/logs data/backups src/shared/config && \
    chmod -R 755 logs working-memory data && \
    chmod +x start_api_v2.py

# Initialize working memory if not exists
RUN if [ ! -f working-memory/current-context.json ]; then \
        echo '{"session_metadata":{"system_status":"docker_container","autonomous_mode":true},"project_state":{"current_phase":"PRODUCTION_DOCKER_DEPLOYMENT","completion_percentage":100}}' > working-memory/current-context.json; \
    fi

# Set environment variables for Docker
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV FRONTEND_HOST=0.0.0.0
ENV FRONTEND_PORT=3000
ENV DATABASE_PATH=/app/saaspype_discovery.db
ENV SECRET_KEY=saaspype-docker-secret-key-2025-secure
ENV LOG_LEVEL=INFO
ENV CORS_ORIGINS=*
ENV DOCKER_DEPLOYMENT=true

# Expose ports
EXPOSE 8000 3000

# Health check for the API
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command - start the API server
CMD ["python", "start_api_v2.py"] 