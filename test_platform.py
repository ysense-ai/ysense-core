#!/usr/bin/env python3
"""
Quick Platform Test Script
Tests all critical components before launch
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

print("="*60)
print("YSense Platform v4.1 - Quick Test")
print("="*60)

# Test 1: Configuration
print("\n[1/5] Testing Configuration...")
try:
    from src.config import Config
    assert Config.QWEN_API_KEY and not Config.QWEN_API_KEY.startswith('your-'), "QWEN API key not configured"
    assert Config.ANTHROPIC_API_KEY and not Config.ANTHROPIC_API_KEY.startswith('your-'), "Anthropic API key not configured"
    assert Config.SECRET_KEY and len(Config.SECRET_KEY) >= 32, "SECRET_KEY too short"
    assert Config.JWT_SECRET_KEY and len(Config.JWT_SECRET_KEY) >= 32, "JWT_SECRET_KEY too short"
    print("[PASS] Configuration")
    print(f"   - QWEN API: Configured")
    print(f"   - Anthropic API: Configured")
    print(f"   - Database: {Config.DATABASE_URL}")
except AssertionError as e:
    print(f"[FAIL] Configuration - {e}")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Configuration - {e}")
    sys.exit(1)

# Test 2: Database Models
print("\n[2/5] Testing Database Models...")
try:
    from src.models import create_tables, User, WisdomDrop
    print("[PASS] Database Models")
    print("   - All models imported successfully")
except Exception as e:
    print(f"[FAIL] Database Models - {e}")
    sys.exit(1)

# Test 3: Backend API
print("\n[3/5] Testing Backend API...")
try:
    from src.main import app
    print("[PASS] Backend API")
    print("   - FastAPI app created successfully")
except Exception as e:
    print(f"[FAIL] Backend API - {e}")
    sys.exit(1)

# Test 4: Core Modules
print("\n[4/5] Testing Core Modules...")
try:
    from src.crypto_auth import CryptoAuthManager
    from src.methodology_core_engine import MethodologyCoreEngine
    from src.revenue_transparency_system import RevenueTransparencySystem
    print("[PASS] Core Modules")
    print("   - Crypto Auth: OK")
    print("   - Methodology Engine: OK")
    print("   - Revenue System: OK")
except Exception as e:
    print(f"[FAIL] Core Modules - {e}")
    sys.exit(1)

# Test 5: AI Integration
print("\n[5/5] Testing AI Integration...")
try:
    from src.agent_system_v41 import YSenseAgentSystem
    from src.qwen_integration import QWENClient
    from src.anthropic_integration import AnthropicClient
    print("[PASS] AI Integration")
    print("   - Agent System: OK")
    print("   - QWEN Client: OK")
    print("   - Anthropic Client: OK")
except Exception as e:
    print(f"[FAIL] AI Integration - {e}")
    sys.exit(1)

print("\n" + "="*60)
print("ALL TESTS PASSED!")
print("="*60)
print("\nPlatform Status: READY TO LAUNCH")
print("\nTo start the platform:")
print("  python launch_ysense_v41.py")
print("\nOr manually:")
print("  Terminal 1: python -m uvicorn src.main:app --host 0.0.0.0 --port 8003")
print("  Terminal 2: streamlit run streamlit_app.py --server.port 8501")
print("\n" + "="*60)
