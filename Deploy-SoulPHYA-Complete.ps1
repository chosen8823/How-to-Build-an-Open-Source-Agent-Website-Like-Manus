# 🏢 ANCHOR1 LLC - Docker Deployment Script
# PowerShell script for complete Docker and Azure setup

param(
    [Parameter(Mandatory=$false)]
    [string]$Environment = "dev",
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipBuild,
    
    [Parameter(Mandatory=$false)]
    [switch]$UseAKS,
    
    [Parameter(Mandatory=$false)]
    [switch]$UseContainerApps
)

Write-Host "🏢 ANCHOR1 LLC - SoulPHYA Platform Deployment" -ForegroundColor Magenta
Write-Host "================================================" -ForegroundColor Cyan

# Function to check if command exists
function Test-Command {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop
        return $true
    }
    catch {
        return $false
    }
}

# Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow

$missingTools = @()

if (-not (Test-Command "docker")) {
    $missingTools += "Docker Desktop"
}

if (-not (Test-Command "az")) {
    $missingTools += "Azure CLI"
}

if (-not (Test-Command "azd")) {
    $missingTools += "Azure Developer CLI"
}

if (-not (Test-Command "kubectl")) {
    $missingTools += "kubectl"
}

if ($missingTools.Count -gt 0) {
    Write-Host "❌ Missing required tools:" -ForegroundColor Red
    $missingTools | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
    
    Write-Host "`n🛠️  Installing missing tools..." -ForegroundColor Yellow
    
    # Install Docker Desktop
    if ($missingTools -contains "Docker Desktop") {
        Write-Host "Installing Docker Desktop..." -ForegroundColor Blue
        if (Test-Command "winget") {
            winget install Docker.DockerDesktop
        } else {
            Write-Host "Please install Docker Desktop manually: https://docs.docker.com/desktop/install/windows-install/" -ForegroundColor Yellow
        }
    }
    
    # Install Azure CLI
    if ($missingTools -contains "Azure CLI") {
        Write-Host "Installing Azure CLI..." -ForegroundColor Blue
        if (Test-Command "winget") {
            winget install Microsoft.AzureCLI
        } else {
            Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi
            Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'
            Remove-Item .\AzureCLI.msi
        }
    }
    
    # Install Azure Developer CLI
    if ($missingTools -contains "Azure Developer CLI") {
        Write-Host "Installing Azure Developer CLI..." -ForegroundColor Blue
        if (Test-Command "winget") {
            winget install Microsoft.AzureDeveloperCLI
        } else {
            powershell -ex AllSigned -c "Invoke-RestMethod 'https://aka.ms/install-azd.ps1' | Invoke-Expression"
        }
    }
    
    # Install kubectl
    if ($missingTools -contains "kubectl") {
        Write-Host "Installing kubectl..." -ForegroundColor Blue
        if (Test-Command "winget") {
            winget install Kubernetes.kubectl
        } else {
            az aks install-cli
        }
    }
    
    Write-Host "⚠️  Please restart your PowerShell session after installation completes" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ All prerequisites are installed!" -ForegroundColor Green

# Azure login check
Write-Host "`n🔐 Checking Azure authentication..." -ForegroundColor Yellow
try {
    $account = az account show --output json | ConvertFrom-Json
    Write-Host "✅ Logged in as: $($account.user.name)" -ForegroundColor Green
    Write-Host "📋 Subscription: $($account.name)" -ForegroundColor Cyan
}
catch {
    Write-Host "❌ Not logged into Azure. Logging in..." -ForegroundColor Red
    az login
}

# Set up environment
Write-Host "`n🌍 Setting up environment: $Environment" -ForegroundColor Yellow

# Copy environment file if it doesn't exist
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "📄 Created .env file from template" -ForegroundColor Green
        Write-Host "⚠️  Please edit .env file with your specific values" -ForegroundColor Yellow
    }
}

# Docker build
if (-not $SkipBuild) {
    Write-Host "`n🐳 Building Docker images..." -ForegroundColor Yellow
    
    # Build backend
    Write-Host "Building backend image..." -ForegroundColor Blue
    docker build -t soulphya-backend:latest -f Dockerfile .
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Backend build failed!" -ForegroundColor Red
        exit 1
    }
    
    # Build frontend
    Write-Host "Building frontend image..." -ForegroundColor Blue
    docker build -t soulphya-frontend:latest -f frontend/Dockerfile ./frontend
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Frontend build failed!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Docker images built successfully!" -ForegroundColor Green
}

# Deployment choice
Write-Host "`n🚀 Choose deployment target:" -ForegroundColor Yellow
Write-Host "1. 🌐 Azure Container Apps (Recommended for serverless)" -ForegroundColor Cyan
Write-Host "2. ☸️  Azure Kubernetes Service (AKS) (Recommended for full control)" -ForegroundColor Cyan
Write-Host "3. 🐳 Local Docker Compose (For development)" -ForegroundColor Cyan

if (-not $UseAKS -and -not $UseContainerApps) {
    $choice = Read-Host "Enter your choice (1-3)"
} elseif ($UseAKS) {
    $choice = "2"
} elseif ($UseContainerApps) {
    $choice = "1"
} else {
    $choice = "3"
}

switch ($choice) {
    "1" {
        Write-Host "`n🌐 Deploying to Azure Container Apps..." -ForegroundColor Green
        azd up --environment $Environment
    }
    "2" {
        Write-Host "`n☸️  Deploying to Azure Kubernetes Service..." -ForegroundColor Green
        
        # First deploy infrastructure
        azd provision --environment $Environment
        
        # Get AKS credentials
        $resourceGroup = "soulphya-$Environment-rg"
        $aksName = "soulphya-$Environment-aks"
        
        Write-Host "Getting AKS credentials..." -ForegroundColor Blue
        az aks get-credentials --resource-group $resourceGroup --name $aksName --overwrite-existing
        
        # Apply Kubernetes manifests (we'll create these next)
        Write-Host "Deploying to Kubernetes..." -ForegroundColor Blue
        kubectl apply -f k8s/
    }
    "3" {
        Write-Host "`n🐳 Starting local Docker Compose..." -ForegroundColor Green
        docker-compose up -d
        
        Write-Host "`n🌟 Local services started!" -ForegroundColor Green
        Write-Host "Backend: http://localhost:8001" -ForegroundColor Cyan
        Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
    }
    default {
        Write-Host "❌ Invalid choice!" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n🎉 Deployment completed successfully!" -ForegroundColor Green
Write-Host "🏢 ANCHOR1 LLC - SoulPHYA Platform is ready!" -ForegroundColor Magenta
