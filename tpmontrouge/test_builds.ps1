# TPMontrouge Build Test Script
# Quick smoke test for built executables
# Run from tpmontrouge directory on Windows VM
# Usage: powershell -ExecutionPolicy Bypass -File test_builds.ps1

param(
    [int]$WaitSeconds = 5,
    [switch]$SkipGUI = $false
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Green
Write-Host "Testing TPMontrouge Executables" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Check we're in the right directory
if (-not (Test-Path "scripts\dist")) {
    Write-Host "ERROR: scripts\dist directory not found" -ForegroundColor Red
    Write-Host "Current directory: $PWD" -ForegroundColor Red
    Write-Host "Run build_local.ps1 first to create executables" -ForegroundColor Yellow
    exit 1
}

$testResults = @()
$failedTests = 0

# Function to test an executable
function Test-Executable {
    param(
        [string]$Name,
        [string]$Path,
        [int]$WaitTime = 5
    )
    
    Write-Host "`nTesting $Name..." -ForegroundColor Cyan
    
    # Check file exists
    if (-not (Test-Path $Path)) {
        Write-Host "  ✗ File not found: $Path" -ForegroundColor Red
        return $false
    }
    
    # Check file size
    $size = [math]::Round((Get-Item $Path).Length / 1MB, 2)
    Write-Host "  File size: $size MB" -ForegroundColor Gray
    
    if ($size -lt 10) {
        Write-Host "  ✗ File size suspiciously small (< 10 MB)" -ForegroundColor Red
        return $false
    }
    
    # Try to launch
    try {
        Write-Host "  Launching executable..." -ForegroundColor Gray
        $proc = Start-Process $Path -PassThru -WindowStyle Minimized
        
        # Wait for process to start
        Start-Sleep -Seconds 1
        
        if ($proc.HasExited) {
            Write-Host "  ✗ Process exited immediately (exit code: $($proc.ExitCode))" -ForegroundColor Red
            return $false
        }
        
        # Wait to see if it crashes
        Write-Host "  Waiting $WaitTime seconds to check stability..." -ForegroundColor Gray
        Start-Sleep -Seconds $WaitTime
        
        if ($proc.HasExited) {
            Write-Host "  ✗ Process crashed after $WaitTime seconds (exit code: $($proc.ExitCode))" -ForegroundColor Red
            return $false
        }
        
        # Success - kill the process
        Write-Host "  Stopping process..." -ForegroundColor Gray
        Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
        
        # Wait for cleanup
        Start-Sleep -Seconds 1
        
        Write-Host "  ✓ $Name launched successfully and ran for $WaitTime seconds" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "  ✗ Exception occurred: $_" -ForegroundColor Red
        return $false
    }
}

# Test 1: empty_bode.exe
Write-Host "`n[1/3] Testing empty_bode.exe" -ForegroundColor Yellow
$result1 = Test-Executable -Name "empty_bode.exe" -Path "scripts\dist\empty_bode.exe" -WaitTime $WaitSeconds
$testResults += @{Name="empty_bode.exe"; Result=$result1}
if (-not $result1) { $failedTests++ }

# Test 2: interface.exe
Write-Host "`n[2/3] Testing interface.exe" -ForegroundColor Yellow
$result2 = Test-Executable -Name "interface.exe" -Path "scripts\dist\interface.exe" -WaitTime $WaitSeconds
$testResults += @{Name="interface.exe"; Result=$result2}
if (-not $result2) { $failedTests++ }

# Test 3: installer
Write-Host "`n[3/3] Testing installer" -ForegroundColor Yellow
if (Test-Path "scripts\dist\interface_agreg_setup.exe") {
    $size = [math]::Round((Get-Item "scripts\dist\interface_agreg_setup.exe").Length / 1MB, 2)
    Write-Host "  Installer found: $size MB" -ForegroundColor Gray
    
    if ($size -lt 20) {
        Write-Host "  ✗ Installer size suspiciously small (< 20 MB)" -ForegroundColor Red
        $testResults += @{Name="installer"; Result=$false}
        $failedTests++
    } else {
        Write-Host "  ✓ Installer exists and has reasonable size" -ForegroundColor Green
        Write-Host "  Note: Not running installer (would require admin rights)" -ForegroundColor Gray
        $testResults += @{Name="installer"; Result=$true}
    }
} else {
    Write-Host "  ⊘ Installer not found (may have been built with -SkipInstaller)" -ForegroundColor Yellow
    $testResults += @{Name="installer"; Result="skipped"}
}

# Summary
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Test Results" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

foreach ($result in $testResults) {
    $status = if ($result.Result -eq $true) {
        "✓ PASS"
    } elseif ($result.Result -eq "skipped") {
        "⊘ SKIP"
    } else {
        "✗ FAIL"
    }
    
    $color = if ($result.Result -eq $true) { "Green" } 
             elseif ($result.Result -eq "skipped") { "Yellow" }
             else { "Red" }
    
    Write-Host "  $status - $($result.Name)" -ForegroundColor $color
}

Write-Host ""
if ($failedTests -eq 0) {
    Write-Host "All tests passed!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "$failedTests test(s) failed" -ForegroundColor Red
    Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
    Write-Host "  • Check build logs for errors" -ForegroundColor Gray
    Write-Host "  • Try rebuilding: powershell -ExecutionPolicy Bypass -File build_local.ps1 -Verbose" -ForegroundColor Gray
    Write-Host "  • Check Python dependencies: pip list" -ForegroundColor Gray
    Write-Host "  • Test manually by double-clicking the .exe files" -ForegroundColor Gray
    exit 1
}
