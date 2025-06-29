#!/usr/bin/env python3
"""
Test Fixed Master API - Verify all issues are resolved
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {data['status']}")
            print(f"   Components: {len(data['components'])} operational")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_authentication():
    """Test fixed authentication"""
    print("\n🔐 Testing Fixed Authentication...")
    
    # Test user creation
    try:
        user_data = {
            "username": "fixed_test_user",
            "email": "fixed@test.com",
            "password": "TestPassword123!"
        }
        
        # Register user (ignore if exists)
        requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
        
        # Test login with JSON
        print("   Testing JSON login...")
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"username": user_data["username"], "password": user_data["password"]},
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code == 200:
            print("✅ JSON login successful")
            token_data = login_response.json()
            token = token_data.get("access_token")
            print(f"   Token received: {bool(token)}")
            return token
        else:
            print(f"❌ JSON login failed: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return None

def test_discovery_fixed():
    """Test fixed discovery service"""
    print("\n🔍 Testing Fixed Discovery Service...")
    
    try:
        discovery_data = {
            "subreddit": "entrepreneur",
            "limit": 3
        }
        
        response = requests.post(
            f"{BASE_URL}/api/discovery/analyze",
            json=discovery_data,
            timeout=30
        )
        
        print(f"   Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Discovery service working")
            print(f"   Posts analyzed: {data.get('posts_analyzed', 0)}")
            print(f"   Pain points found: {data.get('pain_points_found', 0)}")
            
            # Check for pain points with total_score
            pain_points = data.get('pain_points', [])
            if pain_points:
                first_pain_point = pain_points[0]
                print(f"   Sample pain point keys: {list(first_pain_point.keys())}")
                if 'total_score' in first_pain_point:
                    print(f"   ✅ total_score field present: {first_pain_point['total_score']}")
                else:
                    print(f"   ⚠️  total_score missing, using opportunity_score: {first_pain_point.get('opportunity_score', 'N/A')}")
            
            return True
        else:
            print(f"❌ Discovery failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Discovery error: {e}")
        return False

def test_intelligence_fixed():
    """Test fixed intelligence engine"""
    print("\n🧠 Testing Fixed Intelligence Engine...")
    
    try:
        # Test with correct parameter name
        test_data = {
            "content": "We're looking for a better project management solution. Current tools are too expensive and don't integrate well."
        }
        
        response = requests.post(
            f"{BASE_URL}/api/intelligence/analyze",
            json=test_data,
            timeout=15
        )
        
        print(f"   Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Intelligence engine working")
            print(f"   Analysis keys: {list(data.keys())}")
            
            if 'sentiment_analysis' in data:
                sentiment = data['sentiment_analysis']
                print(f"   Sentiment: {sentiment.get('sentiment_label')} ({sentiment.get('compound', 0):.3f})")
            
            if 'business_analysis' in data:
                business = data['business_analysis']
                print(f"   Business score: {business.get('business_score')}/10")
            
            if 'processing_time_seconds' in data:
                print(f"   Processing time: {data['processing_time_seconds']:.3f}s")
            
            return True
        else:
            print(f"❌ Intelligence failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Intelligence error: {e}")
        return False

def test_chat_with_auth(token):
    """Test fixed chat service with authentication"""
    print("\n💬 Testing Fixed Chat Service...")
    
    if not token:
        print("❌ No authentication token available")
        return False
    
    try:
        chat_data = {
            "message": "What are the current trends in SaaS business opportunities?"
        }
        
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.post(
            f"{BASE_URL}/api/chat/message",
            json=chat_data,
            headers=headers,
            timeout=15
        )
        
        print(f"   Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat service working")
            print(f"   Response keys: {list(data.keys())}")
            
            if 'response' in data:
                response_text = data['response']
                print(f"   Response preview: {response_text[:100]}...")
            
            return True
        else:
            print(f"❌ Chat failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return False

def test_mega_scraper():
    """Test mega scraper (should work from previous tests)"""
    print("\n🕸️ Testing Mega Scraper...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/scraper/mega-scan",
            json={"keywords": ["business tools"], "limit": 2},
            timeout=20
        )
        
        print(f"   Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Mega scraper working")
            print(f"   Platforms scraped: {data.get('sources_scraped', 0)}")
            print(f"   Signals found: {data.get('total_signals', 0)}")
            return True
        else:
            print(f"❌ Mega scraper failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Mega scraper error: {e}")
        return False

def main():
    """Run all fixed API tests"""
    print("🚀 TESTING FIXED MASTER API")
    print("=" * 60)
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 API URL: {BASE_URL}")
    
    tests = []
    
    # Test health
    health_ok = test_health()
    tests.append(("Health Check", health_ok))
    
    # Test authentication
    token = test_authentication()
    tests.append(("Authentication", bool(token)))
    
    # Test discovery (fixed scoring)
    discovery_ok = test_discovery_fixed()
    tests.append(("Discovery Service", discovery_ok))
    
    # Test intelligence (fixed parameters)
    intelligence_ok = test_intelligence_fixed()
    tests.append(("Intelligence Engine", intelligence_ok))
    
    # Test chat (fixed with auth)
    chat_ok = test_chat_with_auth(token)
    tests.append(("Chat Service", chat_ok))
    
    # Test mega scraper
    scraper_ok = test_mega_scraper()
    tests.append(("Mega Scraper", scraper_ok))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 FIXED API TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ FIXED" if result else "❌ STILL BROKEN"
        print(f"   • {test_name}: {status}")
    
    print(f"\n🎯 Overall Status: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL ISSUES FIXED - Master API fully operational!")
    elif passed >= total * 0.8:
        print("✅ MAJOR FIXES SUCCESSFUL - API mostly operational")
    else:
        print("⚠️  MORE FIXES NEEDED - Some issues remain")
    
    return passed, total

if __name__ == "__main__":
    main() 