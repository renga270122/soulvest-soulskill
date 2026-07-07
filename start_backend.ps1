# Start SoulSkill API Server
Write-Host "Starting SoulSkill API Server..." -ForegroundColor Cyan
Set-Location D:\Personal\soulskill
& D:\Personal\soulskill\.venv\Scripts\Activate.ps1
python api_server.py
