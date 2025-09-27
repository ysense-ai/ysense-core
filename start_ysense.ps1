# YSense Platform v3.0 - PowerShell Startup Script

Write-Host "🚀 Starting YSense Platform v3.0..." -ForegroundColor Green
Write-Host ""

# Start Backend API
Write-Host "📡 Starting Backend API on port 8003..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn src.main:app --port 8003"

# Wait for backend to start
Write-Host "⏳ Waiting 3 seconds for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Start Frontend UI
Write-Host "🌐 Starting Frontend UI on port 8501..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "streamlit run streamlit_app.py --server.port 8501"

Write-Host ""
Write-Host "✅ YSense Platform v3.0 is starting!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access your platform:" -ForegroundColor White
Write-Host "   Frontend: http://localhost:8501" -ForegroundColor Blue
Write-Host "   Backend:  http://localhost:8003" -ForegroundColor Blue
Write-Host "   API Docs: http://localhost:8003/docs" -ForegroundColor Blue
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")



