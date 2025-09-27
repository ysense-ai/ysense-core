@echo off
chcp 65001 > nul
echo 🚀 YSense Platform v4.0 - Independent Launch
echo.

echo 🔎 Checking for existing processes...
tasklist /FI "IMAGENAME eq python.exe" /NH | find /I "python.exe" >nul
if %errorlevel% equ 0 (
    echo 🛑 Stopping any existing YSense processes...
    for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /NH') do (
        taskkill /PID %%a /F >nul 2>&1
    )
    echo ✅ Existing processes stopped
) else (
    echo ✅ No existing processes found
)
echo.

echo ⏳ Waiting 2 seconds for ports to be released...
timeout /t 2 /nobreak > nul
echo.

echo ⚙️ Starting YSense v4.0 Backend API on port 8004...
start "YSense v4.0 Backend" cmd /k "python -m uvicorn src.main:app --port 8004 --host 127.0.0.1"
echo ⏳ Waiting 5 seconds for backend to fully start...
timeout /t 5 /nobreak > nul
echo.

echo 🌐 Starting YSense v4.0 Frontend UI on port 8502...
start "YSense v4.0 Frontend" cmd /k "streamlit run streamlit_v4_app.py --server.port 8502"
echo.

echo 🎉 YSense Platform v4.0 is launching independently!
echo.
echo 🔗 Access your v4.0 platform:
echo    Frontend: http://localhost:8502
echo    Backend:  http://localhost:8004
echo    API Docs: http://localhost:8004/docs
echo.
echo ✨ Features:
echo    🤖 AI-Powered Story Analysis
echo    🌊 Enhanced Deep Vibe Distillation
echo    🔑 Crypto Key Recovery System
echo    💭 Human Experience Respected
echo.
echo 💡 Note: This is the independent v4.0 launch
echo    No version selection needed - pure v4.0 experience!
echo.
pause



