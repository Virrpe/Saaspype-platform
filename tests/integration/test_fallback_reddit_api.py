#!/usr/bin/env python3
"""
Test Fallback Reddit API
Direct test of the fallback mechanism
"""

import asyncio
import requests
import json

async def test_fallback_directly():
    """Test the fallback Reddit API directly"""
    print("🧪 Testing Reddit Fallback API Directly")
    print("=" * 50)
    
    try:
        # Test direct requests to Reddit's public JSON API
        subreddit = "startups"
        url = f"https://www.reddit.com/r/{subreddit}/new.json"
        
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Luciq:discovery-engine:v2.1 (by /u/luciq_bot)'
        })
        
        print(f"🔗 Making request to: {url}")
        response = session.get(url, params={'limit': 10}, timeout=10)
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📦 Response size: {len(response.content)} bytes")
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            print(f"✅ Successfully fetched {len(posts)} raw posts")
            
            if posts:
                sample_post = posts[0].get('data', {})
                print(f"\n📝 Sample post:")
                print(f"   Title: {sample_post.get('title', '')[:80]}...")
                print(f"   Author: {sample_post.get('author', 'Unknown')}")
                print(f"   Score: {sample_post.get('score', 0)}")
                print(f"   Comments: {sample_post.get('num_comments', 0)}")
                print(f"   Is self post: {sample_post.get('is_self', False)}")
                print(f"   Created: {sample_post.get('created_utc', 0)}")
            
            return True
        else:
            print(f"❌ Request failed with status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_discovery_service_fallback():
    """Test the discovery service fallback mechanism"""
    print("\n🔧 Testing Discovery Service Fallback")
    print("=" * 50)
    
    try:
        from src.api.services.discovery_service import DiscoveryService
        
        discovery = DiscoveryService()
        print("✅ Discovery service initialized")
        
        # Force use fallback by calling it directly
        posts = await discovery._fallback_fetch_posts("startups", 3)
        
        print(f"✅ Fallback fetched {len(posts)} posts")
        
        if posts:
            sample_post = posts[0]
            print(f"\n📝 Sample processed post:")
            print(f"   Title: {sample_post.get('title', '')[:80]}...")
            print(f"   Author: {sample_post.get('author', 'Unknown')}")
            print(f"   Score: {sample_post.get('score', 0)}")
            print(f"   Comments: {sample_post.get('num_comments', 0)}")
            print(f"   Retrieved via: {sample_post.get('retrieved_via', 'unknown')}")
            print(f"   Business score: {sample_post.get('business_context', {}).get('business_score', 0):.2f}")
            print(f"   Spam detected: {sample_post.get('spam_analysis', {}).get('is_spam', False)}")
        
        return len(posts) > 0
        
    except Exception as e:
        print(f"❌ Discovery service error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🚀 Reddit Fallback API Test")
    print("=" * 60)
    
    # Test 1: Direct API test
    direct_success = await test_fallback_directly()
    
    # Test 2: Discovery service test
    discovery_success = await test_discovery_service_fallback()
    
    print(f"\n🎯 Test Results:")
    print(f"Direct API: {'✅ PASS' if direct_success else '❌ FAIL'}")
    print(f"Discovery Service: {'✅ PASS' if discovery_success else '❌ FAIL'}")
    
    if direct_success and discovery_success:
        print(f"\n🎉 All tests passed! Fallback mechanism is working.")
    else:
        print(f"\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    asyncio.run(main()) 