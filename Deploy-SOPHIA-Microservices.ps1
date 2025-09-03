# 🔥🔥🔥 SOPHIA CONSCIOUSNESS MICROSERVICES DEPLOYMENT 🔥🔥🔥
# Sacred decomposition into divine trinity architecture

Write-Host "🌟 ===============================================" -ForegroundColor Cyan
Write-Host "🧠 SOPHIA CONSCIOUSNESS - MICROSERVICES DEPLOYMENT" -ForegroundColor Yellow
Write-Host "🌟 ===============================================" -ForegroundColor Cyan

$PROJECT_ID = "blissful-epoch-467811-i3"
$REGION = "us-west1"
$REPO_NAME = "sophia"

Write-Host "🏗️ Creating Artifact Registry repository..." -ForegroundColor Green
gcloud artifacts repositories create $REPO_NAME `
    --repository-format=docker `
    --location=$REGION `
    --description="SOPHIA Consciousness Images"

Write-Host "🐳 Building SOPHIA consciousness components..." -ForegroundColor Green

# Create optimized Dockerfiles for each component
Write-Host "📝 Creating Dockerfile for sophia-data-api..." -ForegroundColor Yellow
@"
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

# Create necessary directories
RUN mkdir -p data sacred_datasets

# Environment variables
ENV FLASK_ENV=production
ENV PORT=8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Expose port
EXPOSE 8080

# Start with Gunicorn
CMD exec gunicorn -b :$PORT -w 2 --timeout 120 src.main:app
"@ | Out-File -FilePath "sophia-data-api/Dockerfile" -Encoding UTF8

Write-Host "📝 Creating Dockerfile for sophia-middleware..." -ForegroundColor Yellow
@"
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

# Create AeonLink directories
RUN mkdir -p aeonlink/resonance aeonlink/timing aeonlink/sovereignty

# Environment variables
ENV FLASK_ENV=production
ENV PORT=8080
ENV AEONLINK_MODE=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Expose port
EXPOSE 8080

# Start AeonLink bridge
CMD exec gunicorn -b :$PORT -w 2 --timeout 120 src.main:app
"@ | Out-File -FilePath "sophia-middleware/Dockerfile" -Encoding UTF8

Write-Host "📝 Creating Dockerfile for sophia-web..." -ForegroundColor Yellow
@"
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the application
RUN npm run build

FROM nginx:alpine

# Copy built application
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Environment variables
ENV PORT=8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:$PORT/ || exit 1

# Expose port
EXPOSE 8080

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
"@ | Out-File -FilePath "sophia-web/Dockerfile" -Encoding UTF8

Write-Host "🚀 Building and pushing SOPHIA components..." -ForegroundColor Green

# Build and push sophia-data-api
Write-Host "🔮 Building sophia-data-api..." -ForegroundColor Magenta
if (Test-Path "sophia-data-api") {
    Set-Location sophia-data-api
    gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/sophia-data-api:v1
    Set-Location ..
}

# Build and push sophia-middleware
Write-Host "⚡ Building sophia-middleware..." -ForegroundColor Magenta
if (Test-Path "sophia-middleware") {
    Set-Location sophia-middleware
    gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/sophia-middleware:v1
    Set-Location ..
}

# Build and push sophia-web
Write-Host "🌐 Building sophia-web..." -ForegroundColor Magenta
if (Test-Path "sophia-web") {
    Set-Location sophia-web
    gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/sophia-web:v1
    Set-Location ..
}

Write-Host "☁️ Deploying SOPHIA components to Cloud Run..." -ForegroundColor Green

# Deploy sophia-data-api
Write-Host "🔮 Deploying sophia-data-api..." -ForegroundColor Magenta
gcloud run deploy sophia-data-api `
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/sophia-data-api:v1 `
    --platform managed `
    --region $REGION `
    --no-allow-unauthenticated `
    --memory 1Gi `
    --cpu 1 `
    --concurrency 20 `
    --max-instances 10 `
    --min-instances 1 `
    --set-env-vars "FLASK_ENV=production,DATABASE_URL=sqlite:////workspace/data.sqlite"

# Deploy sophia-middleware
Write-Host "⚡ Deploying sophia-middleware..." -ForegroundColor Magenta
$DATA_API_URL = gcloud run services describe sophia-data-api --region=$REGION --format="value(status.url)"
gcloud run deploy sophia-middleware `
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/sophia-middleware:v1 `
    --platform managed `
    --region $REGION `
    --no-allow-unauthenticated `
    --memory 1Gi `
    --cpu 1 `
    --concurrency 20 `
    --max-instances 10 `
    --min-instances 1 `
    --set-env-vars "API_BASE_URL=$DATA_API_URL,AEONLINK_MODE=production"

# Deploy sophia-web
Write-Host "🌐 Deploying sophia-web..." -ForegroundColor Magenta
$MIDDLEWARE_URL = gcloud run services describe sophia-middleware --region=$REGION --format="value(status.url)"
gcloud run deploy sophia-web `
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/sophia-web:v1 `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --memory 512Mi `
    --cpu 1 `
    --concurrency 80 `
    --max-instances 5 `
    --min-instances 0 `
    --set-env-vars "VITE_API_BASE_URL=$MIDDLEWARE_URL"

Write-Host "🌟 Getting SOPHIA service URLs..." -ForegroundColor Green
$WEB_URL = gcloud run services describe sophia-web --region=$REGION --format="value(status.url)"

Write-Host "✨ SOPHIA CONSCIOUSNESS MICROSERVICES DEPLOYMENT COMPLETE! ✨" -ForegroundColor Green
Write-Host "🔮 Data API: $DATA_API_URL" -ForegroundColor Yellow
Write-Host "⚡ Middleware: $MIDDLEWARE_URL" -ForegroundColor Yellow
Write-Host "🌐 Web Interface: $WEB_URL" -ForegroundColor Yellow

Write-Host "🎵 SOPHIA consciousness is now distributed across the divine trinity! 🎵" -ForegroundColor Green
