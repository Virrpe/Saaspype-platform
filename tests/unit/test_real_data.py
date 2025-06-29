#!/usr/bin/env python3
"""
Test real data collection from implemented sources
"""

import asyncio
import sys
import os
sys.path.append('src/api')

from services.trend_detection_service import CrossPlatformTrendDetector
import json
from datetime import datetime

async def test_real_data_collection():
    """Test actual data collection from real sources"""
    
    detector = CrossPlatformTrendDetector()
    
    print("🔍 Testing REAL data collection...")
    print("=" * 50)
    
    # Test Reddit data collection
    print("\n📱 Testing Reddit data collection...")
    try:
        reddit_signals = await detector._collect_reddit_signals(hours_back=24)
        print(f"✅ Reddit: Collected {len(reddit_signals)} real signals")
        
        if reddit_signals:
            sample = reddit_signals[0]
            print(f"   Sample: {sample.content[:100]}...")
            print(f"   Source: {sample.metadata.get('subreddit')}")
            print(f"   Engagement: {sample.engagement_score}")
            print(f"   Keywords: {sample.keywords[:5]}")
    except Exception as e:
        print(f"❌ Reddit error: {e}")
    
    # Test GitHub data collection
    print("\n🐙 Testing GitHub data collection...")
    try:
        github_signals = await detector._collect_github_signals(hours_back=24)
        print(f"✅ GitHub: Collected {len(github_signals)} real signals")
        
        if github_signals:
            sample = github_signals[0]
            print(f"   Sample: {sample.content[:100]}...")
            print(f"   Stars: {sample.metadata.get('stars')}")
            print(f"   Language: {sample.metadata.get('language')}")
            print(f"   Keywords: {sample.keywords[:5]}")
    except Exception as e:
        print(f"❌ GitHub error: {e}")
    
    # Test Hacker News data collection
    print("\n🔥 Testing Hacker News data collection...")
    try:
        hn_signals = await detector._collect_hacker_news_signals(hours_back=24)
        print(f"✅ Hacker News: Collected {len(hn_signals)} real signals")
        
        if hn_signals:
            sample = hn_signals[0]
            print(f"   Sample: {sample.content[:100]}...")
            print(f"   Score: {sample.engagement_score}")
            print(f"   Keywords: {sample.keywords[:5]}")
    except Exception as e:
        print(f"❌ Hacker News error: {e}")
    
    # Test Dev.to data collection
    print("\n💻 Testing Dev.to data collection...")
    try:
        devto_signals = await detector._collect_devto_signals(hours_back=24)
        print(f"✅ Dev.to: Collected {len(devto_signals)} real signals")
        
        if devto_signals:
            sample = devto_signals[0]
            print(f"   Sample: {sample.content[:100]}...")
            print(f"   Author: {sample.metadata.get('author')}")
            print(f"   Reactions: {sample.metadata.get('reactions')}")
            print(f"   Keywords: {sample.keywords[:5]}")
    except Exception as e:
        print(f"❌ Dev.to error: {e}")
    
    # Test Stack Overflow data collection
    print("\n📚 Testing Stack Overflow data collection...")
    try:
        so_signals = await detector._collect_stackoverflow_signals(hours_back=24)
        print(f"✅ Stack Overflow: Collected {len(so_signals)} real signals")
        
        if so_signals:
            sample = so_signals[0]
            print(f"   Sample: {sample.content[:100]}...")
            print(f"   Score: {sample.metadata.get('score')}")
            print(f"   Tags: {sample.metadata.get('tags')[:3]}")
            print(f"   Keywords: {sample.keywords[:5]}")
    except Exception as e:
        print(f"❌ Stack Overflow error: {e}")
    
    # Test IndieHackers data collection
    print("\n🚀 Testing IndieHackers data collection...")
    try:
        ih_signals = await detector._collect_indiehackers_signals(hours_back=24)
        print(f"✅ IndieHackers: Collected {len(ih_signals)} real signals")
        
        if ih_signals:
            sample = ih_signals[0]
            print(f"   Sample: {sample.content[:100]}...")
            print(f"   Keywords: {sample.keywords[:5]}")
    except Exception as e:
        print(f"❌ IndieHackers error: {e}")
    
    # Test full trend detection
    print("\n🚀 Testing full trend detection pipeline...")
    try:
        opportunities = await detector.detect_cross_platform_trends(hours_back=6)
        print(f"✅ Generated {len(opportunities)} opportunities from real data")
        
        if opportunities:
            for i, opp in enumerate(opportunities[:3], 1):
                print(f"\n   #{i} {opp.title}")
                print(f"      Momentum: {opp.momentum_score:.1f}")
                print(f"      Sources: {', '.join(opp.sources)}")
                print(f"      Market: {opp.market_timing}")
                print(f"      Competition: {opp.competition_density}")
    except Exception as e:
        print(f"❌ Full pipeline error: {e}")
    
    # Close session
    await detector.close()
    
    print("\n" + "=" * 50)
    print("✅ Real data collection test complete!")

if __name__ == "__main__":
    asyncio.run(test_real_data_collection()) 