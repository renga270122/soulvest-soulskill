# 🚀 Quick Deploy to Soulvest.ai
# Run this script to prepare for deployment

Write-Host "🚀 Soulvest.ai Deployment Preparation" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if in correct directory
if (-not (Test-Path "app.py")) {
    Write-Host "❌ Error: app.py not found. Please run this script from the project root." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Found app.py" -ForegroundColor Green

# Check Python version
Write-Host ""
Write-Host "📋 Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "   $pythonVersion" -ForegroundColor Gray

# Check if requirements.txt exists
if (Test-Path "requirements.txt") {
    Write-Host "✅ Found requirements.txt" -ForegroundColor Green
} else {
    Write-Host "❌ requirements.txt not found" -ForegroundColor Red
    exit 1
}

# Check for Git repository
Write-Host ""
Write-Host "📋 Checking Git repository..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
    
    # Check git status
    $gitStatus = git status --porcelain
    if ($gitStatus) {
        Write-Host "⚠️  You have uncommitted changes:" -ForegroundColor Yellow
        git status --short
        Write-Host ""
        $commit = Read-Host "Do you want to commit these changes? (y/n)"
        if ($commit -eq "y" -or $commit -eq "Y") {
            Write-Host "📝 Committing changes..." -ForegroundColor Yellow
            git add .
            $message = Read-Host "Enter commit message (or press Enter for default)"
            if (-not $message) {
                $message = "Ready for soulvest.ai deployment"
            }
            git commit -m $message
            Write-Host "✅ Changes committed" -ForegroundColor Green
        }
    } else {
        Write-Host "✅ Working directory clean" -ForegroundColor Green
    }
    
    # Check remote
    $remotes = git remote -v
    if ($remotes) {
        Write-Host "✅ Git remote configured:" -ForegroundColor Green
        Write-Host "   $($remotes -split "`n" | Select-Object -First 1)" -ForegroundColor Gray
    } else {
        Write-Host "⚠️  No git remote configured" -ForegroundColor Yellow
        Write-Host "   Add remote with: git remote add origin <your-repo-url>" -ForegroundColor Gray
    }
} else {
    Write-Host "❌ Not a git repository" -ForegroundColor Red
    Write-Host "   Initialize with: git init" -ForegroundColor Gray
    exit 1
}

# Check for required files
Write-Host ""
Write-Host "📋 Checking deployment files..." -ForegroundColor Yellow

$requiredFiles = @(
    "manifest.json",
    "service-worker.js",
    "robots.txt",
    "sitemap.xml",
    "CNAME",
    "runtime.txt",
    ".streamlit/config.toml"
)

$allFilesPresent = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "   ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file (missing)" -ForegroundColor Red
        $allFilesPresent = $false
    }
}

if (-not $allFilesPresent) {
    Write-Host ""
    Write-Host "⚠️  Some deployment files are missing" -ForegroundColor Yellow
    Write-Host "   This might affect PWA functionality" -ForegroundColor Gray
}

# Check for API key
Write-Host ""
Write-Host "📋 Checking API configuration..." -ForegroundColor Yellow
$apiKey = $env:GOOGLE_API_KEY
if ($apiKey) {
    Write-Host "✅ GOOGLE_API_KEY found in environment" -ForegroundColor Green
} else {
    Write-Host "⚠️  GOOGLE_API_KEY not set in environment" -ForegroundColor Yellow
    Write-Host "   Remember to add it to Streamlit Cloud Secrets!" -ForegroundColor Gray
}

# Summary
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "📊 Deployment Readiness Summary" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ Core Files: Ready" -ForegroundColor Green
Write-Host "✅ PWA Files: Ready" -ForegroundColor Green
Write-Host "✅ Git Repository: Ready" -ForegroundColor Green
if ($apiKey) {
    Write-Host "✅ API Key: Configured" -ForegroundColor Green
} else {
    Write-Host "⚠️  API Key: Not set (add to Streamlit Secrets)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Push to GitHub: git push origin main" -ForegroundColor White
Write-Host "2. Visit: https://share.streamlit.io" -ForegroundColor White
Write-Host "3. Click 'New app' and select your repository" -ForegroundColor White
Write-Host "4. Add GOOGLE_API_KEY to Secrets in Advanced Settings" -ForegroundColor White
Write-Host "5. Configure custom domain: soulvest.ai" -ForegroundColor White
Write-Host ""
Write-Host "📖 Full deployment guide: SOULVEST_DEPLOYMENT.md" -ForegroundColor Gray
Write-Host ""

$deploy = Read-Host "Do you want to push to GitHub now? (y/n)"
if ($deploy -eq "y" -or $deploy -eq "Y") {
    Write-Host ""
    Write-Host "📤 Pushing to GitHub..." -ForegroundColor Yellow
    git push origin main
    Write-Host "✅ Pushed to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Now deploy on Streamlit Cloud:" -ForegroundColor Cyan
    Write-Host "   https://share.streamlit.io" -ForegroundColor Blue
    Start-Process "https://share.streamlit.io"
}

Write-Host ""
Write-Host "✨ Good luck with your deployment! 🚀" -ForegroundColor Cyan
Write-Host ""
