@echo off
echo.
echo ========================================
echo   YSense Platform v4.0 - LAUNCH SCRIPT
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

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ⚠️  Virtual environment not found
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
)

echo ✅ Virtual environment found
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activated
echo.

REM Install/update requirements
echo Installing/updating requirements...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ⚠️  Some packages may not have installed correctly
    echo Continuing anyway...
)
echo ✅ Requirements installed
echo.

REM Check if database exists, if not create it
if not exist "ysense_local.db" (
    echo Creating database...
    python scripts/init_db.py
    if errorlevel 1 (
        echo ⚠️  Database initialization had issues
        echo Continuing anyway...
    )
    echo ✅ Database created
) else (
    echo ✅ Database found
)
echo.

REM Start backend in background
echo Starting FastAPI backend (Port 8003)...
start "YSense Backend" cmd /k "call venv\Scripts\activate.bat && python -m uvicorn src.main:app --port 8003 --reload"

REM Wait a moment for backend to start
echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

REM Start frontend in background
echo Starting Streamlit frontend (Port 8501)...
start "YSense Frontend" cmd /k "call venv\Scripts\activate.bat && streamlit run streamlit_app.py --server.port 8501"

REM Wait a moment for frontend to start
echo Waiting for frontend to start...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   YSense Platform v4.0 - LAUNCHED!
echo ========================================
echo.
echo 🚀 Backend API: http://localhost:8003
echo 🌐 Frontend UI: http://localhost:8501
echo 📚 API Docs: http://localhost:8003/docs
echo.
echo ✅ Both services are starting up...
echo ✅ Check the opened windows for any errors
echo.
echo Press any key to open the platform in your browser...
pause >nul

REM Open browser to frontend
start http://localhost:8501

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



