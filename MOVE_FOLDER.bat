@echo off
echo ========================================
echo YSense Platform v4.1 - Folder Move Tool
echo ========================================
echo.
echo This will move the platform folder to:
echo Desktop\YSense-Platform-v4.1
echo.
echo Current location:
echo %~dp0
echo.
pause

echo.
echo Moving folder...
cd ..
move "YSense-Platform-v4.1-Fresh" "C:\Users\weibi\OneDrive\Desktop\YSense-Platform-v4.1"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! Folder moved successfully!
    echo ========================================
    echo.
    echo New location: C:\Users\weibi\OneDrive\Desktop\YSense-Platform-v4.1
    echo.
    echo To launch your platform:
    echo   1. Navigate to Desktop\YSense-Platform-v4.1
    echo   2. Run: python launch_ysense_v41.py
    echo.
) else (
    echo.
    echo ========================================
    echo ERROR: Could not move folder
    echo ========================================
    echo.
    echo Possible reasons:
    echo   - Folder is open in File Explorer
    echo   - Terminal is inside the folder
    echo   - Editor has files open
    echo.
    echo Solution:
    echo   1. Close all programs using this folder
    echo   2. Run this script again
    echo.
)

pause
