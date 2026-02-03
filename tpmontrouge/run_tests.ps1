# Script PowerShell pour exécuter les tests sur Windows
# Équivalent de run_tests.sh pour Windows

# Supprimer les warnings Python non critiques
$env:PYTHONWARNINGS = "ignore::DeprecationWarning,ignore::UserWarning"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Running tests on Windows..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Exécuter les tests
python -m unittest discover

# Capturer le code de sortie
$exitCode = $LASTEXITCODE

Write-Host ""
if ($exitCode -eq 0) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "All tests passed!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
} else {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "Some tests failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
}

# Retourner le code de sortie
exit $exitCode
