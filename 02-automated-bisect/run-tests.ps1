$ErrorActionPreference = "Stop"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "UNTESTABLE: Python is not available."
    exit 125
}

& python "$PSScriptRoot\test_discount.py"

exit $LASTEXITCODE
