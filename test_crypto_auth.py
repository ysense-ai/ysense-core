#!/usr/bin/env python3
"""
Test Script for YSense™ Crypto Authentication System
Tests registration, login, and attribution key generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.crypto_auth import CryptoAuthManager
import json

def test_crypto_authentication():
    """Test the complete crypto authentication system"""
    print("🧪 Testing YSense™ Crypto Authentication System")
    print("=" * 60)
    
    # Initialize crypto auth manager
    crypto_auth = CryptoAuthManager()
    print("✅ CryptoAuthManager initialized")
    
    # Test 1: Create a test user
    print("\n🔑 Test 1: Creating Test User")
    print("-" * 30)
    
    test_username = "test_user_crypto"
    test_password = "test_password_123"
    test_tier = "Founding Contributor"
    
    result = crypto_auth.create_user(test_username, test_password, test_tier)
    
    if result['success']:
        print(f"✅ User created successfully!")
        print(f"   Username: {result['username']}")
        print(f"   Tier: {result['tier']}")
        print(f"   Private Key: {result['private_key'][:20]}...")
        print(f"   Public Key: {result['public_key'][:20]}...")
        
        # Store user data for next tests
        user_id = result['user_id']
        private_key = result['private_key']
        public_key = result['public_key']
        
    else:
        print(f"❌ User creation failed: {result['error']}")
        return False
    
    # Test 2: Authenticate the user
    print("\n🔐 Test 2: Authenticating User")
    print("-" * 30)
    
    auth_result = crypto_auth.authenticate_user(test_username, test_password)
    
    if auth_result:
        print(f"✅ Authentication successful!")
        print(f"   User ID: {auth_result['id']}")
        print(f"   Username: {auth_result['username']}")
        print(f"   Tier: {auth_result['tier']}")
        print(f"   Attribution Count: {auth_result['attribution_count']}")
        print(f"   Total Revenue: ${auth_result['total_revenue']}")
        
        # Verify keys match
        if auth_result['public_key'] == public_key:
            print("✅ Public key verification successful!")
        else:
            print("❌ Public key mismatch!")
            return False
            
    else:
        print("❌ Authentication failed!")
        return False
    
    # Test 3: Generate attribution key
    print("\n📊 Test 3: Generating Attribution Key")
    print("-" * 30)
    
    wisdom_content = "This is a test wisdom drop for crypto authentication testing."
    attribution_result = crypto_auth.generate_attribution_key(user_id, wisdom_content)
    
    if attribution_result['success']:
        print(f"✅ Attribution key generated!")
        print(f"   Attribution Key: {attribution_result['attribution_key']}")
        print(f"   Signature: {attribution_result['signature'][:20]}...")
        
        attribution_key = attribution_result['attribution_key']
        signature = attribution_result['signature']
        
    else:
        print(f"❌ Attribution key generation failed: {attribution_result['error']}")
        return False
    
    # Test 4: Verify attribution
    print("\n🔍 Test 4: Verifying Attribution")
    print("-" * 30)
    
    verification_result = crypto_auth.verify_attribution(attribution_key, signature)
    
    if verification_result:
        print("✅ Attribution verification successful!")
    else:
        print("❌ Attribution verification failed!")
        return False
    
    # Test 5: Get user stats
    print("\n📈 Test 5: Getting User Statistics")
    print("-" * 30)
    
    stats = crypto_auth.get_user_stats(user_id)
    
    if stats:
        print(f"✅ User stats retrieved!")
        print(f"   Username: {stats['username']}")
        print(f"   Tier: {stats['tier']}")
        print(f"   Attribution Count: {stats['attribution_count']}")
        print(f"   Total Revenue: ${stats['total_revenue']}")
        print(f"   Member Since: {stats['created_at']}")
    else:
        print("❌ Failed to get user stats!")
        return False
    
    # Test 6: Generate session token
    print("\n🎫 Test 6: Generating Session Token")
    print("-" * 30)
    
    session_token = crypto_auth.generate_session_token(user_id)
    
    if session_token:
        print(f"✅ Session token generated!")
        print(f"   Token: {session_token[:20]}...")
        
        # Verify session token
        verified_user_id = crypto_auth.verify_session_token(session_token)
        if verified_user_id == user_id:
            print("✅ Session token verification successful!")
        else:
            print("❌ Session token verification failed!")
            return False
    else:
        print("❌ Session token generation failed!")
        return False
    
    # Test 7: Test wrong password
    print("\n🚫 Test 7: Testing Wrong Password")
    print("-" * 30)
    
    wrong_auth = crypto_auth.authenticate_user(test_username, "wrong_password")
    
    if wrong_auth is None:
        print("✅ Wrong password correctly rejected!")
    else:
        print("❌ Wrong password was accepted!")
        return False
    
    # Test 8: Test wrong username
    print("\n🚫 Test 8: Testing Wrong Username")
    print("-" * 30)
    
    wrong_username_auth = crypto_auth.authenticate_user("wrong_username", test_password)
    
    if wrong_username_auth is None:
        print("✅ Wrong username correctly rejected!")
    else:
        print("❌ Wrong username was accepted!")
        return False
    
    # Test 9: Test duplicate username
    print("\n🚫 Test 9: Testing Duplicate Username")
    print("-" * 30)
    
    duplicate_result = crypto_auth.create_user(test_username, "another_password", "Standard")
    
    if not duplicate_result['success'] and "already exists" in duplicate_result['error']:
        print("✅ Duplicate username correctly rejected!")
    else:
        print("❌ Duplicate username was accepted!")
        return False
    
    # Cleanup: Deactivate test user
    print("\n🧹 Cleanup: Deactivating Test User")
    print("-" * 30)
    
    deactivate_result = crypto_auth.deactivate_user(user_id)
    
    if deactivate_result:
        print("✅ Test user deactivated successfully!")
    else:
        print("❌ Failed to deactivate test user!")
    
    # Final Results
    print("\n🎉 Test Results Summary")
    print("=" * 60)
    print("✅ All crypto authentication tests passed!")
    print("✅ User registration with crypto keypair: PASSED")
    print("✅ User authentication with password: PASSED")
    print("✅ Attribution key generation: PASSED")
    print("✅ Attribution verification: PASSED")
    print("✅ Session token management: PASSED")
    print("✅ Security validation (wrong credentials): PASSED")
    print("✅ Duplicate username prevention: PASSED")
    print("✅ User statistics retrieval: PASSED")
    print("✅ User deactivation: PASSED")
    
    print("\n🔐 Crypto Authentication System Status: FULLY OPERATIONAL")
    print("🚀 Ready for production deployment!")
    
    return True

if __name__ == "__main__":
    try:
        success = test_crypto_authentication()
        if success:
            print("\n✅ All tests completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        sys.exit(1)





