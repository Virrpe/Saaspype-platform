#!/usr/bin/env python3
"""
Real Platform Connectivity Test
Let's see what we can actually access and get data from!
"""

import asyncio
import aiohttp
import time
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

async def test_reddit_access():
    """Test if we can actually get Reddit data"""
    print("\n🔍 Testing Reddit Access...")
    
    try:
        async with aiohttp.ClientSession() as session:
            url = "https://www.reddit.com/r/startups/hot.json?limit=5"
            
            async with session.get(url) as response:
                print(f"   📡 Status: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    posts = data.get('data', {}).get('children', [])
                    
                    print(f"   ✅ Success: Got {len(posts)} posts")
                    if posts:
                        sample_post = posts[0].get('data', {})
                        print(f"   📝 Sample: '{sample_post.get('title', 'No title')[:60]}...'")
                        print(f"   📊 Score: {sample_post.get('score', 0)}")
                    return True
                else:
                    print(f"   ❌ Failed: HTTP {response.status}")
                    return False
                    
    except Exception as e:
        print(f"   💥 Error: {e}")
        return False

async def test_github_access():
    """Test if we can actually get GitHub data"""
    print("\n🔍 Testing GitHub Access...")
    
    try:
        async with aiohttp.ClientSession() as session:
            url = "https://api.github.com/search/repositories"
            params = {
                'q': 'stars:>1',
                'sort': 'stars',
                'order': 'desc',
                'per_page': 3
            }
            
            async with session.get(url, params=params) as response:
                print(f"   📡 Status: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    repos = data.get('items', [])
                    
                    print(f"   ✅ Success: Got {len(repos)} repositories")
                    if repos:
                        sample_repo = repos[0]
                        print(f"   📝 Sample: '{sample_repo.get('name', 'No name')}'")
                        print(f"   ⭐ Stars: {sample_repo.get('stargazers_count', 0)}")
                    return True
                else:
                    print(f"   ❌ Failed: HTTP {response.status}")
                    if response.status == 403:
                        print(f"   🚫 Rate limited by GitHub")
                    return False
                    
    except Exception as e:
        print(f"   💥 Error: {e}")
        return False

async def test_hackernews_access():
    """Test if we can actually get Hacker News data"""
    print("\n🔍 Testing Hacker News Access...")
    
    try:
        async with aiohttp.ClientSession() as session:
            # First get top story IDs
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            
            async with session.get(url) as response:
                print(f"   📡 Status: {response.status}")
                
                if response.status == 200:
                    story_ids = await response.json()
                    print(f"   ✅ Success: Got {len(story_ids)} story IDs")
                    
                    # Test getting one story detail
                    if story_ids:
                        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_ids[0]}.json"
                        async with session.get(story_url) as story_response:
                            if story_response.status == 200:
                                story = await story_response.json()
                                print(f"   📝 Sample: '{story.get('title', 'No title')[:60]}...'")
                                print(f"   📊 Score: {story.get('score', 0)}")
                                return True
                            else:
                                print(f"   ❌ Story detail failed: HTTP {story_response.status}")
                                return False
                else:
                    print(f"   ❌ Failed: HTTP {response.status}")
                    return False
                    
    except Exception as e:
        print(f"   💥 Error: {e}")
        return False

async def test_flippa_access():
    """Test if we can actually get Flippa data"""
    print("\n🔍 Testing Flippa Access...")
    
    try:
        # Import our enhanced client
        from src.api.domains.discovery.services.flippa_intelligence_client import FlippaIntelligenceClient
        
        client = FlippaIntelligenceClient()
        
        start_time = time.time()
        market_data = await client.discover_marketplace_trends()
        execution_time = time.time() - start_time
        
        print(f"   ⏱️ Execution time: {execution_time:.2f}s")
        
        if market_data and market_data.get('diverse_categories'):
            categories = market_data.get('diverse_categories', [])
            trends = market_data.get('market_trends', [])
            
            print(f"   ✅ Success: Got marketplace data")
            print(f"   📊 Categories: {len(categories)} found")
            print(f"   📈 Trends: {len(trends)} found")
            
            if categories:
                print(f"   📝 Sample categories: {', '.join(categories[:3])}")
            
            # Check if we got real data or fallback
            if market_data.get('data_source') == 'fallback':
                print(f"   ⚠️ Note: Using fallback data (real site may be blocked)")
                await client.close()
                return 'fallback'
            else:
                print(f"   🎉 Real data retrieved!")
                await client.close()
                return True
        else:
            print(f"   ❌ Failed: No data returned")
            await client.close()
            return False
            
    except Exception as e:
        print(f"   💥 Error: {e}")
        return False

async def test_empire_flippers_access():
    """Test if we can actually get Empire Flippers data"""
    print("\n🔍 Testing Empire Flippers Access...")
    
    try:
        from src.api.domains.discovery.services.empire_flippers_client import EmpireFlippersIntelligenceClient
        
        client = EmpireFlippersIntelligenceClient()
        
        start_time = time.time()
        market_data = await client.get_premium_market_intelligence_summary()
        execution_time = time.time() - start_time
        
        print(f"   ⏱️ Execution time: {execution_time:.2f}s")
        
        if market_data and market_data.get('market_overview'):
            overview = market_data.get('market_overview', {})
            categories = overview.get('premium_categories', [])
            
            print(f"   ✅ Success: Got market intelligence")
            print(f"   📊 Categories: {len(categories)} found")
            
            if categories:
                print(f"   📝 Sample categories: {', '.join(categories[:3])}")
            
            await client.close()
            return True
        else:
            print(f"   ❌ Failed: No data returned")
            await client.close()
            return False
            
    except Exception as e:
        print(f"   💥 Error: {e}")
        return False

async def test_acquire_access():
    """Test if we can actually get Acquire.com data"""
    print("\n🔍 Testing Acquire.com Access...")
    
    try:
        from src.api.domains.discovery.services.acquire_intelligence_client import AcquireIntelligenceClient
        
        client = AcquireIntelligenceClient()
        
        start_time = time.time()
        market_data = await client.get_market_intelligence_summary()
        execution_time = time.time() - start_time
        
        print(f"   ⏱️ Execution time: {execution_time:.2f}s")
        
        if market_data and market_data.get('market_overview'):
            overview = market_data.get('market_overview', {})
            categories = overview.get('trending_categories', [])
            
            print(f"   ✅ Success: Got market intelligence")
            print(f"   📊 Categories: {len(categories)} found")
            
            if categories:
                print(f"   📝 Sample categories: {', '.join(categories[:3])}")
            
            await client.close()
            return True
        else:
            print(f"   ❌ Failed: No data returned")
            await client.close()
            return False
            
    except Exception as e:
        print(f"   💥 Error: {e}")
        return False

async def test_twitter_access():
    """Test if we can actually get Twitter data (probably will fail without API key)"""
    print("\n🔍 Testing Twitter Access...")
    
    try:
        from src.api.domains.discovery.services.twitter_intelligence_client import TwitterIntelligenceClient
        
        client = TwitterIntelligenceClient()
        
        start_time = time.time()
        trends_data = await client.discover_realtime_business_trends()
        execution_time = time.time() - start_time
        
        print(f"   ⏱️ Execution time: {execution_time:.2f}s")
        
        if trends_data and (trends_data.get('market_signals') or trends_data.get('founder_pain_points')):
            signals = len(trends_data.get('market_signals', []))
            pain_points = len(trends_data.get('founder_pain_points', []))
            
            print(f"   ✅ Success: Got Twitter intelligence")
            print(f"   📊 Market signals: {signals}")
            print(f"   📈 Pain points: {pain_points}")
            
            await client.close()
            return True
        else:
            print(f"   ❌ Failed: No data returned (likely no API key)")
            await client.close()
            return False
            
    except Exception as e:
        print(f"   💥 Error: {e}")
        print(f"   📝 Note: Twitter requires API credentials")
        return False

async def main():
    """Run comprehensive connectivity tests"""
    print("🔗 Luciq Platform Connectivity Test")
    print("=" * 50)
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Test all platforms
    platforms = [
        ("Reddit", test_reddit_access),
        ("GitHub", test_github_access),
        ("Hacker News", test_hackernews_access),
        ("Flippa", test_flippa_access),
        ("Empire Flippers", test_empire_flippers_access),
        ("Acquire.com", test_acquire_access),
        ("Twitter", test_twitter_access)
    ]
    
    for platform_name, test_func in platforms:
        try:
            result = await test_func()
            results[platform_name] = result
            
            # Add a small delay between tests
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"   💥 Test crashed: {e}")
            results[platform_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 CONNECTIVITY TEST RESULTS")
    print("=" * 50)
    
    working_count = 0
    total_count = len(results)
    
    for platform, result in results.items():
        if result is True:
            print(f"✅ {platform}: WORKING")
            working_count += 1
        elif result == 'fallback':
            print(f"⚠️ {platform}: FALLBACK (site may be blocked)")
            working_count += 0.5
        else:
            print(f"❌ {platform}: FAILED")
    
    success_rate = (working_count / total_count) * 100
    
    print(f"\n📈 Overall Success Rate: {working_count}/{total_count} ({success_rate:.1f}%)")
    
    if success_rate >= 60:
        print("🎉 GOOD: Most platforms accessible!")
    elif success_rate >= 40:
        print("⚠️ MODERATE: Some platforms working")
    else:
        print("🚨 POOR: Many platforms inaccessible")
    
    print(f"\n🔄 Test completed at: {datetime.now().strftime('%H:%M:%S')}")
    
    return results

if __name__ == "__main__":
    asyncio.run(main()) 