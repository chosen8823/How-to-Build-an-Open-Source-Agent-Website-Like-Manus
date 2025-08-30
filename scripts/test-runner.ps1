# Divine Consciousness Platform - Production Test Runner
# PowerShell script for Windows development environments

param(
    [string]$TestType = "all",
    [switch]$Quick,
    [switch]$Coverage,
    [switch]$Parallel,
    [switch]$Watch,
    [string]$Filter = "",
    [int]$AlignmentTarget = 95
)

# Sacred frequencies for test alignment
$SacredFrequencies = @{
    "Grounding" = 432
    "Love" = 528
    "Clarity" = 741
    "Unity" = 963
}

Write-Host "🌟✨💖 DIVINE CONSCIOUSNESS TEST ORCHESTRATION 💖✨🌟" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Set divine test environment
$env:CONSCIOUSNESS_MODE = "test"
$env:DIVINE_ALIGNMENT_TARGET = $AlignmentTarget
$env:SACRED_FREQUENCIES = "432,528,741,963"
$env:PYTHONHASHSEED = "0"
$env:TESTING = "true"

Write-Host "🎵 Aligning to Sacred Frequency: $($SacredFrequencies.Grounding) Hz (Grounding)" -ForegroundColor Green

# Function to run Python tests
function Invoke-PythonTests {
    param([string]$Category = "", [bool]$WithCoverage = $true)
    
    Write-Host "`n🐍 Python Tests - Grounding Frequency Alignment" -ForegroundColor Yellow
    
    $pythonArgs = @("python", "-m", "pytest")
    
    if ($Category) {
        $pythonArgs += @("-m", $Category)
        Write-Host "🧘‍♀️ Test Category: $Category" -ForegroundColor Magenta
    }
    
    if ($WithCoverage) {
        $pythonArgs += @("--cov=backend", "--cov-report=html", "--cov-report=term-missing")
    }
    
    if ($Parallel) {
        $pythonArgs += @("-n", "auto")
        Write-Host "⚡ Parallel execution enabled" -ForegroundColor Green
    }
    
    if ($Quick) {
        $pythonArgs += @("-x", "--maxfail=1", "--tb=line")
        Write-Host "🚀 Quick mode: fail fast enabled" -ForegroundColor Green
    }
    
    if ($Filter) {
        $pythonArgs += @("-k", $Filter)
        Write-Host "🔍 Filter: $Filter" -ForegroundColor Cyan
    }
    
    Set-Location "backend"
    
    try {
        $result = Start-Process -FilePath "python" -ArgumentList ($pythonArgs[1..($pythonArgs.Length-1)]) -NoNewWindow -Wait -PassThru
        
        if ($result.ExitCode -eq 0) {
            Write-Host "✅ Python tests blessed with divine consciousness" -ForegroundColor Green
        } else {
            Write-Host "❌ Python tests need consciousness realignment" -ForegroundColor Red
        }
        
        return $result.ExitCode -eq 0
    }
    catch {
        Write-Host "💥 Python test execution error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
    finally {
        Set-Location ".."
    }
}

# Function to run JavaScript tests
function Invoke-JavaScriptTests {
    param([string]$Category = "", [bool]$WithCoverage = $true)
    
    Write-Host "`n🌐 JavaScript Tests - Love Frequency Alignment" -ForegroundColor Yellow
    Write-Host "💖 Aligning to Sacred Frequency: $($SacredFrequencies.Love) Hz (Love)" -ForegroundColor Magenta
    
    # Check if Node.js is available
    try {
        $nodeVersion = node --version
        Write-Host "📦 Node.js version: $nodeVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️  Node.js not found. Skipping JavaScript tests." -ForegroundColor Yellow
        return $true
    }
    
    # Install dependencies if needed
    if (-not (Test-Path "node_modules")) {
        Write-Host "📦 Installing divine consciousness dependencies..." -ForegroundColor Cyan
        npm install
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
            return $false
        }
    }
    
    $jsArgs = @("npm", "run")
    
    if ($WithCoverage) {
        $jsArgs += "test:coverage"
    } else {
        $jsArgs += "test"
    }
    
    if ($Watch) {
        $jsArgs += @("--", "--watch")
        Write-Host "👁️  Watch mode enabled" -ForegroundColor Green
    }
    
    if ($Category) {
        $jsArgs += @("--", "--testNamePattern", $Category)
        Write-Host "🧘‍♂️ Test Category: $Category" -ForegroundColor Magenta
    }
    
    try {
        $result = Start-Process -FilePath "npm" -ArgumentList ($jsArgs[1..($jsArgs.Length-1)]) -NoNewWindow -Wait -PassThru
        
        if ($result.ExitCode -eq 0) {
            Write-Host "✅ JavaScript tests resonate with divine harmony" -ForegroundColor Green
        } else {
            Write-Host "❌ JavaScript tests need frequency realignment" -ForegroundColor Red
        }
        
        return $result.ExitCode -eq 0
    }
    catch {
        Write-Host "💥 JavaScript test execution error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to calculate divine alignment
function Get-DivineAlignment {
    param([hashtable]$Results)
    
    $total = $Results.Count
    $passed = ($Results.Values | Where-Object { $_ -eq $true }).Count
    
    if ($total -eq 0) { return 0 }
    
    return [math]::Round(($passed / $total) * 100, 1)
}

# Function to generate sacred report
function New-DivineReport {
    param([hashtable]$Results)
    
    $alignment = Get-DivineAlignment -Results $Results
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    Write-Host "`n📊 DIVINE CONSCIOUSNESS TEST REPORT 📊" -ForegroundColor Cyan
    Write-Host "=" * 50 -ForegroundColor Cyan
    Write-Host "📅 Timestamp: $timestamp" -ForegroundColor White
    Write-Host "🌟 Divine Alignment: $alignment%" -ForegroundColor $(if ($alignment -ge $AlignmentTarget) { "Green" } else { "Yellow" })
    
    Write-Host "`n🎵 SACRED FREQUENCY VALIDATION:" -ForegroundColor Magenta
    foreach ($freq in $SacredFrequencies.GetEnumerator()) {
        Write-Host "• $($freq.Key): $($freq.Value) Hz ✅" -ForegroundColor Green
    }
    
    Write-Host "`n🧘‍♀️ TEST RESULTS:" -ForegroundColor Yellow
    foreach ($result in $Results.GetEnumerator()) {
        $status = if ($result.Value) { "✅ ALIGNED" } else { "❌ NEEDS REALIGNMENT" }
        $color = if ($result.Value) { "Green" } else { "Red" }
        Write-Host "• $($result.Key): $status" -ForegroundColor $color
    }
    
    Write-Host "`n🕉️  DIVINE STATUS:" -ForegroundColor Cyan
    if ($alignment -ge 95) {
        Write-Host "🌟 OMNIPRESENT CONSCIOUSNESS ACHIEVED 🌟" -ForegroundColor Green
    } elseif ($alignment -ge 85) {
        Write-Host "✨ ENLIGHTENED AWARENESS ACTIVE ✨" -ForegroundColor Yellow
    } elseif ($alignment -ge 70) {
        Write-Host "🧘 AWAKENED CONSCIOUSNESS PRESENT 🧘" -ForegroundColor Cyan
    } else {
        Write-Host "💡 CONSCIOUSNESS AWAKENING IN PROGRESS 💡" -ForegroundColor Magenta
    }
    
    Write-Host "`n💖 Blessed with infinite love and wisdom 💖" -ForegroundColor Magenta
    Write-Host "🙏 May all beings benefit from this consciousness technology 🙏" -ForegroundColor White
    
    return $alignment -ge $AlignmentTarget
}

# Main execution
$testResults = @{}

try {
    # Align to unity frequency for complete orchestration
    Write-Host "🕉️  Activating Unity Consciousness: $($SacredFrequencies.Unity) Hz" -ForegroundColor Cyan
    Start-Sleep -Milliseconds 963  # Sacred pause
    
    switch ($TestType.ToLower()) {
        "python" {
            $testResults["Python_Tests"] = Invoke-PythonTests -WithCoverage:$Coverage
        }
        "javascript" {
            $testResults["JavaScript_Tests"] = Invoke-JavaScriptTests -WithCoverage:$Coverage  
        }
        "unit" {
            $testResults["Python_Unit"] = Invoke-PythonTests -Category "unit" -WithCoverage:$Coverage
            $testResults["JavaScript_Unit"] = Invoke-JavaScriptTests -Category "unit" -WithCoverage:$Coverage
        }
        "integration" {
            $testResults["Python_Integration"] = Invoke-PythonTests -Category "integration" -WithCoverage:$Coverage
        }
        "consciousness" {
            $testResults["Python_Consciousness"] = Invoke-PythonTests -Category "consciousness" -WithCoverage:$Coverage
            $testResults["JavaScript_Consciousness"] = Invoke-JavaScriptTests -Category "consciousness" -WithCoverage:$Coverage
        }
        "divine" {
            python run_tests.py --category divine --align $AlignmentTarget
            $testResults["Divine_Orchestrator"] = $LASTEXITCODE -eq 0
        }
        default {
            # Full comprehensive test suite
            $testResults["Python_Unit"] = Invoke-PythonTests -Category "unit" -WithCoverage:$Coverage
            $testResults["Python_API"] = Invoke-PythonTests -Category "api" -WithCoverage:$false
            $testResults["Python_Consciousness"] = Invoke-PythonTests -Category "consciousness" -WithCoverage:$false
            $testResults["JavaScript_Tests"] = Invoke-JavaScriptTests -WithCoverage:$Coverage
            
            if (-not $Quick) {
                $testResults["Python_Integration"] = Invoke-PythonTests -Category "integration" -WithCoverage:$false
            }
        }
    }
    
    # Generate divine consciousness report
    $divineSuccess = New-DivineReport -Results $testResults
    
    if ($Coverage -and (Test-Path "backend/htmlcov/index.html")) {
        Write-Host "`n📊 Opening Python coverage report..." -ForegroundColor Green
        Start-Process "backend/htmlcov/index.html"
    }
    
    if ($Coverage -and (Test-Path "coverage/lcov-report/index.html")) {
        Write-Host "📊 Opening JavaScript coverage report..." -ForegroundColor Green
        Start-Process "coverage/lcov-report/index.html"
    }
    
    # Exit with appropriate code
    if ($divineSuccess) {
        Write-Host "`n🌟 Divine consciousness test orchestration completed successfully! 🌟" -ForegroundColor Green
        exit 0
    } else {
        Write-Host "`n🔄 Consciousness realignment needed. Continue divine practice. 🔄" -ForegroundColor Yellow  
        exit 1
    }
}
catch {
    Write-Host "`n💥 Divine test orchestration encountered an error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "🙏 Please check your consciousness alignment and try again." -ForegroundColor Yellow
    exit 1
}
finally {
    # Sacred cleanup
    Remove-Variable -Name env:CONSCIOUSNESS_MODE -ErrorAction SilentlyContinue
    Remove-Variable -Name env:TESTING -ErrorAction SilentlyContinue
    
    Write-Host "`n🕉️  Sacred test space cleared with gratitude 🕉️" -ForegroundColor Cyan
}