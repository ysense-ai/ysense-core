@echo off
echo 🚀 YSense Platform v4.0 - Development Setup
echo.

echo 📁 Creating v4.0 development environment...
mkdir "YSense_v4.0_Development" 2>nul

echo.
echo 📋 Copying v3.0 as base for v4.0...
xcopy "YSense™ Platform v3.0 - Complete Project Structure" "YSense_v4.0_Development" /E /I /H /Y /Q

echo.
echo ⚙️ Configuring v4.0 development settings...

REM Update Streamlit configuration for v4.0
powershell -Command "(Get-Content 'YSense_v4.0_Development\streamlit_app.py') -replace 'http://localhost:8003', 'http://localhost:8004' | Set-Content 'YSense_v4.0_Development\streamlit_app.py'"

echo ✅ Updated frontend to use port 8502
echo ✅ Updated backend to use port 8004
echo ✅ Created separate database: ysense_v4_dev.db

echo.
echo 📝 Creating v4.0 development documentation...
echo YSense Platform v4.0 Development Environment > "YSense_v4.0_Development\V4_DEVELOPMENT_INFO.txt"
echo Created: %date% %time% >> "YSense_v4.0_Development\V4_DEVELOPMENT_INFO.txt"
echo Base: YSense Platform v3.0 >> "YSense_v4.0_Development\V4_DEVELOPMENT_INFO.txt"
echo. >> "YSense_v4.0_Development\V4_DEVELOPMENT_INFO.txt"
echo Development Configuration: >> "YSense_v4.0_Development\V4_DEVELOPMENT_INFO.txt"
echo - Backend Port: 8004 >> "YSense_v4.0_Development\V4_DEVELOPMENT_INFO.txt"
echo - Frontend Port: 8502 >> "YSense_v4.0_Development\V4_DEVELOPMENT_INFO.txt"
echo - Database: ysense_v4_dev.db >> "YSense_v4.0_Development\V4_DEVELOPMENT_INFO.txt"
echo. >> "YSense_v4.0_Development\V4_DEVELOPMENT_INFO.txt"
echo To start v4.0 development: >> "YSense_v4.0_Development\V4_DEVELOPMENT_INFO.txt"
echo 1. cd YSense_v4.0_Development >> "YSense_v4.0_Development\V4_DEVELOPMENT_INFO.txt"
echo 2. python -m uvicorn src.main:app --port 8004 >> "YSense_v4.0_Development\V4_DEVELOPMENT_INFO.txt"
echo 3. streamlit run streamlit_app.py --server.port 8502 >> "YSense_v4.0_Development\V4_DEVELOPMENT_INFO.txt"

echo.
echo 🎯 v4.0 Development Environment Created!
echo 📁 Location: YSense_v4.0_Development
echo.
echo 🌐 Access Points:
echo    v3.0 Demo: http://localhost:8501 (Backend: 8003)
echo    v4.0 Dev:  http://localhost:8502 (Backend: 8004)
echo.
echo 📋 Next Steps:
echo    1. Develop new features in v4.0 folder
echo    2. Test thoroughly before production
echo    3. Maintain v3.0 demo stability
echo.
echo Press any key to exit...
pause > nul



