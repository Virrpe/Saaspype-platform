#!/usr/bin/env python3
"""
Real Reddit Discovery Pipeline - Pain Point Analysis
Uses the actual DiscoveryService with LLM analysis for finding SaaS opportunities
"""

import sys
import os
sys.path.append('src')

import asyncio
import json
from datetime import datetime

from api.domains.discovery.services.discovery_service import DiscoveryService

async def run_real_discovery():
    """Run the actual Reddit discovery pipeline with pain point analysis"""
    
    print("🚀 RUNNING ACTUAL REDDIT DISCOVERY PIPELINE")
    print("=" * 60)
    
    # Initialize the real discovery service
    service = DiscoveryService()
    
    print("📍 Target Subreddits:", service.target_subreddits)
    print("🎯 Starting real Reddit scraping with pain point analysis...")
    print("⚡ Using LLM analysis for business context extraction...")
    
    # Run discovery on entrepreneur subreddit
    discovery_request = {
        'subreddit': 'entrepreneur',
        'limit': 10
    }
    
    try:
        result = await service.discover_pain_points(
            subreddit=discovery_request['subreddit'],
            limit=discovery_request['limit']
        )
        
        print(f"\n✅ DISCOVERY COMPLETE")
        print(f"📊 Posts Analyzed: {result.get('posts_analyzed', 0)}")
        print(f"⚠️ Pain Points Found: {len(result.get('pain_points', []))}")
        print(f"💡 SaaS Concepts Generated: {len(result.get('concepts', []))}")
        print(f"🌟 Ranked Opportunities: {len(result.get('ranked_opportunities', []))}")
        
        # Show top SaaS concepts
        concepts = result.get('concepts', [])
        if concepts:
            print(f"\n🏆 TOP SAAS CONCEPTS:")
            for i, concept in enumerate(concepts[:3], 1):
                saas_concept = concept.get('saas_concept', {})
                source_opp = concept.get('source_opportunity', {})
                data = concept.get('data', {})
                
                print(f"\n#{i} {saas_concept.get('name', 'Untitled')}")
                print(f"   📝 {saas_concept.get('description', 'No description')}")
                print(f"   📊 Score: {source_opp.get('score', 0)}/10")
                print(f"   🎯 Industry: {data.get('industry', 'Unknown')}")
                print(f"   📍 Source: r/{data.get('subreddit', 'unknown')}")
                
                # Show key features
                features = saas_concept.get('key_features', [])
                if features:
                    print(f"   🔧 Key Features:")
                    for feature in features[:3]:
                        print(f"      • {feature}")
        
        # Show pain points
        pain_points = result.get('pain_points', [])
        if pain_points:
            print(f"\n⚠️ TOP PAIN POINTS DISCOVERED:")
            for i, pain_point in enumerate(pain_points[:5], 1):
                print(f"\n#{i} {pain_point.get('title', 'Untitled')}")
                print(f"   📊 Score: {pain_point.get('score', 0)}")
                print(f"   🏭 Industry: {pain_point.get('business_context', {}).get('industry', 'Unknown')}")
                print(f"   🔍 Pain Indicators: {len(pain_point.get('business_context', {}).get('pain_indicators', []))}")
        
        # Show ranked opportunities
        opportunities = result.get('ranked_opportunities', [])
        if opportunities:
            print(f"\n🌟 TOP RANKED OPPORTUNITIES:")
            for i, opp in enumerate(opportunities[:5], 1):
                print(f"\n#{i} {opp.get('title', 'Untitled')}")
                print(f"   📊 Score: {opp.get('score', 0)}/10")
                print(f"   🏭 Domain: {opp.get('domain', 'Unknown')}")
                print(f"   💰 Business Potential: {opp.get('business_potential', 'Unknown')}")
                print(f"   📍 Source: r/{opp.get('subreddit', 'unknown')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Discovery failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(run_real_discovery())
    
    if result:
        print(f"\n📊 DISCOVERY SUMMARY:")
        print(f"   📝 Posts: {result.get('posts_analyzed', 0)}")
        print(f"   ⚠️ Pain Points: {len(result.get('pain_points', []))}")
        print(f"   💡 Concepts: {len(result.get('concepts', []))}")
        print(f"   🌟 Opportunities: {len(result.get('ranked_opportunities', []))}")
        print(f"\n🎯 Real Reddit discovery pipeline completed successfully!")
    else:
        print(f"\n❌ Discovery pipeline failed!") 