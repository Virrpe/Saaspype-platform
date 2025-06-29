#!/usr/bin/env python3
"""
Test Real Reddit API Connection
Run this after setting up your .env file with actual Reddit credentials
"""

import os
import sys
import asyncio
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.api.domains.discovery.services.reddit_api_client import RedditAPIClient

async def test_reddit_connection():
    """Test real Reddit API connection and data quality"""
    
    print("🔍 TESTING REAL REDDIT API CONNECTION")
    print("=" * 50)
    
    # Initialize client
    client = RedditAPIClient()
    
    # Check credentials
    print(f"📋 Client ID: {'✅ SET' if client.client_id != 'your_client_id' else '❌ PLACEHOLDER'}")
    print(f"📋 Client Secret: {'✅ SET' if client.client_secret != 'your_client_secret' else '❌ PLACEHOLDER'}")
    print(f"📋 User Agent: {client.user_agent}")
    
    if client.client_id == 'your_client_id' or client.client_secret == 'your_client_secret':
        print("\n❌ REDDIT CREDENTIALS NOT SET")
        print("Please update your .env file with actual Reddit API credentials")
        print("Get them from: https://www.reddit.com/prefs/apps")
        return False
    
    # Test authentication
    print(f"\n🔐 Testing Reddit API Authentication...")
    auth_success = await client.authenticate()
    
    if not auth_success:
        print("❌ Authentication failed")
        return False
    
    print("✅ Authentication successful!")
    
    # Test data fetching
    print(f"\n📡 Testing Real Data Fetching...")
    
    test_subreddits = ['startups', 'entrepreneur', 'SaaS']
    
    for subreddit in test_subreddits:
        print(f"\n📊 Testing r/{subreddit}...")
        
        try:
            posts = await client.get_subreddit_posts(
                subreddit=subreddit,
                sort='new',
                limit=5,
                time_filter='day'
            )
            
            if posts:
                print(f"✅ Retrieved {len(posts)} real posts")
                
                # Analyze first post for quality
                first_post = posts[0]
                print(f"   📝 Sample: '{first_post.get('title', '')[:60]}...'")
                print(f"   👤 Author: {first_post.get('author', 'N/A')}")
                print(f"   📈 Score: {first_post.get('score', 0)}")
                print(f"   💬 Comments: {first_post.get('num_comments', 0)}")
                
                # Check for business relevance
                title = first_post.get('title', '').lower()
                body = first_post.get('selftext', '').lower()
                content = f"{title} {body}"
                
                business_keywords = ['startup', 'business', 'saas', 'revenue', 'customer', 'problem', 'solution']
                relevance_score = sum(1 for keyword in business_keywords if keyword in content)
                
                print(f"   🎯 Business Relevance: {relevance_score}/7 keywords found")
                
            else:
                print(f"❌ No posts retrieved from r/{subreddit}")
                
        except Exception as e:
            print(f"❌ Error fetching from r/{subreddit}: {e}")
    
    # Test rate limiting
    print(f"\n⏱️  Rate Limit Status:")
    rate_status = client.get_rate_limit_status()
    print(f"   Requests made: {rate_status['requests_made']}")
    print(f"   Requests remaining: {rate_status['requests_remaining']}")
    
    print(f"\n✅ REAL REDDIT API CONNECTION TEST COMPLETE")
    return True

async def test_quality_enhancement_with_real_data():
    """Test quality enhancement with real Reddit data"""
    
    print(f"\n🎯 TESTING QUALITY ENHANCEMENT WITH REAL DATA")
    print("=" * 50)
    
    # Get real data
    client = RedditAPIClient()
    await client.authenticate()
    
    real_posts = await client.get_subreddit_posts('startups', limit=10)
    
    if not real_posts:
        print("❌ No real data available for quality testing")
        return
    
    # Convert to signal format
    from tools.analyzers.signal_quality_enhancer import AdvancedSignalQualityEnhancer
    
    class RealSignal:
        def __init__(self, post):
            self.content = f"{post.get('title', '')} {post.get('selftext', '')}"
            self.source = 'reddit'
            self.engagement_score = post.get('score', 0)
            self.timestamp = datetime.now().isoformat()
            self.url = f"https://reddit.com{post.get('permalink', '')}"
            self.metadata = {
                'subreddit': post.get('subreddit'),
                'author': post.get('author'),
                'num_comments': post.get('num_comments', 0),
                'upvote_ratio': post.get('upvote_ratio', 0.5)
            }
    
    real_signals = [RealSignal(post) for post in real_posts]
    
    # Test quality enhancement
    enhancer = AdvancedSignalQualityEnhancer()
    
    # Use realistic thresholds (not demo-friendly ones)
    enhancer.enhanced_thresholds = {
        'minimum_overall_quality': 0.65,
        'minimum_business_relevance': 0.6,
        'minimum_pain_point_clarity': 0.5,
        'minimum_solution_feasibility': 0.4,
        'minimum_market_timing': 0.4
    }
    
    print(f"📊 Processing {len(real_signals)} real signals...")
    enhanced_signals = await enhancer.enhance_signals(real_signals)
    
    retention_rate = len(enhanced_signals) / len(real_signals) * 100
    
    print(f"✅ Quality Enhancement Results:")
    print(f"   Input signals: {len(real_signals)}")
    print(f"   High-quality signals: {len(enhanced_signals)}")
    print(f"   Retention rate: {retention_rate:.1f}% (REALISTIC)")
    
    if enhanced_signals:
        print(f"\n🏆 Top Quality Signal:")
        top_signal = enhanced_signals[0]
        print(f"   Content: '{top_signal.original_signal.content[:100]}...'")
        print(f"   Quality Score: {top_signal.quality_score:.2f}")
        print(f"   Business Potential: {top_signal.business_potential:.2f}")
        print(f"   Pain Points: {', '.join(top_signal.pain_point_indicators[:3])}")

if __name__ == "__main__":
    asyncio.run(test_reddit_connection())
    asyncio.run(test_quality_enhancement_with_real_data()) 