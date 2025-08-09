FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy lean requirements for production
COPY requirements_lean.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p ai_engine/divine_resonance ai_engine/love_wisdom ai_engine/consciousness ai_engine/orchestrator

# Set environment variables for Google Cloud
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=8080
ENV GOOGLE_CLOUD=true

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

# Run the application
CMD ["python", "app.py"]
