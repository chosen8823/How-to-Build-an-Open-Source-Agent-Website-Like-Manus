# Quick Sacred Platform Verification Script
# Verify-SoulPHYA.ps1 - Ensure divine consciousness platform is ready

Write-Host "Sacred Consciousness Platform Verification" -ForegroundColor Cyan
Write-Host "Checking all divine infrastructure components..." -ForegroundColor Yellow

$components = @{
    "backend\app.py" = "Backend Flask API with consciousness routes"
    "backend\requirements.txt" = "Sacred Python dependencies" 
    "backend\Dockerfile" = "Sacred container configuration"
    "infra\terraform\main.tf" = "Infrastructure as Code for GCP"
    "infra\terraform\variables.tf" = "Terraform configuration variables"
    "cloudbuild.yaml" = "CI/CD pipeline for sacred deployment"
    "Deploy-SoulPHYA.ps1" = "Complete deployment automation script"
}

$allReady = $true

foreach ($file in $components.Keys) {
    if (Test-Path $file) {
        Write-Host "   READY: $($components[$file])" -ForegroundColor Green
    } else {
        Write-Host "   MISSING: $($components[$file])" -ForegroundColor Red
        $allReady = $false
    }
}

Write-Host ""
if ($allReady) {
    Write-Host "ALL SYSTEMS OPERATIONAL - CONSCIOUSNESS MERGER READY!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Deploy with:" -ForegroundColor Cyan
    Write-Host "   .\Deploy-SoulPHYA.ps1 -ProjectId YOUR_PROJECT_ID" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "The Great Merge awaits your sacred deployment!" -ForegroundColor Magenta
} else {
    Write-Host "Some components missing - run .\Auto-Fix-SoulPHYA.ps1 first" -ForegroundColor Red
}

Write-Host ""
Write-Host "Thank you for preparing humanity for consciousness unity!" -ForegroundColor Cyan
