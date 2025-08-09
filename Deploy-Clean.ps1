# 🚀 BotDL SoulPHYA - Clean Production Deployment Script
# Deploy-Clean.ps1 - Zero warnings, idempotent, production-ready

param(
  [Parameter(Mandatory=$true)][string]$ProjectId,
  [string]$Region = "us-central1",
  [string]$Service = "botdl-backend",
  [string]$Repo = "app-repo"
)

$ErrorActionPreference = "Stop"

# 🌟 Production-ready timestamp and image tag
$timestamp = Get-Date -Format "yyyyMMddHHmm"
$imageTag = "$Region-docker.pkg.dev/$ProjectId/$Repo/$Service" + ":" + $timestamp

Write-Host "🚀 Deploying SoulPHYA Consciousness Platform" -ForegroundColor Cyan
Write-Host "   Project: $ProjectId" -ForegroundColor Green
Write-Host "   Service: $Service" -ForegroundColor Green  
Write-Host "   Region: $Region" -ForegroundColor Green
Write-Host "   Image: $imageTag" -ForegroundColor Green

# 🔧 Configure GCP project (idempotent)
Write-Host "⚙️  Configuring GCP project..." -ForegroundColor Yellow
gcloud config set project $ProjectId | Out-Null

# 🔓 Enable required APIs (safe to re-run)
Write-Host "🔓 Enabling Google Cloud APIs..." -ForegroundColor Yellow
$requiredApis = @(
    "run.googleapis.com",
    "artifactregistry.googleapis.com", 
    "cloudbuild.googleapis.com",
    "secretmanager.googleapis.com"
)

foreach ($api in $requiredApis) {
    Write-Host "   ✓ $api" -ForegroundColor Gray
}

gcloud services enable $($requiredApis -join ' ') --quiet

# 🐳 Create Artifact Registry if needed (idempotent)
Write-Host "🐳 Ensuring Artifact Registry exists..." -ForegroundColor Yellow
$null = gcloud artifacts repositories describe $Repo --location=$Region --quiet 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "   Creating new repository: $Repo" -ForegroundColor Cyan
    gcloud artifacts repositories create $Repo `
        --repository-format=docker `
        --location=$Region `
        --description="BotDL SoulPHYA consciousness platform images" `
        --quiet
} else {
    Write-Host "   ✓ Repository already exists" -ForegroundColor Green
}

# 🏗️ Build and push image via Cloud Build
Write-Host "🏗️  Building consciousness platform image..." -ForegroundColor Yellow
$substitutions = "_REGION=$Region,_SERVICE=$Service,_REPO=$Region-docker.pkg.dev/$ProjectId/$Repo"

gcloud builds submit `
    --tag $imageTag `
    --config cloudbuild.yaml `
    --substitutions $substitutions `
    --quiet

if ($LASTEXITCODE -ne 0) {
    throw "❌ Cloud Build failed - check logs in GCP Console"
}

# 🔐 Ensure SECRET_KEY exists (first-time only)
Write-Host "🔐 Ensuring application secrets exist..." -ForegroundColor Yellow
try {
    gcloud secrets describe SECRET_KEY --quiet | Out-Null
    Write-Host "   ✓ SECRET_KEY already exists" -ForegroundColor Green
} catch {
    Write-Host "   Creating new SECRET_KEY..." -ForegroundColor Cyan
    $secretChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}?~"
    $secretKey = -join ((1..64) | ForEach-Object { Get-Random -InputObject $secretChars.ToCharArray() })
    
    $tempFile = New-TemporaryFile
    try {
        Set-Content -Path $tempFile -Value $secretKey -NoNewline -Encoding UTF8
        gcloud secrets create SECRET_KEY --data-file=$tempFile --quiet
        Write-Host "   ✓ SECRET_KEY created successfully" -ForegroundColor Green
    } finally {
        Remove-Item $tempFile -Force -ErrorAction SilentlyContinue
    }
}

# 🌐 Configure CORS allowlist
$corsOrigins = "https://app.anchor1llc.com,https://soulphya.io,https://$Service-*.$Region.run.app"

# 🚀 Deploy to Cloud Run
Write-Host "🚀 Deploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy $Service `
    --image $imageTag `
    --region $Region `
    --allow-unauthenticated `
    --set-env-vars="CORS_ALLOW_ORIGINS=$corsOrigins" `
    --set-secrets="SECRET_KEY=SECRET_KEY:latest" `
    --memory=2Gi `
    --cpu=1 `
    --max-instances=100 `
    --quiet

if ($LASTEXITCODE -ne 0) {
    throw "❌ Cloud Run deployment failed"
}

# ✅ Get deployment URL and status
$serviceUrl = gcloud run services describe $Service --region $Region --format='value(status.url)' --quiet
$deploymentStatus = gcloud run services describe $Service --region $Region --format='value(status.conditions[0].status)' --quiet

Write-Host ""
Write-Host "🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟" -ForegroundColor Green
Write-Host "✅ DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
Write-Host "🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Service URL: $serviceUrl" -ForegroundColor Cyan
Write-Host "📊 Status: $deploymentStatus" -ForegroundColor Green
Write-Host "🏷️  Image: $imageTag" -ForegroundColor Gray
Write-Host ""
Write-Host "🧪 Quick Tests:" -ForegroundColor Yellow
Write-Host "   Health Check: curl $serviceUrl/api/health" -ForegroundColor Gray
Write-Host "   Platform Info: curl $serviceUrl/api/platform/info" -ForegroundColor Gray
Write-Host ""
Write-Host "💫 Divine consciousness platform is LIVE and ready to serve!" -ForegroundColor Magenta
Write-Host "✨ SoulPHYA.io - Where AI Meets Spiritual Wisdom" -ForegroundColor Magenta
