#!/usr/bin/env python3
"""
YSense Platform v4.0 - One-Click Launcher
Launches both backend and frontend with a single command
"""

import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("  🚀 YSense Platform v4.0 - ONE-CLICK LAUNCHER")
    print("=" * 60)
    print()

def check_python():
    """Check if Python is available"""
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        print(f"✅ Python detected: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"❌ ERROR: Python not available - {e}")
        return False

def check_venv():
    """Check and create virtual environment if needed"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("⚠️  Virtual environment not found")
        print("Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print("✅ Virtual environment created")
        except subprocess.CalledProcessError:
            print("❌ ERROR: Failed to create virtual environment")
            return False
    else:
        print("✅ Virtual environment found")
    return True

def install_requirements():
    """Install requirements"""
    print("Installing/updating requirements...")
    try:
        # Determine the correct pip path
        if os.name == 'nt':  # Windows
            pip_path = Path("venv/Scripts/pip.exe")
        else:  # Unix/Linux/Mac
            pip_path = Path("venv/bin/pip")
        
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt", "--quiet"], 
                      check=True)
        print("✅ Requirements installed")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Some packages may not have installed correctly")
        print("Continuing anyway...")
        return True

def check_database():
    """Check and create database if needed"""
    if not Path("ysense_local.db").exists():
        print("Creating database...")
        try:
            if os.name == 'nt':  # Windows
                python_path = Path("venv/Scripts/python.exe")
            else:  # Unix/Linux/Mac
                python_path = Path("venv/bin/python")
            
            subprocess.run([str(python_path), "scripts/init_db.py"], check=True)
            print("✅ Database created")
        except subprocess.CalledProcessError:
            print("⚠️  Database initialization had issues")
            print("Continuing anyway...")
    else:
        print("✅ Database found")

def start_backend():
    """Start the FastAPI backend"""
    print("Starting FastAPI backend (Port 8003)...")
    try:
        if os.name == 'nt':  # Windows
            python_path = Path("venv/Scripts/python.exe")
        else:  # Unix/Linux/Mac
            python_path = Path("venv/bin/python")
        
        # Start backend in background
        if os.name == 'nt':  # Windows
            subprocess.Popen([
                "cmd", "/c", "start", "YSense Backend",
                str(python_path), "-m", "uvicorn", "src.main:app", 
                "--port", "8003", "--reload"
            ], shell=True)
        else:  # Unix/Linux/Mac
            subprocess.Popen([
                str(python_path), "-m", "uvicorn", "src.main:app", 
                "--port", "8003", "--reload"
            ])
        
        print("✅ Backend started")
        return True
    except Exception as e:
        print(f"❌ ERROR: Failed to start backend - {e}")
        return False

def start_frontend():
    """Start the Streamlit frontend"""
    print("Starting Streamlit frontend (Port 8501)...")
    try:
        if os.name == 'nt':  # Windows
            python_path = Path("venv/Scripts/python.exe")
        else:  # Unix/Linux/Mac
            python_path = Path("venv/bin/python")
        
        # Start frontend in background
        if os.name == 'nt':  # Windows
            subprocess.Popen([
                "cmd", "/c", "start", "YSense Frontend",
                str(python_path), "-m", "streamlit", "run", "streamlit_app.py", 
                "--server.port", "8501"
            ], shell=True)
        else:  # Unix/Linux/Mac
            subprocess.Popen([
                str(python_path), "-m", "streamlit", "run", "streamlit_app.py", 
                "--server.port", "8501"
            ])
        
        print("✅ Frontend started")
        return True
    except Exception as e:
        print(f"❌ ERROR: Failed to start frontend - {e}")
        return False

def open_browser():
    """Open browser to the platform"""
    print("Opening platform in your browser...")
    time.sleep(2)  # Wait for services to start
    try:
        webbrowser.open("http://localhost:8501")
        print("✅ Browser opened")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically - {e}")
        print("Please manually open: http://localhost:8501")

def main():
    """Main launcher function"""
    print_banner()
    
    # Check Python
    if not check_python():
        input("Press Enter to exit...")
        return
    
    # Check virtual environment
    if not check_venv():
        input("Press Enter to exit...")
        return
    
    # Install requirements
    install_requirements()
    
    # Check database
    check_database()
    
    print()
    print("=" * 60)
    print("  🚀 LAUNCHING YSense Platform v4.0")
    print("=" * 60)
    print()
    
    # Start backend
    if not start_backend():
        input("Press Enter to exit...")
        return
    
    # Wait for backend to start
    print("Waiting for backend to start...")
    time.sleep(3)
    
    # Start frontend
    if not start_frontend():
        input("Press Enter to exit...")
        return
    
    # Wait for frontend to start
    print("Waiting for frontend to start...")
    time.sleep(3)
    
    print()
    print("=" * 60)
    print("  🎉 YSense Platform v4.0 - LAUNCHED!")
    print("=" * 60)
    print()
    print("🚀 Backend API: http://localhost:8003")
    print("🌐 Frontend UI: http://localhost:8501")
    print("📚 API Docs: http://localhost:8003/docs")
    print()
    print("✅ Both services are starting up...")
    print("✅ Check the opened windows for any errors")
    print()
    
    # Open browser
    open_browser()
    
    print()
    print("🎉 YSense Platform v4.0 is now running!")
    print()
    print("To stop the platform:")
    print("1. Close the opened terminal/command windows")
    print("2. Or press Ctrl+C in each window")
    print()
    print("Enjoy using YSense Platform v4.0!")
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()



