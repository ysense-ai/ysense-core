#!/usr/bin/env python3
"""
YSense Platform v4.0 - API Setup Test Script
Test your API keys and platform functionality
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment_setup():
    """Test if .env file is properly configured"""
    print("🔍 Testing Environment Setup...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("   Please create .env file with your API keys")
        return False
    
    print("✅ .env file found")
    
    # Check required environment variables
    required_vars = [
        'QWEN_API_KEY',
        'ANTHROPIC_API_KEY',
        'SECRET_KEY',
        'JWT_SECRET_KEY',
        'ENCRYPTION_KEY'
    ]
    
    missing_vars = []
    placeholder_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        elif 'your_' in value or 'sk-ant-your' in value:
            placeholder_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    if placeholder_vars:
        print(f"⚠️  Placeholder values detected: {', '.join(placeholder_vars)}")
        print("   Please replace with actual API keys")
        return False
    
    print("✅ All environment variables configured")
    return True

def test_qwen_api():
    """Test QWEN API connection"""
    print("\n🧠 Testing QWEN API...")
    
    try:
        from src.qwen_integration import QWENClient
        
        client = QWENClient()
        
        if client.use_fallback:
            print("⚠️  QWEN API using fallback mode (no API key)")
            return False
        
        # Test with a simple message
        import asyncio
        
        async def test_qwen():
            messages = [
                {"role": "user", "content": "Hello, this is a test message for YSense platform."}
            ]
            
            response = await client.create_completion(
                messages=messages,
                temperature=0.7,
                max_tokens=100
            )
            
            return response
        
        response = asyncio.run(test_qwen())
        
        if response and len(response) > 10:
            print("✅ QWEN API working correctly")
            print(f"   Response: {response[:100]}...")
            return True
        else:
            print("❌ QWEN API response too short or empty")
            return False
            
    except Exception as e:
        print(f"❌ QWEN API error: {e}")
        return False

def test_anthropic_api():
    """Test Anthropic API connection"""
    print("\n🤖 Testing Anthropic API...")
    
    try:
        from src.anthropic_integration import AnthropicClient
        
        client = AnthropicClient()
        
        if client.use_fallback:
            print("⚠️  Anthropic API using fallback mode (no API key)")
            return False
        
        # Test with a simple message
        import asyncio
        
        async def test_anthropic():
            messages = [
                {"role": "user", "content": "Hello, this is a test message for YSense platform."}
            ]
            
            response = await client.create_completion(
                messages=messages,
                temperature=0.7,
                max_tokens=100
            )
            
            return response
        
        response = asyncio.run(test_anthropic())
        
        if response and len(response) > 10:
            print("✅ Anthropic API working correctly")
            print(f"   Response: {response[:100]}...")
            return True
        else:
            print("❌ Anthropic API response too short or empty")
            return False
            
    except Exception as e:
        print(f"❌ Anthropic API error: {e}")
        return False

def test_platform_functionality():
    """Test overall platform functionality"""
    print("\n🚀 Testing Platform Functionality...")
    
    try:
        # Test if we can import main components
        from src.main import app
        from src.models import create_tables
        from api.wisdom_v4 import router as wisdom_router
        
        print("✅ Core platform components imported successfully")
        
        # Test database connection
        create_tables()
        print("✅ Database connection working")
        
        # Test API routes
        routes = [route.path for route in app.routes if hasattr(route, 'path')]
        expected_routes = ['/health', '/api/v4/wisdom/analyze-story', '/api/v4/wisdom/create-wisdom-drop']
        
        for route in expected_routes:
            if any(route in r for r in routes):
                print(f"✅ Route {route} found")
            else:
                print(f"⚠️  Route {route} not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Platform functionality error: {e}")
        return False

def main():
    """Run all tests"""
    print("🎯 YSense Platform v4.0 - API Setup Test")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("QWEN API", test_qwen_api),
        ("Anthropic API", test_anthropic_api),
        ("Platform Functionality", test_platform_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 CONGRATULATIONS!")
        print("Your YSense platform is fully configured and ready for production!")
        print("\nNext steps:")
        print("1. Start your platform: python -m uvicorn src.main:app --host 0.0.0.0 --port 8004")
        print("2. Start frontend: streamlit run streamlit_v4_app.py --server.port 8502")
        print("3. Visit: http://localhost:8502")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above and:")
        print("1. Ensure your .env file is properly configured")
        print("2. Verify your API keys are correct")
        print("3. Check your internet connection")
        print("4. Review the API_SETUP_GUIDE.md for detailed instructions")

if __name__ == "__main__":
    main()
