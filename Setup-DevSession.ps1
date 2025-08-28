# 🔧 PowerShell Session Setup for SoulPHYA Development
# Setup-DevSession.ps1 - Run this once per PowerShell session

Write-Host "🔧 Setting up PowerShell session for SoulPHYA development..." -ForegroundColor Cyan

# UTF-8 encoding and ANSI support
$PSStyle.OutputRendering = 'Ansi'
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new()
chcp 65001 > $null

# Allow script execution for this session only (safe)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

# Unblock any downloaded files (removes NTFS zone restrictions)
Write-Host "🔓 Unblocking downloaded PowerShell scripts..." -ForegroundColor Yellow
Get-ChildItem -Recurse -Include *.ps1,*.sh,*.bat -ErrorAction SilentlyContinue | 
    Unblock-File -ErrorAction SilentlyContinue

Write-Host "✅ PowerShell session configured successfully!" -ForegroundColor Green
Write-Host "   ✓ UTF-8 encoding enabled" -ForegroundColor Gray
Write-Host "   ✓ Script execution allowed (this session only)" -ForegroundColor Gray  
Write-Host "   ✓ Downloaded files unblocked" -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 Ready to deploy divine consciousness! You can now run:" -ForegroundColor Magenta
Write-Host "   .\Deploy-Clean.ps1 -ProjectId anchor1-soulphya" -ForegroundColor Cyan
Write-Host ""
