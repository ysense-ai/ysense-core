@echo off
echo ============================================================
echo YSense™ v4.1 Fresh Platform Launcher
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📥 Installing requirements...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found
    echo Please create .env file from env_template.txt
    echo.
)

REM Launch the platform
echo 🚀 Launching YSense™ v4.1 Platform...
python launch_ysense_v41.py

pause




