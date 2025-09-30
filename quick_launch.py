#!/usr/bin/env python3
"""
YSense™ v4.1 Quick Launcher
Simple launcher that finds available port and starts Streamlit
"""

import subprocess
import sys
import socket
import time

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

def main():
    print("🚀 YSense™ v4.1 Quick Launcher")
    print("=" * 50)
    
    # Find available port
    port = find_available_port(8501, 10)
    if port is None:
        print("❌ No available ports found (8501-8510)")
        print("Please close other applications using these ports")
        input("Press Enter to exit...")
        return
    
    print(f"🔍 Found available port: {port}")
    print(f"🎨 Starting YSense™ v4.1 on http://localhost:{port}")
    print("=" * 50)
    
    try:
        # Start Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", str(port), "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 YSense™ v4.1 stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()

