#!/usr/bin/env python3
"""
Test Z Protocol consent lookup functionality
"""

import requests
import json

def test_consent_lookup():
    """Test looking up user by Z Protocol consent key"""
    url = "http://localhost:8003/api/v3/auth/consent/lookup/2d9ad-3c8bf-42407-09624-8b2ae-06d68-79f23-002fb"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Consent lookup successful!")
            result = response.json()
            print(f"Username: {result.get('username')}")
            print(f"Email: {result.get('email')}")
            print(f"Jurisdiction: {result.get('jurisdiction')}")
            print(f"Z Protocol Tier: {result.get('z_protocol_tier')}")
            print(f"Consent Version: {result.get('consent_version')}")
            print(f"Account Status: {result.get('account_status')}")
        else:
            print("❌ Consent lookup failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_consent_lookup()



