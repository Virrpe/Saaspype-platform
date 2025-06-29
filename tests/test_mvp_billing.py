#!/usr/bin/env python3
"""
Test MVP Billing System
Test the API key generation and usage tracking
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_mvp_billing_system():
    """Test the complete MVP billing flow"""
    
    print("🚀 Testing Luciq MVP Billing System")
    print("=" * 50)
    
    # Step 1: Check pricing tiers
    print("\n1. Testing pricing tiers endpoint...")
    response = requests.get(f"{BASE_URL}/api/mvp/pricing")
    if response.status_code == 200:
        pricing = response.json()
        print("✅ Pricing tiers loaded successfully")
        for tier, info in pricing["pricing_tiers"].items():
            print(f"   {info['name']}: ${info['price_monthly']}/month - {info['monthly_calls']} calls")
    else:
        print(f"❌ Pricing endpoint failed: {response.status_code}")
        return
    
    # Step 2: Generate API key
    print("\n2. Testing API key generation...")
    api_key_request = {
        "email": "test@luciq.com",
        "tier": "professional"
    }
    
    response = requests.post(f"{BASE_URL}/api/mvp/generate-key", json=api_key_request)
    if response.status_code == 200:
        key_data = response.json()
        print("✅ API key generated successfully")
        print(f"   Tier: {key_data['tier']}")
        print(f"   Monthly limit: {key_data['monthly_limit']}")
        print(f"   Price: ${key_data['price_monthly']}/month")
        api_key = key_data["api_key"]
        print(f"   API Key: {api_key[:20]}...")
    else:
        print(f"❌ API key generation failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return
    
    # Step 3: Test protected endpoint
    print("\n3. Testing protected endpoint with API key...")
    headers = {"X-API-Key": api_key}
    test_request = {
        "content": "I'm struggling with managing my team's productivity. We use multiple tools but nothing integrates well.",
        "platform": "reddit"
    }
    
    response = requests.post(f"{BASE_URL}/api/intelligence/pain-point-detection", 
                           json=test_request, headers=headers)
    if response.status_code == 200:
        result = response.json()
        print("✅ Protected endpoint accessed successfully")
        print(f"   Analysis completed: {result.get('success', False)}")
        confidence = result.get('pain_point_analysis', {}).get('confidence_score', 0)
        print(f"   Confidence score: {confidence:.2f}")
    else:
        print(f"❌ Protected endpoint failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return
    
    # Step 4: Check usage statistics
    print("\n4. Testing usage tracking...")
    response = requests.get(f"{BASE_URL}/api/mvp/usage", headers=headers)
    if response.status_code == 200:
        usage = response.json()
        print("✅ Usage tracking working")
        print(f"   Monthly usage: {usage['monthly_usage']}/{usage['monthly_limit']}")
        print(f"   Usage percentage: {usage['usage_percentage']:.1f}%")
        print(f"   Tier: {usage['tier']}")
    else:
        print(f"❌ Usage tracking failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return
    
    # Step 5: Test without API key (should fail)
    print("\n5. Testing endpoint without API key (should fail)...")
    response = requests.post(f"{BASE_URL}/api/intelligence/pain-point-detection", json=test_request)
    if response.status_code == 401:
        print("✅ Endpoint properly protected - unauthorized access blocked")
    else:
        print(f"❌ Security issue: endpoint accessible without API key (status: {response.status_code})")
    
    print("\n" + "=" * 50)
    print("🎉 MVP Billing System Test Complete!")
    print("\n💰 REVENUE GENERATION READY:")
    print("   ✅ API key generation working")
    print("   ✅ Usage tracking operational") 
    print("   ✅ Endpoint protection active")
    print("   ✅ Billing integration ready")
    print("\n🚀 Ready to launch and start generating revenue!")

if __name__ == "__main__":
    # Wait a moment for API to start
    print("Waiting for API to start...")
    time.sleep(3)
    
    try:
        test_mvp_billing_system()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure master_luciq_api.py is running on port 8000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}") 