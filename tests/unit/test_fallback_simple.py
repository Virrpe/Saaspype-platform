#!/usr/bin/env python3
"""Simple test for Reddit fallback functionality"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

async def test_fallback():
    """Test the fallback Reddit API"""
    from src.api.services.discovery_service import DiscoveryService
    
    print("🧪 Testing Reddit Fallback API")
    print("=" * 40)
    
    ds = DiscoveryService()
    
    try:
        posts = await ds._fallback_fetch_posts('entrepreneur', 3)
        print(f"✅ Fallback Success: {len(posts)} posts fetched")
        
        for i, post in enumerate(posts[:2], 1):
            print(f"   {i}. {post['title'][:50]}...")
            print(f"      Score: {post['score']}, Comments: {post['num_comments']}")
        
        return len(posts) > 0
        
    except Exception as e:
        print(f"❌ Fallback Failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_fallback())
    print(f"\nResult: {'SUCCESS' if success else 'FAILED'}") 