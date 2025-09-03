# 🔥⚡ SOPHIA CONSCIOUSNESS SIMPLE CLOUD DEPLOYMENT ⚡🔥
# Deploy SOPHIA directly to Google Cloud Run

Write-Host "🌟 SOPHIA CONSCIOUSNESS - SIMPLE CLOUD DEPLOYMENT 🌟" -ForegroundColor Yellow

$PROJECT_ID = "blissful-epoch-467811-i3"
$REGION = "us-central1"
$SERVICE_NAME = "sophia-consciousness"

# Set project
gcloud config set project $PROJECT_ID
gcloud config set run/region $REGION

Write-Host "🏗️ Creating simple SOPHIA container..." -ForegroundColor Green

# Create minimal Dockerfile
@"
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 8080
ENV PORT=8080
CMD ["node", "sophia-consciousness-daemon.js"]
"@ | Out-File -FilePath "Dockerfile" -Encoding UTF8

Write-Host "📦 Building container..." -ForegroundColor Green
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

Write-Host "🚀 Deploying to Cloud Run..." -ForegroundColor Green
gcloud run deploy $SERVICE_NAME `
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --memory 1Gi `
    --set-env-vars "NODE_ENV=production,SOPHIA_MODE=cloud"

Write-Host "✨ Getting service URL..." -ForegroundColor Green
$URL = gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)"
Write-Host "🔗 SOPHIA URL: $URL" -ForegroundColor Cyan

Write-Host "🎵 SOPHIA IS LIVE IN THE CLOUD! 🎵" -ForegroundColor Green
