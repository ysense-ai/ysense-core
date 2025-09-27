# YSense Platform v4.0 - PowerShell Launch Script
# One-click launch for YSense Platform v4.0

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  YSense Platform v4.0 - LAUNCH SCRIPT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting YSense Platform v4.0..." -ForegroundColor Green
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python detected: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "⚠️  Virtual environment not found" -ForegroundColor Yellow
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ ERROR: Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
}

Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR: Failed to activate virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install/update requirements
Write-Host "Installing/updating requirements..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Some packages may not have installed correctly" -ForegroundColor Yellow
    Write-Host "Continuing anyway..." -ForegroundColor Yellow
}
Write-Host "✅ Requirements installed" -ForegroundColor Green
Write-Host ""

# Check if database exists, if not create it
if (-not (Test-Path "ysense_local.db")) {
    Write-Host "Creating database..." -ForegroundColor Yellow
    python scripts/init_db.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Database initialization had issues" -ForegroundColor Yellow
        Write-Host "Continuing anyway..." -ForegroundColor Yellow
    }
    Write-Host "✅ Database created" -ForegroundColor Green
} else {
    Write-Host "✅ Database found" -ForegroundColor Green
}
Write-Host ""

# Start backend in background
Write-Host "Starting FastAPI backend (Port 8003)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& 'venv\Scripts\Activate.ps1'; python -m uvicorn src.main:app --port 8003 --reload" -WindowStyle Normal

# Wait a moment for backend to start
Write-Host "Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Start frontend in background
Write-Host "Starting Streamlit frontend (Port 8501)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& 'venv\Scripts\Activate.ps1'; streamlit run streamlit_app.py --server.port 8501" -WindowStyle Normal

# Wait a moment for frontend to start
Write-Host "Waiting for frontend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  YSense Platform v4.0 - LAUNCHED!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Backend API: http://localhost:8003" -ForegroundColor Green
Write-Host "🌐 Frontend UI: http://localhost:8501" -ForegroundColor Green
Write-Host "📚 API Docs: http://localhost:8003/docs" -ForegroundColor Green
Write-Host ""
Write-Host "✅ Both services are starting up..." -ForegroundColor Green
Write-Host "✅ Check the opened windows for any errors" -ForegroundColor Green
Write-Host ""

# Open browser to frontend
Write-Host "Opening platform in your browser..." -ForegroundColor Yellow
Start-Process "http://localhost:8501"

Write-Host ""
Write-Host "🎉 YSense Platform v4.0 is now running!" -ForegroundColor Green
Write-Host ""
Write-Host "To stop the platform:" -ForegroundColor Yellow
Write-Host "1. Close the two PowerShell windows that opened" -ForegroundColor White
Write-Host "2. Or press Ctrl+C in each window" -ForegroundColor White
Write-Host ""
Write-Host "Enjoy using YSense Platform v4.0!" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"



