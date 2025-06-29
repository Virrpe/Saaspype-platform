#!/usr/bin/env python3
"""
Reddit API Integration Test
Tests the new Reddit API client and discovery service
"""

import sys
import asyncio
import requests
import json
from pathlib import Path

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent / "src"))

from src.api.services.reddit_api_client import reddit_api_client
from src.api.services.discovery_service import DiscoveryService
from src.shared.config.reddit_config import reddit_config, get_reddit_api_setup_instructions

class RedditAPITester:
    """Test suite for Reddit API integration"""
    
    def __init__(self):
        self.reddit_client = reddit_api_client
        self.discovery_service = DiscoveryService()
        self.base_url = "http://localhost:8000"
        
    def test_reddit_config(self) -> bool:
        """Test Reddit API configuration"""
        print("🔧 Testing Reddit API Configuration")
        print("=" * 50)
        
        status = reddit_config.get_credentials_status()
        
        print(f"Client ID Set: {'✅' if status['client_id_set'] else '❌'}")
        print(f"Client Secret Set: {'✅' if status['client_secret_set'] else '❌'}")
        print(f"User Agent: {status['user_agent']}")
        print(f"Configured: {'✅' if status['configured'] else '❌'}")
        print(f"Fallback Enabled: {'✅' if status['fallback_enabled'] else '❌'}")
        
        if not status['configured']:
            print("\n⚠️  Reddit API credentials not configured")
            print("System will use fallback public API for testing")
            print("\nTo set up Reddit API credentials:")
            print(get_reddit_api_setup_instructions())
        
        return True
    
    async def test_reddit_client_direct(self) -> bool:
        """Test Reddit API client directly"""
        print("\n🔌 Testing Reddit API Client (Direct)")
        print("=" * 50)
        
        try:
            # Test authentication
            auth_result = await self.reddit_client.authenticate()
            print(f"Authentication: {'✅ SUCCESS' if auth_result else '❌ FAILED (using fallback)'}")
            
            # Test fetching posts
            posts = await self.reddit_client.get_subreddit_posts(
                subreddit="entrepreneur",
                limit=3
            )
            
            if posts:
                print(f"✅ Posts Retrieved: {len(posts)} posts from r/entrepreneur")
                for i, post in enumerate(posts[:2], 1):
                    print(f"   {i}. {post['title'][:60]}...")
                    print(f"      Score: {post['score']}, Comments: {post['num_comments']}")
                return True
            else:
                print("❌ No posts retrieved from Reddit API")
                return False
                
        except Exception as e:
            print(f"❌ Reddit API Client test failed: {e}")
            return False
    
    async def test_discovery_service(self) -> bool:
        """Test discovery service with Reddit API"""
        print("\n🕵️ Testing Discovery Service")
        print("=" * 50)
        
        try:
            result = await self.discovery_service.discover_pain_points(
                subreddit="startups",
                limit=3
            )
            
            if result and result.get('posts_analyzed', 0) > 0:
                print(f"✅ Discovery Service: {result['posts_analyzed']} posts analyzed")
                print(f"   Pain Points Found: {result['pain_points_found']}")
                print(f"   Opportunities: {len(result.get('ranked_opportunities', []))}")
                print(f"   Concepts: {len(result.get('generated_concepts', []))}")
                
                # Show Reddit API status
                api_status = result.get('reddit_api_status', {})
                print(f"   API Requests Made: {api_status.get('requests_made', 0)}")
                print(f"   API Integration: {result.get('api_integration', 'unknown')}")
                
                return True
            else:
                print(f"❌ Discovery Service failed: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ Discovery Service test failed: {e}")
            return False
    
    async def test_api_endpoint(self) -> bool:
        """Test the API endpoint"""
        print("\n🌐 Testing API Endpoint")
        print("=" * 50)
        
        try:
            # First test authentication endpoint
            auth_response = requests.post(
                f"{self.base_url}/auth/login",
                json={
                    "email": "test@gmail.com",
                    "password": "TestPass123!"
                }
            )
            
            if auth_response.status_code == 200:
                token = auth_response.json()['access_token']
                print("✅ Authentication successful")
                
                # Test discovery endpoint
                discovery_response = requests.post(
                    f"{self.base_url}/api/discover",
                    json={
                        "subreddit": "entrepreneur",
                        "limit": 3
                    },
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    }
                )
                
                if discovery_response.status_code == 200:
                    data = discovery_response.json()
                    print(f"✅ Discovery API: {data.get('posts_analyzed', 0)} posts analyzed")
                    print(f"   Pain Points: {data.get('pain_points_found', 0)}")
                    print(f"   API Integration: {data.get('api_integration', 'unknown')}")
                    return True
                else:
                    print(f"❌ Discovery API failed: {discovery_response.status_code}")
                    print(f"   Response: {discovery_response.text}")
                    return False
            else:
                print(f"❌ Authentication failed: {auth_response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ API Endpoint test failed: {e}")
            return False
    
    def test_rate_limiting(self) -> bool:
        """Test rate limiting functionality"""
        print("\n⏱️ Testing Rate Limiting")
        print("=" * 50)
        
        try:
            rate_status = self.reddit_client.get_rate_limit_status()
            
            print(f"Requests Made: {rate_status['requests_made']}")
            print(f"Requests Remaining: {rate_status['requests_remaining']}")
            print(f"Authenticated: {'✅' if rate_status['authenticated'] else '❌'}")
            
            if rate_status['last_request_time']:
                print(f"Last Request: {rate_status['last_request_time']}")
            
            print("✅ Rate limiting system operational")
            return True
            
        except Exception as e:
            print(f"❌ Rate limiting test failed: {e}")
            return False

async def main():
    """Run all Reddit API integration tests"""
    print("🚀 REDDIT API INTEGRATION TEST SUITE")
    print("=" * 60)
    
    tester = RedditAPITester()
    results = []
    
    # Test configuration
    results.append(("Configuration", tester.test_reddit_config()))
    
    # Test Reddit client directly
    results.append(("Reddit Client", await tester.test_reddit_client_direct()))
    
    # Test discovery service
    results.append(("Discovery Service", await tester.test_discovery_service()))
    
    # Test rate limiting
    results.append(("Rate Limiting", tester.test_rate_limiting()))
    
    # Test API endpoint
    results.append(("API Endpoint", await tester.test_api_endpoint()))
    
    # Summary
    print("\n" + "=" * 60)
    print("🏁 TEST SUITE SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nSuccess Rate: {passed}/{total} ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL REDDIT API INTEGRATION TESTS PASSED!")
        print("Task 2: Reddit API Integration - COMPLETE")
    else:
        print(f"\n⚠️  {total-passed} tests failed. Reddit API integration needs attention.")
        
        if not reddit_config.is_configured():
            print("\n💡 Tip: Set up Reddit API credentials for full functionality")
            print("For now, the system will use public Reddit JSON API as fallback")
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 