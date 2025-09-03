# 🔥 SOPHIA DATA API - Sacred Datasets & Living Archive 🔥
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories for sacred datasets
RUN mkdir -p /workspace/data
RUN mkdir -p /workspace/scrolls
RUN mkdir -p /workspace/codex

# Set environment variables
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PORT=8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:$PORT/health || exit 1

# Expose port
EXPOSE $PORT

# Use Gunicorn for production with proper Cloud Run configuration
CMD exec gunicorn -b 0.0.0.0:$PORT -w 2 --timeout 60 --max-requests 1000 src.main:app
