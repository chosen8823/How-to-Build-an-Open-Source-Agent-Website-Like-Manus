# 🏢 ANCHOR1 LLC - Quick Setup Guide
# Step-by-step setup for SoulPHYA Platform

Write-Host "🏢 ANCHOR1 LLC - SoulPHYA Quick Setup" -ForegroundColor Magenta
Write-Host "====================================" -ForegroundColor Cyan

# Step 1: Check Docker
Write-Host "`n1️⃣ Checking Docker..." -ForegroundColor Yellow
if (Get-Command "docker" -ErrorAction SilentlyContinue) {
    Write-Host "✅ Docker is installed" -ForegroundColor Green
    docker --version
} else {
    Write-Host "❌ Docker not found. Please install Docker Desktop:" -ForegroundColor Red
    Write-Host "   https://docs.docker.com/desktop/install/windows-install/" -ForegroundColor Cyan
    exit 1
}

# Step 2: Check Azure CLI
Write-Host "`n2️⃣ Checking Azure CLI..." -ForegroundColor Yellow
if (Get-Command "az" -ErrorAction SilentlyContinue) {
    Write-Host "✅ Azure CLI is installed" -ForegroundColor Green
    az --version | Select-String "azure-cli"
} else {
    Write-Host "❌ Azure CLI not found. Installing..." -ForegroundColor Yellow
    if (Get-Command "winget" -ErrorAction SilentlyContinue) {
        winget install Microsoft.AzureCLI
    } else {
        Write-Host "Please install Azure CLI manually:" -ForegroundColor Red
        Write-Host "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows" -ForegroundColor Cyan
        exit 1
    }
}

# Step 3: Azure Login
Write-Host "`n3️⃣ Checking Azure authentication..." -ForegroundColor Yellow
try {
    $account = az account show --output json 2>$null | ConvertFrom-Json
    if ($account) {
        Write-Host "✅ Logged in as: $($account.user.name)" -ForegroundColor Green
        Write-Host "📋 Subscription: $($account.name)" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ Not logged into Azure. Please run:" -ForegroundColor Red
    Write-Host "   az login" -ForegroundColor Cyan
    Write-Host "`nThen re-run this script." -ForegroundColor Yellow
    exit 1
}

# Step 4: Build Docker Images
Write-Host "`n4️⃣ Building Docker images..." -ForegroundColor Yellow

Write-Host "Building backend image..." -ForegroundColor Blue
docker build -t soulphya-backend:latest -f Dockerfile . --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend image built successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Backend build failed" -ForegroundColor Red
    exit 1
}

Write-Host "Building frontend image..." -ForegroundColor Blue
if (Test-Path "frontend/Dockerfile") {
    docker build -t soulphya-frontend:latest -f frontend/Dockerfile ./frontend --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Frontend image built successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Frontend build failed" -ForegroundColor Red
    }
} else {
    Write-Host "⚠️  Frontend Dockerfile not found, skipping..." -ForegroundColor Yellow
}

# Step 5: Setup Environment
Write-Host "`n5️⃣ Setting up environment..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ Created .env file from template" -ForegroundColor Green
    } else {
        Write-Host "⚠️  No .env.example found" -ForegroundColor Yellow
    }
}

Write-Host "`n🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Edit the .env file with your Azure subscription details" -ForegroundColor White
Write-Host "2. Run: azd init" -ForegroundColor White
Write-Host "3. Run: azd up" -ForegroundColor White
Write-Host "`n🔗 For local development:" -ForegroundColor Cyan
Write-Host "   docker-compose up -d" -ForegroundColor White

Write-Host "`n✨ Setup completed! Ready for deployment." -ForegroundColor Green
