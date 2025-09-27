#!/usr/bin/env python3
"""
Test script for YSense registration endpoint
"""

import requests
import json

def test_registration():
    """Test user registration"""
    url = "http://localhost:8003/api/v3/auth/register"
    
    data = {
        "username": "testuser",
        "email": "test@example.com", 
        "age": 25,
        "jurisdiction": "Malaysia",
        "cultural_context": "Global",
        "consent_data_collection": True,
        "consent_commercial_use": True,
        "consent_ai_training": True,
        "consent_revenue_sharing": True,
        "consent_attribution": True,
        "consent_terms": True
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registration successful!")
            result = response.json()
            print(f"Username: {result.get('username')}")
            print(f"User ID: {result.get('user_id')}")
            print(f"Crypto Key: {result.get('crypto_key')}")
            print(f"Z Protocol Consent Key: {result.get('z_protocol_consent_key')}")
            print("🔑 Save both keys for future use!")
        else:
            print("❌ Registration failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_registration()
