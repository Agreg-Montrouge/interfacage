# TPMontrouge Windows Build Script
# Run from tpmontrouge directory on Windows VM
# Usage: powershell -ExecutionPolicy Bypass -File build_local.ps1

param(
    [switch]$SkipInstaller = $false,
    [switch]$SkipTests = $false,
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Green
Write-Host "TPMontrouge Windows Build" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Check we're in the right directory
if (-not (Test-Path "tpmontrouge\__init__.py")) {
    Write-Host "ERROR: Must run from tpmontrouge package root directory" -ForegroundColor Red
    Write-Host "Current directory: $PWD" -ForegroundColor Red
    exit 1
}

# Get version
Write-Host "`nRetrieving version..." -ForegroundColor Yellow
Push-Location tpmontrouge
try {
    $version = python -W ignore -c "import tpmontrouge; print(tpmontrouge.__version__)" 2>&1 | Select-Object -Last 1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to get version" -ForegroundColor Red
        exit 1
    }
} finally {
    Pop-Location
}
Write-Host "Building version: $version" -ForegroundColor Cyan

# Install package
Write-Host "`nInstalling package in development mode..." -ForegroundColor Yellow
pip install -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Package installation failed" -ForegroundColor Red
    exit 1
}

# Run tests if not skipped
if (-not $SkipTests) {
    Write-Host "`nRunning tests..." -ForegroundColor Yellow
    $env:PYTHONWARNINGS = "ignore::DeprecationWarning,ignore::UserWarning"
    python -m unittest discover -s tpmontrouge -p "test_*.py" -v
    if ($LASTEXITCODE -ne 0) {
        Write-Host "WARNING: Some tests failed, but continuing build..." -ForegroundColor Yellow
    } else {
        Write-Host "  ✓ All tests passed" -ForegroundColor Green
    }
}

# Build executables
Write-Host "`nBuilding executables with PyInstaller..." -ForegroundColor Yellow
Push-Location scripts

# Clean previous builds
if (Test-Path "dist") {
    Write-Host "  Cleaning previous builds..." -ForegroundColor Gray
    Remove-Item -Recurse -Force dist
}
if (Test-Path "build") {
    Remove-Item -Recurse -Force build
}

# Build empty_bode.exe
Write-Host "  [1/3] Building empty_bode.exe..." -ForegroundColor Cyan
if ($Verbose) {
    pyinstaller -y empty_bode.spec
} else {
    pyinstaller -y empty_bode.spec 2>&1 | Out-Null
}
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: empty_bode.exe build failed" -ForegroundColor Red
    Pop-Location
    exit 1
}
Write-Host "        ✓ empty_bode.exe built successfully" -ForegroundColor Green

# Build interface.exe
Write-Host "  [2/3] Building interface.exe..." -ForegroundColor Cyan
if ($Verbose) {
    pyinstaller -y interface.spec
} else {
    pyinstaller -y interface.spec 2>&1 | Out-Null
}
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: interface.exe build failed" -ForegroundColor Red
    Pop-Location
    exit 1
}
Write-Host "        ✓ interface.exe built successfully" -ForegroundColor Green

# Build interface_folder (for installer)
if (-not $SkipInstaller) {
    Write-Host "  [3/3] Building interface_folder (for installer)..." -ForegroundColor Cyan
    if ($Verbose) {
        pyinstaller -y interface_folder.spec
    } else {
        pyinstaller -y interface_folder.spec 2>&1 | Out-Null
    }
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: interface_folder build failed" -ForegroundColor Red
        Pop-Location
        exit 1
    }
    Write-Host "        ✓ interface_folder built successfully" -ForegroundColor Green
    
    # Generate Inno Setup script
    Write-Host "`nGenerating installer script..." -ForegroundColor Yellow
    $template = Get-Content interface_gui.iss.tpl -Raw
    $output = $template -replace '\$version', $version
    $output | Set-Content interface_gui.iss -Encoding UTF8
    Write-Host "  ✓ Generated interface_gui.iss with version $version" -ForegroundColor Green
    
    # Build installer
    Write-Host "`nBuilding installer with Inno Setup..." -ForegroundColor Yellow
    $isccPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    if (-not (Test-Path $isccPath)) {
        Write-Host "WARNING: Inno Setup not found at $isccPath" -ForegroundColor Yellow
        Write-Host "Skipping installer build..." -ForegroundColor Yellow
    } else {
        & $isccPath interface_gui.iss
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: Installer build failed" -ForegroundColor Red
            Pop-Location
            exit 1
        }
        Write-Host "  ✓ Installer built successfully" -ForegroundColor Green
    }
} else {
    Write-Host "  [3/3] Skipping installer build (--SkipInstaller)" -ForegroundColor Gray
}

Pop-Location

# Summary
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host "Version: $version" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nArtifacts created:"

$artifacts = @()
if (Test-Path "scripts\dist\empty_bode.exe") {
    $size = [math]::Round((Get-Item "scripts\dist\empty_bode.exe").Length / 1MB, 2)
    Write-Host "  ✓ empty_bode.exe ($size MB)" -ForegroundColor White
    $artifacts += "empty_bode.exe"
}
if (Test-Path "scripts\dist\interface.exe") {
    $size = [math]::Round((Get-Item "scripts\dist\interface.exe").Length / 1MB, 2)
    Write-Host "  ✓ interface.exe ($size MB)" -ForegroundColor White
    $artifacts += "interface.exe"
}
if (Test-Path "scripts\dist\interface_agreg_setup.exe") {
    $size = [math]::Round((Get-Item "scripts\dist\interface_agreg_setup.exe").Length / 1MB, 2)
    Write-Host "  ✓ interface_agreg_setup.exe ($size MB)" -ForegroundColor White
    $artifacts += "interface_agreg_setup.exe"
}

Write-Host "`nArtifacts location: $(Resolve-Path scripts\dist)" -ForegroundColor Cyan
Write-Host "`nTotal artifacts: $($artifacts.Count)" -ForegroundColor Cyan

# Create summary file
$summaryPath = "scripts\dist\build_summary.txt"
@"
TPMontrouge Build Summary
=========================
Build Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Version: $version
Platform: Windows $(([Environment]::OSVersion.Version).ToString())
Python: $(python --version)

Artifacts:
$($artifacts -join "`n")

Build Location: $(Resolve-Path scripts\dist)
"@ | Out-File -FilePath $summaryPath -Encoding UTF8

Write-Host "`nBuild summary saved to: $summaryPath" -ForegroundColor Gray
