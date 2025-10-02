#!/usr/bin/env python3
"""
Simple Test for Crypto Authentication
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src.crypto_auth import CryptoAuthManager
    print("✅ CryptoAuthManager imported successfully")
    
    # Test basic functionality
    crypto_auth = CryptoAuthManager()
    print("✅ CryptoAuthManager initialized")
    
    # Test keypair generation
    private_key, public_key = crypto_auth.generate_crypto_keypair()
    print(f"✅ Keypair generated - Private: {private_key[:20]}..., Public: {public_key[:20]}...")
    
    # Test user creation
    result = crypto_auth.create_user("test_user", "test_pass", "Standard")
    if result['success']:
        print("✅ User creation test passed")
        print(f"   User ID: {result['user_id']}")
        print(f"   Private Key: {result['private_key'][:20]}...")
    else:
        print(f"❌ User creation failed: {result['error']}")
    
    # Test authentication
    auth_result = crypto_auth.authenticate_user("test_user", "test_pass")
    if auth_result:
        print("✅ Authentication test passed")
        print(f"   Username: {auth_result['username']}")
        print(f"   Tier: {auth_result['tier']}")
    else:
        print("❌ Authentication failed")
    
    print("\n🎉 Basic crypto authentication tests completed!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")





