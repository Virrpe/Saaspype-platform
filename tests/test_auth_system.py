#!/usr/bin/env python3
"""
Simple test script to verify API authentication system
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_api_authentication():
    """Test the API authentication system"""
    print("🔐 Testing Luciq API Authentication System")
    print("=" * 50)
    
    # Step 1: Test API health
    print("\n1. Testing API health...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is healthy and running")
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to API: {e}")
        print("   Make sure master_luciq_api.py is running on port 8000")
        return False
    
    # Step 2: Test pricing endpoint (public)
    print("\n2. Testing pricing endpoint (public)...")
    try:
        response = requests.get(f"{BASE_URL}/api/mvp/pricing")
        if response.status_code == 200:
            pricing_data = response.json()
            print("✅ Pricing endpoint working")
            print(f"   Available tiers: {list(pricing_data['pricing_tiers'].keys())}")
        else:
            print(f"❌ Pricing endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Pricing endpoint error: {e}")
        return False
    
    # Step 3: Generate API key
    print("\n3. Testing API key generation...")
    api_key_request = {
        "email": "test@example.com",
        "tier": "professional"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/mvp/generate-key", json=api_key_request)
        if response.status_code == 200:
            key_data = response.json()
            print("✅ API key generated successfully")
            print(f"   Tier: {key_data['tier']}")
            print(f"   Monthly limit: {key_data['monthly_limit']}")
            api_key = key_data["api_key"]
            print(f"   API Key: {api_key[:20]}...")
        else:
            print(f"❌ API key generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ API key generation error: {e}")
        return False
    
    # Step 4: Test protected endpoint with API key
    print("\n4. Testing protected endpoint with API key...")
    headers = {"X-API-Key": api_key}
    
    try:
        response = requests.get(f"{BASE_URL}/api/mvp/usage", headers=headers)
        if response.status_code == 200:
            usage_data = response.json()
            print("✅ Protected endpoint accessible with API key")
            print(f"   Usage: {usage_data['monthly_usage']}/{usage_data['monthly_limit']}")
        else:
            print(f"❌ Protected endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Protected endpoint error: {e}")
        return False
    
    # Step 5: Test revenue endpoint with API key
    print("\n5. Testing revenue endpoint with API key...")
    test_request = {
        "content": "I hate manually managing my inventory. It takes hours every day and I always make mistakes.",
        "platform": "test",
        "context": {"test": True}
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/mvp/market-validation", 
                                json=test_request, headers=headers)
        if response.status_code == 200:
            analysis_data = response.json()
            print("✅ Revenue endpoint working with API key")
            print(f"   Success: {analysis_data['success']}")
            print(f"   Usage remaining: {analysis_data['usage_remaining']}")
        else:
            print(f"❌ Revenue endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Revenue endpoint error: {e}")
        return False
    
    # Step 6: Test without API key (should fail)
    print("\n6. Testing endpoint without API key (should fail)...")
    try:
        response = requests.get(f"{BASE_URL}/api/mvp/usage")
        if response.status_code == 401:
            print("✅ Endpoint properly protected - unauthorized access blocked")
        else:
            print(f"❌ Security issue: endpoint accessible without API key (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Security test error: {e}")
        return False
    
    print("\n🎉 API Authentication System Test Complete!")
    print("=" * 50)
    print("✅ All tests passed successfully!")
    print("\n📊 System Status:")
    print("   ✅ API key generation working")
    print("   ✅ Authentication middleware working")
    print("   ✅ Usage tracking operational")
    print("   ✅ Revenue endpoints protected")
    print("   ✅ Security controls active")
    
    return True

if __name__ == "__main__":
    success = test_api_authentication()
    sys.exit(0 if success else 1) 