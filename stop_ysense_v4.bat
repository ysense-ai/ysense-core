@echo off
chcp 65001 > nul
echo 🛑 Stopping YSense Platform v4.0...
echo.

echo 🔎 Identifying and terminating v4.0 processes...
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /NH ^| findstr /I "uvicorn streamlit"') do (
    echo Terminating PID: %%a
    taskkill /PID %%a /F >nul 2>&1
)
echo.

echo ⏳ Waiting 2 seconds for processes to fully terminate and ports to be released...
timeout /t 2 /nobreak > nul
echo.

echo ✅ YSense Platform v4.0 has been stopped.
echo You can now safely restart the platform or close this window.
echo.
pause



