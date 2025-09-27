@echo off
echo.
echo ========================================
echo   YSense Platform - PORT CLEANER
echo ========================================
echo.
echo Cleaning up ports 8003 and 8501...
echo.

REM Kill processes on port 8003
echo Checking port 8003...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8003') do (
    echo Found process %%a on port 8003, killing...
    taskkill /f /pid %%a >nul 2>&1
    if errorlevel 1 (
        echo Process %%a could not be killed
    ) else (
        echo Process %%a killed successfully
    )
)

REM Kill processes on port 8501
echo Checking port 8501...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501') do (
    echo Found process %%a on port 8501, killing...
    taskkill /f /pid %%a >nul 2>&1
    if errorlevel 1 (
        echo Process %%a could not be killed
    ) else (
        echo Process %%a killed successfully
    )
)

echo.
echo ✅ Port cleanup completed!
echo.
echo You can now run LAUNCH_YSENSE_SMART.bat
echo.
pause



