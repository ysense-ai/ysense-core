@echo off
echo 🚀 YSense Platform v3.0 - Smart Startup Script
echo.

echo 🔍 Checking for existing processes...
echo.

REM Kill any existing Python processes that might be using our ports
echo 🛑 Stopping any existing YSense processes...
taskkill /f /im python.exe 2>nul
if %errorlevel% equ 0 (
    echo ✅ Existing processes stopped
) else (
    echo ℹ️  No existing processes found
)

echo.
echo ⏳ Waiting 2 seconds for ports to be released...
timeout /t 2 /nobreak > nul

echo.
echo 📡 Starting Backend API on port 8003...
start "YSense Backend" cmd /k "python -m uvicorn src.main:app --port 8003"

echo ⏳ Waiting 5 seconds for backend to fully start...
timeout /t 5 /nobreak > nul

echo.
echo 🌐 Starting Frontend UI on port 8501...
start "YSense Frontend" cmd /k "streamlit run streamlit_app.py --server.port 8501"

echo.
echo ✅ YSense Platform v3.0 is starting!
echo.
echo 🌐 Access your platform:
echo    Frontend: http://localhost:8501
echo    Backend:  http://localhost:8003
echo    API Docs: http://localhost:8003/docs
echo.
echo 📝 Note: This script automatically stops any existing processes
echo    to prevent port conflicts. Safe to run multiple times!
echo.
echo Press any key to exit...
pause > nul



