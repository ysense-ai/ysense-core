#!/usr/bin/env python3
"""
Test login functionality with crypto key
"""

import requests
import json

def test_login():
    """Test user login with crypto key"""
    url = "http://localhost:8003/api/v3/auth/login"
    
    # Use the crypto key from the previous registration
    data = {
        "username_or_email": "testuser",
        "crypto_key": "7070-644b-29c5-03fd-659f-8a18-79b4-87d1"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            result = response.json()
            print(f"Username: {result.get('username')}")
            print(f"User ID: {result.get('user_id')}")
            print(f"Z Protocol Tier: {result.get('z_protocol_tier')}")
            print(f"Crypto Key: {result.get('crypto_key')}")
            print(f"Z Protocol Consent Key: {result.get('z_protocol_consent_key')}")
        else:
            print("❌ Login failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_login()



