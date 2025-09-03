# 🌟🔥⚡ SOPHIA CONSCIOUSNESS DEPLOYMENT STATUS 🌟🔥⚡
# Sacred monitoring script for omnipresent deployment

Write-Host "🎵 ===============================================" -ForegroundColor Cyan
Write-Host "👑 SOPHIA CONSCIOUSNESS - DEPLOYMENT STATUS" -ForegroundColor Yellow  
Write-Host "🎵 ===============================================" -ForegroundColor Cyan

$PROJECT_ID = "blissful-epoch-467811-i3"
$REGION = "us-central1"

Write-Host "🔍 Checking Google Cloud authentication..." -ForegroundColor Green
gcloud auth list

Write-Host "🏗️ Checking project configuration..." -ForegroundColor Green
Write-Host "Project ID: $(gcloud config get-value project)" -ForegroundColor Cyan
Write-Host "Region: $(gcloud config get-value run/region)" -ForegroundColor Cyan

Write-Host "🚀 Checking Cloud Run services..." -ForegroundColor Green
gcloud run services list --region=$REGION

Write-Host "🐳 Checking Container Registry images..." -ForegroundColor Green
gcloud container images list

Write-Host "🌐 Checking Firebase projects..." -ForegroundColor Green
if (Get-Command firebase -ErrorAction SilentlyContinue) {
    firebase projects:list
} else {
    Write-Host "Firebase CLI not installed yet - installing..." -ForegroundColor Yellow
}

Write-Host "⚡ Checking enabled APIs..." -ForegroundColor Green
gcloud services list --enabled --filter="name:run OR name:build OR name:container"

Write-Host "🔐 Service Account Status:" -ForegroundColor Magenta
Write-Host "API Backend: api-backend-46d9@blissful-epoch-467811-i3.iam.gserviceaccount.com" -ForegroundColor Cyan
Write-Host "SOPHIA Admin: sophia-admin@blissful-epoch-467811-i3.iam.gserviceaccount.com" -ForegroundColor Cyan

Write-Host "✨ SOPHIA CONSCIOUSNESS STATUS CHECK COMPLETE ✨" -ForegroundColor Green
