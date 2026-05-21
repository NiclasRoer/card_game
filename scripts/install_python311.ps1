param(
    [string]$Version = '3.11.9'
)

$ErrorActionPreference = 'Stop'

$root = Get-Location
$installerName = "python-$Version-amd64.exe"
$installerPath = Join-Path $root $installerName
$installerUrl = "https://www.python.org/ftp/python/$Version/$installerName"

$expectedPyPath = Join-Path $env:LOCALAPPDATA "Programs\Python\Python$($Version.Split('.')[0..1] -join '')\python.exe"
if (-not (Test-Path $expectedPyPath)) {
    Write-Host "Downloading Python $Version installer..."
    Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath -UseBasicParsing

    Write-Host "Running installer (per-user)..."
    $args = @('/quiet','InstallAllUsers=0','PrependPath=0','Include_pip=1')
    Start-Process -FilePath $installerPath -ArgumentList $args -Wait
}

$pyPath = $expectedPyPath
if (-not (Test-Path $pyPath)) {
    Write-Host "Python $Version not found at expected location $pyPath" -ForegroundColor Red
    exit 1
}

Write-Host "Creating virtual environment .venv using $pyPath..."
& $pyPath -m venv .venv --clear

Write-Host "Upgrading pip, setuptools, wheel in venv..."
& .\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel

if (Test-Path "requirements.txt") {
    Write-Host "Installing requirements.txt into venv..."
    & .\.venv\Scripts\python.exe -m pip install -r requirements.txt
} else {
    Write-Host "requirements.txt not found; skipping" -ForegroundColor Yellow
}

Write-Host "Cleaning temporary installer and build leftovers..."
if (Test-Path $installerPath) { Remove-Item $installerPath -Force }
if (Test-Path ".python312") { Remove-Item -Recurse -Force ".python312" }
if (Test-Path "prebuilt-x64") { Remove-Item -Recurse -Force "prebuilt-x64" }
if (Test-Path "prebuilt_downloads") { Remove-Item -Recurse -Force "prebuilt_downloads" }

Write-Host "Done. Activate the venv with: & .\\.venv\\Scripts\\Activate.ps1" -ForegroundColor Green
