#!/usr/bin/env python3
"""
Luciq Quality Dashboard Testing Script
Tests authentication and Quality Dashboard API endpoints
"""

import requests
import json
import sys

# Configuration
API_BASE = "http://localhost:8000"
TEST_USER = {
    "name": "Test User",
    "email": "test@luciq.com", 
    "password": "testpass123",
    "company": "Luciq Testing"
}

def test_signup_and_auth():
    """Test user signup and authentication"""
    print("🔧 Testing Luciq Quality Dashboard Authentication...")
    
    # Step 1: Create test user account
    print("\n1. Creating test user account...")
    try:
        signup_response = requests.post(f"{API_BASE}/api/signup", json=TEST_USER)
        if signup_response.status_code == 200:
            print("✅ Test user created successfully")
            signup_data = signup_response.json()
            token = signup_data['access_token']
        else:
            print(f"ℹ️  User might already exist, trying login...")
            # Try login instead
            login_response = requests.post(f"{API_BASE}/api/login", json={
                "email": TEST_USER["email"],
                "password": TEST_USER["password"]
            })
            if login_response.status_code == 200:
                print("✅ Login successful")
                login_data = login_response.json() 
                token = login_data['access_token']
            else:
                print(f"❌ Authentication failed: {login_response.text}")
                return None
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return None
    
    return token

def test_quality_endpoints(token):
    """Test Quality Dashboard API endpoints"""
    print("\n2. Testing Quality Dashboard API endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test quality metrics
    print("   Testing /api/quality/metrics...")
    try:
        response = requests.get(f"{API_BASE}/api/quality/metrics", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Quality metrics endpoint working")
            print(f"   📊 Quality rate: {data.get('current_validation', {}).get('total_signals_processed', 0)} signals processed")
            print(f"   🌐 Platforms: {data.get('cross_platform_intelligence', {}).get('platforms_configured', 0)} configured")
        else:
            print(f"   ❌ Quality metrics failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Quality metrics error: {e}")
    
    # Test quality trends
    print("   Testing /api/quality/trends...")
    try:
        response = requests.get(f"{API_BASE}/api/quality/trends", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Quality trends endpoint working")
            print(f"   📈 Trends data points: {len(data.get('trends', []))}")
            print(f"   🎯 Average quality: {data.get('summary', {}).get('average_quality_rate', 'N/A')}%")
        else:
            print(f"   ❌ Quality trends failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Quality trends error: {e}")
    
    # Test quality alerts
    print("   Testing /api/quality/alerts...")
    try:
        response = requests.get(f"{API_BASE}/api/quality/alerts", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Quality alerts endpoint working")
            print(f"   🚨 Active alerts: {data.get('alert_summary', {}).get('total', 0)}")
        else:
            print(f"   ❌ Quality alerts failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Quality alerts error: {e}")

def generate_browser_setup(token):
    """Generate JavaScript code to set up browser authentication"""
    print("\n3. Browser Setup Instructions:")
    print("   To access the Quality Dashboard in your browser:")
    print("   1. Open: http://localhost:3000/pages/quality-dashboard.html")
    print("   2. Open browser Developer Tools (F12)")
    print("   3. Go to Console tab")
    print("   4. Paste this code and press Enter:")
    print(f"""
   localStorage.setItem('access_token', '{token}');
   localStorage.setItem('token', '{token}');
   location.reload();
   """)
    print("   5. The Quality Dashboard should now load successfully!")

def main():
    print("=" * 60)
    print("🚀 Luciq Quality Dashboard Test Suite")
    print("=" * 60)
    
    # Test authentication
    token = test_signup_and_auth()
    if not token:
        print("\n❌ Authentication failed - cannot test Quality Dashboard")
        sys.exit(1)
    
    # Test Quality Dashboard endpoints
    test_quality_endpoints(token)
    
    # Provide browser setup instructions
    generate_browser_setup(token)
    
    print("\n" + "=" * 60)
    print("🎉 Quality Dashboard Testing Complete!")
    print("=" * 60)
    print(f"\n📊 Quality Dashboard URL: http://localhost:3000/pages/quality-dashboard.html")
    print(f"🔑 Auth Token: {token[:20]}...")
    print(f"👤 Test User: {TEST_USER['email']}")

if __name__ == "__main__":
    main() 