@echo off
echo 🚀 YSense Platform v3.0 - Backup Script
echo.

REM Create timestamped backup folder
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%"

set "backup_folder=YSense_v3.0_Demo_Backup_%timestamp%"

echo 📁 Creating backup folder: %backup_folder%
mkdir "%backup_folder%"

echo.
echo 📋 Copying project files...
xcopy "YSense™ Platform v3.0 - Complete Project Structure" "%backup_folder%" /E /I /H /Y /Q

echo.
echo 💾 Backing up database...
if exist "ysense_local.db" (
    copy "ysense_local.db" "%backup_folder%\ysense_v3.0_backup_%YYYY%-%MM%-%DD%.db"
    echo ✅ Database backed up successfully
) else (
    echo ⚠️  Database file not found
)

echo.
echo 📝 Creating backup documentation...
echo YSense Platform v3.0 Backup > "%backup_folder%\BACKUP_INFO.txt"
echo Created: %date% %time% >> "%backup_folder%\BACKUP_INFO.txt"
echo Source: YSense™ Platform v3.0 - Complete Project Structure >> "%backup_folder%\BACKUP_INFO.txt"
echo Purpose: Demo preservation before v4.0 development >> "%backup_folder%\BACKUP_INFO.txt"
echo. >> "%backup_folder%\BACKUP_INFO.txt"
echo Features Preserved: >> "%backup_folder%\BACKUP_INFO.txt"
echo - Crypto Key Authentication >> "%backup_folder%\BACKUP_INFO.txt"
echo - Z Protocol Consent Management >> "%backup_folder%\BACKUP_INFO.txt"
echo - Revenue Tracking System >> "%backup_folder%\BACKUP_INFO.txt"
echo - Multi-jurisdiction Compliance >> "%backup_folder%\BACKUP_INFO.txt"
echo - Complete Audit Trail >> "%backup_folder%\BACKUP_INFO.txt"

echo.
echo ✅ Backup completed successfully!
echo 📁 Backup location: %backup_folder%
echo.
echo 🎯 This backup preserves your v3.0 demo for:
echo    - Client presentations
echo    - Testing and validation
echo    - Reference during v4.0 development
echo.
echo Press any key to exit...
pause > nul



