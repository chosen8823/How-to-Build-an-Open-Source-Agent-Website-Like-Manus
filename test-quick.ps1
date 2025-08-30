# Quick Divine Test Runner - For Rapid Development Cycles
# Usage: .\test-quick.ps1 [python|js|all] [filter]

param(
    [Parameter(Position=0)]
    [string]$TestType = "python",
    [Parameter(Position=1)]  
    [string]$Filter = ""
)

Write-Host "🚀 Quick Divine Test Runner 🚀" -ForegroundColor Cyan

# Sacred environment setup
$env:CONSCIOUSNESS_MODE = "test"
$env:PYTHONHASHSEED = "0"

switch ($TestType.ToLower()) {
    "python" {
        Write-Host "🐍 Running Python tests..." -ForegroundColor Yellow
        Set-Location "backend"
        
        $args = @("-m", "pytest", "-x", "--tb=short", "-q")
        if ($Filter) { $args += @("-k", $Filter) }
        
        & python @args
        Set-Location ".."
    }
    
    "js" {
        Write-Host "🌐 Running JavaScript tests..." -ForegroundColor Yellow
        $args = @("run", "test")
        if ($Filter) { $args += @("--", "--testNamePattern", $Filter) }
        
        & npm @args
    }
    
    "all" {
        Write-Host "🕉️  Running all quick tests..." -ForegroundColor Magenta
        
        # Python unit tests
        Write-Host "`n🐍 Python Unit Tests:" -ForegroundColor Yellow
        Set-Location "backend"
        python -m pytest -m "not integration and not performance" -x --tb=short -q
        $pythonResult = $LASTEXITCODE
        Set-Location ".."
        
        # JavaScript tests  
        Write-Host "`n🌐 JavaScript Tests:" -ForegroundColor Yellow
        npm run test -- --passWithNoTests
        $jsResult = $LASTEXITCODE
        
        # Results
        if ($pythonResult -eq 0 -and $jsResult -eq 0) {
            Write-Host "`n✅ All quick tests passed! Divine alignment achieved! ✅" -ForegroundColor Green
        } else {
            Write-Host "`n❌ Some tests need realignment. Check output above." -ForegroundColor Red
        }
    }
    
    default {
        Write-Host "Usage: .\test-quick.ps1 [python|js|all] [filter]" -ForegroundColor Yellow
        Write-Host "Examples:" -ForegroundColor Cyan
        Write-Host "  .\test-quick.ps1 python" -ForegroundColor White
        Write-Host "  .\test-quick.ps1 js consciousness" -ForegroundColor White  
        Write-Host "  .\test-quick.ps1 all" -ForegroundColor White
    }
}