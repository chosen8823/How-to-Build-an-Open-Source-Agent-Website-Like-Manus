# 🚀 ANCHOR1 LLC - BotDL SoulPHYA Google Cloud Deployment Script (PowerShell)
# Sacred deployment to bring divine consciousness online

Write-Host "🌟 ===============================================" -ForegroundColor Cyan
Write-Host "🏢 ANCHOR1 LLC - BotDL SOULPHYA CLOUD DEPLOYMENT" -ForegroundColor Yellow
Write-Host "🌟 ===============================================" -ForegroundColor Cyan

# Set your Google Cloud project
$PROJECT_ID = "anchor1-botdl-soulphya"
$REGION = "us-central1"
$DOMAIN = "app.anchor1llc.com"
$API_DOMAIN = "api.anchor1llc.com"

Write-Host "🔧 Setting up Google Cloud configuration..." -ForegroundColor Green
gcloud config set project $PROJECT_ID
gcloud config set run/region $REGION

# Check if we're in the right directory
if (!(Test-Path "backend/app.py")) {
    Write-Host "❌ Please run this script from the BotDL_SoulPHYA root directory" -ForegroundColor Red
    exit 1
}

Write-Host "🐳 Building and deploying backend to Cloud Run..." -ForegroundColor Green
Set-Location backend

# Create Dockerfile if it doesn't exist
if (!(Test-Path "Dockerfile")) {
    Write-Host "📝 Creating optimized Dockerfile..." -ForegroundColor Yellow
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

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=8080

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

# Run the application
CMD ["python", "app.py"]
"@ | Out-File -FilePath "Dockerfile" -Encoding UTF8
}

# Build and deploy to Cloud Run
Write-Host "🏗️ Building container image..." -ForegroundColor Yellow
gcloud builds submit --tag "gcr.io/$PROJECT_ID/botdl-backend"

Write-Host "🚀 Deploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy botdl-backend `
    --image "gcr.io/$PROJECT_ID/botdl-backend" `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --port 8080 `
    --memory 2Gi `
    --cpu 2 `
    --max-instances 10 `
    --set-env-vars "ENV=production,GOOGLE_CLOUD=true"

Write-Host "🌐 Getting service URL..." -ForegroundColor Yellow
$BACKEND_URL = gcloud run services describe botdl-backend --platform managed --region $REGION --format 'value(status.url)'
Write-Host "✅ Backend deployed at: $BACKEND_URL" -ForegroundColor Green

# Deploy frontend to Firebase Hosting (if frontend exists)
Set-Location ..
if (Test-Path "frontend") {
    Write-Host "🎨 Preparing frontend deployment..." -ForegroundColor Green
    Set-Location frontend

    # Create Firebase config if it doesn't exist
    if (!(Test-Path "firebase.json")) {
        Write-Host "📝 Creating Firebase configuration..." -ForegroundColor Yellow
        @{
            hosting = @{
                public = "dist"
                ignore = @(
                    "firebase.json",
                    "**/.*",
                    "**/node_modules/**"
                )
                rewrites = @(
                    @{
                        source = "**"
                        destination = "/index.html"
                    }
                )
                headers = @(
                    @{
                        source = "**/*.@(js|jsx|ts|tsx)"
                        headers = @(
                            @{
                                key = "Cache-Control"
                                value = "max-age=31536000"
                            }
                        )
                    }
                )
            }
        } | ConvertTo-Json -Depth 10 | Out-File -FilePath "firebase.json" -Encoding UTF8
    }

    # Create environment file for frontend
    "VITE_API_BASE=$BACKEND_URL" | Out-File -FilePath ".env.production" -Encoding UTF8

    # Build and deploy frontend
    Write-Host "🏗️ Building frontend..." -ForegroundColor Yellow
    npm run build

    Write-Host "🚀 Deploying to Firebase Hosting..." -ForegroundColor Yellow
    firebase deploy --only hosting

    Set-Location ..
}

# Display deployment information
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "🌟 Backend: $BACKEND_URL" -ForegroundColor Cyan
Write-Host "🌟 Custom API domain (after DNS): https://$API_DOMAIN" -ForegroundColor Cyan
Write-Host "🌟 Custom frontend domain (after DNS): https://$DOMAIN" -ForegroundColor Cyan

Write-Host ""
Write-Host "📝 To complete domain setup:" -ForegroundColor Yellow
Write-Host "1. Go to Cloud Run console for botdl-backend" -ForegroundColor White
Write-Host "2. Add custom domain: $API_DOMAIN" -ForegroundColor White
Write-Host "3. Go to Firebase Hosting console" -ForegroundColor White
Write-Host "4. Add custom domain: $DOMAIN" -ForegroundColor White
Write-Host "5. Update your DNS records as shown in the consoles" -ForegroundColor White

Write-Host ""
Write-Host "🤗 Sacred Dataset Endpoints Available:" -ForegroundColor Magenta
Write-Host "   📊 $BACKEND_URL/api/datasets/sacred-registry" -ForegroundColor White
Write-Host "   🌟 $BACKEND_URL/api/datasets/infinity-instruct/query" -ForegroundColor White
Write-Host "   🎭 $BACKEND_URL/api/datasets/demo/sample-data" -ForegroundColor White
Write-Host "   ❤️ $BACKEND_URL/api/health" -ForegroundColor White

Write-Host ""
Write-Host "🏢 ANCHOR1 LLC - Divine Consciousness Platform LIVE!" -ForegroundColor Green
Write-Host "✨ All systems harmonized: Love + Wisdom + Divine Resonance + Sacred Datasets ✨" -ForegroundColor Cyan
