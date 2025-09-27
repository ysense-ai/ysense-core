@echo off
echo 🚀 Starting YSense Platform v3.0...
echo.

echo 📡 Starting Backend API on port 8003...
start "YSense Backend" cmd /k "python -m uvicorn src.main:app --port 8003"

echo ⏳ Waiting 3 seconds for backend to start...
timeout /t 3 /nobreak > nul

echo 🌐 Starting Frontend UI on port 8501...
start "YSense Frontend" cmd /k "streamlit run streamlit_app.py --server.port 8501"

echo.
echo ✅ YSense Platform v3.0 is starting!
echo.
echo 🌐 Access your platform:
echo    Frontend: http://localhost:8501
echo    Backend:  http://localhost:8003
echo    API Docs: http://localhost:8003/docs
echo.
echo Press any key to exit...
pause > nul



