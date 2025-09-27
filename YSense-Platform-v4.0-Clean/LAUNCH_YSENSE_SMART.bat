@echo off
echo.
echo ========================================
echo   YSense Platform v4.0 - SMART LAUNCHER
echo ========================================
echo.
echo Starting YSense Platform v4.0...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo ✅ Python detected
echo.

REM Kill any existing processes on our ports
echo Checking for existing processes...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8003') do (
    echo Killing process on port 8003...
    taskkill /f /pid %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501') do (
    echo Killing process on port 8501...
    taskkill /f /pid %%a >nul 2>&1
)

echo ✅ Ports cleared
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
) else (
    echo ⚠️  Virtual environment not found - using system Python
)
echo.

REM Start backend in background
echo Starting FastAPI backend (Port 8003)...
start "YSense Backend" cmd /k "if exist venv\Scripts\activate.bat (call venv\Scripts\activate.bat) && python -m uvicorn src.main:app --port 8003 --reload"

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

REM Check if backend started successfully
netstat -an | findstr :8003 >nul
if errorlevel 1 (
    echo ❌ Backend failed to start on port 8003
    echo Trying alternative port 8004...
    start "YSense Backend" cmd /k "if exist venv\Scripts\activate.bat (call venv\Scripts\activate.bat) && python -m uvicorn src.main:app --port 8004 --reload"
    set BACKEND_PORT=8004
) else (
    echo ✅ Backend started successfully on port 8003
    set BACKEND_PORT=8003
)

REM Start frontend in background
echo Starting Streamlit frontend (Port 8501)...
start "YSense Frontend" cmd /k "if exist venv\Scripts\activate.bat (call venv\Scripts\activate.bat) && streamlit run streamlit_app.py --server.port 8501"

REM Wait for frontend to start
echo Waiting for frontend to start...
timeout /t 5 /nobreak >nul

REM Check if frontend started successfully
netstat -an | findstr :8501 >nul
if errorlevel 1 (
    echo ❌ Frontend failed to start on port 8501
    echo Trying alternative port 8502...
    start "YSense Frontend" cmd /k "if exist venv\Scripts\activate.bat (call venv\Scripts\activate.bat) && streamlit run streamlit_app.py --server.port 8502"
    set FRONTEND_PORT=8502
) else (
    echo ✅ Frontend started successfully on port 8501
    set FRONTEND_PORT=8501
)

echo.
echo ========================================
echo   YSense Platform v4.0 - LAUNCHED!
echo ========================================
echo.
echo 🚀 Backend API: http://localhost:%BACKEND_PORT%
echo 🌐 Frontend UI: http://localhost:%FRONTEND_PORT%
echo 📚 API Docs: http://localhost:%BACKEND_PORT%/docs
echo.
echo ✅ Both services are starting up...
echo ✅ Check the opened windows for any errors
echo.
echo Press any key to open the platform in your browser...
pause >nul

REM Open browser to frontend
start http://localhost:%FRONTEND_PORT%

echo.
echo 🎉 YSense Platform v4.0 is now running!
echo.
echo To stop the platform:
echo 1. Close the two command windows that opened
echo 2. Or press Ctrl+C in each window
echo.
echo Enjoy using YSense Platform v4.0!
echo.
pause
