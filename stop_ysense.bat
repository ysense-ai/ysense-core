@echo off
echo 🛑 YSense Platform v3.0 - Stop Script
echo.

echo 🔍 Stopping all YSense processes...
taskkill /f /im python.exe 2>nul
if %errorlevel% equ 0 (
    echo ✅ All Python processes stopped
) else (
    echo ℹ️  No Python processes found
)

echo.
echo 🔍 Checking if ports are free...
netstat -ano | findstr :8003 >nul
if %errorlevel% equ 0 (
    echo ⚠️  Port 8003 still in use
) else (
    echo ✅ Port 8003 is free
)

netstat -ano | findstr :8501 >nul
if %errorlevel% equ 0 (
    echo ⚠️  Port 8501 still in use
) else (
    echo ✅ Port 8501 is free
)

echo.
echo 🎯 YSense Platform stopped successfully!
echo.
echo To restart, run: start_ysense_smart.bat
echo.
pause



