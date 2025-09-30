#!/usr/bin/env python3
"""
YSense™ v4.1 Fresh Launcher
Clean startup script for the YSense platform
"""

import subprocess
import sys
import os
import time
import socket
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        import sqlalchemy
        import fastapi
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists"""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
        return True
    else:
        print("⚠️  .env file not found")
        print("Please create .env file from env_template.txt")
        return False

def find_available_port(start_port=8501, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def launch_backend():
    """Launch FastAPI backend"""
    print("🚀 Starting YSense™ v4.1 Backend...")
    try:
        # Start backend in background
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "src.main:app", 
            "--host", "0.0.0.0", "--port", "8003", "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for startup
        time.sleep(3)
        
        if backend_process.poll() is None:
            print("✅ Backend started successfully on http://localhost:8003")
            return backend_process
        else:
            print("❌ Backend failed to start")
            return None
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def launch_frontend():
    """Launch Streamlit frontend"""
    print("🎨 Starting YSense™ v4.1 Frontend...")
    try:
        # Find available port
        port = find_available_port(8501, 10)
        if port is None:
            print("❌ No available ports found for frontend")
            return None
        
        print(f"🔍 Using port {port} for frontend")
        
        # Start frontend on available port
        frontend_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", str(port), "--server.headless", "true"
        ])
        
        # Wait a moment for startup
        time.sleep(3)
        
        if frontend_process.poll() is None:
            print(f"✅ Frontend started successfully on http://localhost:{port}")
            return frontend_process
        else:
            print("❌ Frontend failed to start")
            return None
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None

def main():
    """Main launcher function"""
    print("=" * 60)
    print("🌟 YSense™ v4.1 Fresh Platform Launcher")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        return
    
    # Check env file
    check_env_file()
    
    # Launch backend
    backend_process = launch_backend()
    if not backend_process:
        print("❌ Cannot start platform without backend")
        return
    
    # Launch frontend
    frontend_process = launch_frontend()
    if not frontend_process:
        print("❌ Cannot start platform without frontend")
        backend_process.terminate()
        return
    
    print("\n" + "=" * 60)
    print("🎉 YSense™ v4.1 Platform Started Successfully!")
    print("=" * 60)
    print("🌐 Frontend: http://localhost:8501")
    print("🔧 Backend API: http://localhost:8003")
    print("📚 API Docs: http://localhost:8003/docs")
    print("=" * 60)
    print("Press Ctrl+C to stop the platform")
    
    try:
        # Wait for processes
        while True:
            time.sleep(1)
            if backend_process.poll() is not None:
                print("❌ Backend stopped unexpectedly")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend stopped unexpectedly")
                break
    except KeyboardInterrupt:
        print("\n🛑 Stopping YSense™ v4.1 Platform...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Platform stopped successfully")

if __name__ == "__main__":
    main()



