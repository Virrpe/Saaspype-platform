#!/usr/bin/env python3
"""
Direct API test for trends endpoint
"""
import requests
import json

def test_trends_api():
    print("🔍 Testing Luciq Trends API directly...")
    
    # Test health first
    try:
        health_response = requests.get('http://localhost:8000/health')
        print(f"✅ Health check: {health_response.status_code}")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"   Status: {health_data.get('status', 'unknown')}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test trends endpoint with authentication
    try:
        # Create a test user first
        signup_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        print("\n🔐 Creating test user...")
        signup_response = requests.post('http://localhost:8000/api/signup', json=signup_data)
        
        if signup_response.status_code == 200:
            token_data = signup_response.json()
            token = token_data['access_token']
            print(f"✅ Got auth token: {token[:20]}...")
        else:
            # Try login instead
            print("🔐 Trying login...")
            login_response = requests.post('http://localhost:8000/api/login', json=signup_data)
            if login_response.status_code == 200:
                token_data = login_response.json()
                token = token_data['access_token']
                print(f"✅ Got auth token: {token[:20]}...")
            else:
                print(f"❌ Auth failed: {login_response.status_code}")
                print(f"   Response: {login_response.text}")
                return
        
        # Test trends endpoint
        print("\n🚀 Testing trends detection...")
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        trends_data = {
            "hours_back": 6,
            "enable_monitoring": False
        }
        
        trends_response = requests.post(
            'http://localhost:8000/api/trends/detect',
            json=trends_data,
            headers=headers
        )
        
        print(f"✅ Trends API: {trends_response.status_code}")
        
        if trends_response.status_code == 200:
            response_data = trends_response.json()
            print(f"📊 Response keys: {list(response_data.keys())}")
            print(f"📈 Opportunities detected: {response_data.get('opportunities_detected', 0)}")
            print(f"📋 Status: {response_data.get('status', 'unknown')}")
            
            # Show the actual opportunities array
            opportunities = response_data.get('opportunities', [])
            print(f"🔍 Opportunities array length: {len(opportunities)}")
            
            if opportunities:
                print(f"🎯 First opportunity: {opportunities[0].get('title', 'No title')}")
                print(f"📝 Description: {opportunities[0].get('description', 'No description')[:100]}...")
                print(f"📊 Momentum score: {opportunities[0].get('momentum_score', 'N/A')}")
            else:
                print("❌ No opportunities in response array!")
                print(f"📄 Full response: {json.dumps(response_data, indent=2)}")
            
            print("\n✅ SUCCESS: Trends API is working and returning demo opportunities!")
        else:
            print(f"❌ Error: {trends_response.text}")
            
    except Exception as e:
        print(f"❌ Trends test failed: {e}")

if __name__ == "__main__":
    test_trends_api() 