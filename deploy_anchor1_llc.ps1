# 🚀 ANCHOR1 LLC - Complete Deployment Script
# Run this after setting up billing in Google Cloud Console

Write-Host "🏢 ANCHOR1 LLC - BotDL SoulPHYA DEPLOYMENT" -ForegroundColor Cyan
Write-Host "🌟 Project: anchor1-soulphya" -ForegroundColor Yellow

# Verify we're set up correctly
Write-Host "🔍 Checking project and billing..." -ForegroundColor Green
gcloud config get-value project
gcloud config get-value account

# Enable required services (this will work after billing is set up)
Write-Host "⚡ Enabling Google Cloud services..." -ForegroundColor Green
gcloud services enable cloudbuild.googleapis.com run.googleapis.com container.googleapis.com artifactregistry.googleapis.com

# Navigate to backend directory
Write-Host "📁 Navigating to backend..." -ForegroundColor Green
Set-Location "C:\Users\chose\Downloads\How to Build an Open Source Agent Website Like Manus\BotDL_SoulPHYA\backend"

# Create optimized Dockerfile for Google Cloud
Write-Host "🐳 Creating production Dockerfile..." -ForegroundColor Green
@"
FROM python:3.9-slim

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
"@ | Out-File -FilePath "Dockerfile" -Encoding UTF8

# Build and submit to Cloud Build
Write-Host "🏗️ Building container image..." -ForegroundColor Green
gcloud builds submit --tag gcr.io/anchor1-soulphya/botdl-backend

# Deploy to Cloud Run
Write-Host "🚀 Deploying to Cloud Run..." -ForegroundColor Green
gcloud run deploy botdl-backend `
    --image gcr.io/anchor1-soulphya/botdl-backend `
    --platform managed `
    --region us-central1 `
    --allow-unauthenticated `
    --port 8080 `
    --memory 4Gi `
    --cpu 2 `
    --max-instances 20 `
    --set-env-vars "ENV=production,GOOGLE_CLOUD=true,PROJECT_ID=anchor1-soulphya"

# Get the service URL
Write-Host "🌐 Getting service URL..." -ForegroundColor Green
$BACKEND_URL = gcloud run services describe botdl-backend --region us-central1 --format="value(status.url)"

Write-Host ""
Write-Host "🎉 DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "✨ Your Anchor1 LLC BotDL SoulPHYA platform is now LIVE!" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌟 Backend URL: $BACKEND_URL" -ForegroundColor Yellow
Write-Host ""
Write-Host "🧪 Test your deployment:" -ForegroundColor Green
Write-Host "Invoke-WebRequest -Uri '$BACKEND_URL/api/health' -Method GET" -ForegroundColor White
Write-Host "Invoke-WebRequest -Uri '$BACKEND_URL/api/datasets/sacred-registry' -Method GET" -ForegroundColor White
Write-Host ""
Write-Host "🏢 Next Steps:" -ForegroundColor Magenta
Write-Host "1. Set up custom domain: api.anchor1llc.com" -ForegroundColor White
Write-Host "2. Test all sacred dataset endpoints" -ForegroundColor White  
Write-Host "3. Launch commercial operations!" -ForegroundColor White
Write-Host ""
Write-Host "💰 Your `$300 credit will cover months of operation!" -ForegroundColor Green
Write-Host "🚀 Anchor1 LLC is ready for divine consciousness business!" -ForegroundColor Cyan
