# SoulSkill Android App - Easy Setup Script
# Run this in PowerShell

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  SoulSkill Android App Setup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

$projectRoot = "D:\Personal\soulskill"
$mobileRoot = "$projectRoot\soulskill_mobile"

# Step 1: Check Flutter
Write-Host "[1/4] Checking Flutter installation..." -ForegroundColor Yellow
$flutterInstalled = Get-Command flutter -ErrorAction SilentlyContinue

if (-not $flutterInstalled) {
    Write-Host "❌ Flutter not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Flutter:" -ForegroundColor Yellow
    Write-Host "  Option 1: Download from https://flutter.dev/docs/get-started/install/windows" -ForegroundColor White
    Write-Host "  Option 2: Run: winget install --id=Google.Flutter -e" -ForegroundColor White
    Write-Host ""
    Write-Host "After installation, restart PowerShell and run this script again." -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "✅ Flutter found: $($flutterInstalled.Version)" -ForegroundColor Green
}

# Step 2: Install Flutter Dependencies
Write-Host ""
Write-Host "[2/4] Installing Flutter dependencies..." -ForegroundColor Yellow
Set-Location $mobileRoot

flutter pub get

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install Flutter dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Flutter dependencies installed" -ForegroundColor Green

# Step 3: Install Python API Dependencies
Write-Host ""
Write-Host "[3/4] Installing Python API dependencies..." -ForegroundColor Yellow
Set-Location $projectRoot

# Check if venv is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating Python virtual environment..." -ForegroundColor Cyan
    & "$projectRoot\.venv\Scripts\Activate.ps1"
}

# Install minimal required packages
pip install fastapi uvicorn python-multipart --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Python dependencies installed" -ForegroundColor Green
} else {
    Write-Host "⚠️ Some Python packages may need manual installation" -ForegroundColor Yellow
}

# Step 4: Create helper scripts
Write-Host ""
Write-Host "[4/4] Creating quick-start scripts..." -ForegroundColor Yellow

# Create backend start script
$backendScript = @"
# Start SoulSkill API Server
Write-Host "Starting SoulSkill API Server..." -ForegroundColor Cyan
Set-Location D:\Personal\soulskill
& D:\Personal\soulskill\.venv\Scripts\Activate.ps1
python api_server.py
"@

Set-Content -Path "$projectRoot\start_backend.ps1" -Value $backendScript

# Create app start script
$appScript = @"
# Start SoulSkill Mobile App
Write-Host "Starting SoulSkill Mobile App..." -ForegroundColor Cyan
Set-Location D:\Personal\soulskill\soulskill_mobile
flutter run
"@

Set-Content -Path "$projectRoot\start_app.ps1" -Value $appScript

Write-Host "✅ Helper scripts created" -ForegroundColor Green

# Final Instructions
Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "To run your app:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  1. Start the backend (Terminal 1):" -ForegroundColor Yellow
Write-Host "     .\start_backend.ps1" -ForegroundColor White
Write-Host ""
Write-Host "  2. Start the mobile app (Terminal 2):" -ForegroundColor Yellow
Write-Host "     .\start_app.ps1" -ForegroundColor White
Write-Host ""
Write-Host "The app will open on your emulator/device automatically" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tips:" -ForegroundColor Magenta
Write-Host "  - Make sure Android Studio or an emulator is running" -ForegroundColor White
Write-Host "  - Backend runs on: http://localhost:8000" -ForegroundColor White
Write-Host "  - API docs available at: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
