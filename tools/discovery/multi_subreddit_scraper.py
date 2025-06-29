#!/usr/bin/env python3
"""
Multi-Subreddit Pain Point Scraper
Scrapes 10 subreddits for real business pain points and SaaS opportunities
"""

import sys
import os
sys.path.append('src')

import asyncio
import json
from datetime import datetime
from collections import defaultdict

from api.domains.discovery.services.discovery_service import DiscoveryService

async def scrape_multiple_subreddits():
    """Scrape 10 subreddits for comprehensive pain point analysis"""
    
    print("🚀 MULTI-SUBREDDIT PAIN POINT SCRAPER")
    print("=" * 60)
    
    # Target subreddits for comprehensive analysis
    target_subreddits = [
        'entrepreneur',      # Main entrepreneurship discussions
        'startups',         # Startup-specific problems
        'SaaS',            # SaaS business challenges
        'smallbusiness',   # Small business pain points
        'freelance',       # Freelancer problems
        'indiehackers',    # Indie hacker challenges
        'business',        # General business issues
        'marketing',       # Marketing pain points
        'webdev',          # Developer problems
        'productivity'     # Productivity challenges
    ]
    
    # Initialize discovery service
    service = DiscoveryService()
    
    # Storage for all results
    all_pain_points = []
    all_opportunities = []
    all_concepts = []
    subreddit_stats = {}
    
    print(f"🎯 Target Subreddits: {len(target_subreddits)}")
    print(f"📊 Posts per subreddit: 8")
    print(f"🔍 Total posts to analyze: {len(target_subreddits) * 8}")
    print("\n" + "="*60)
    
    # Scrape each subreddit
    for i, subreddit in enumerate(target_subreddits, 1):
        print(f"\n🔍 [{i}/{len(target_subreddits)}] SCRAPING r/{subreddit}")
        print("-" * 40)
        
        try:
            # Run discovery on this subreddit
            result = await service.discover_pain_points(
                subreddit=subreddit,
                limit=8  # 8 posts per subreddit = 80 total posts
            )
            
            # Extract results
            posts_analyzed = result.get('posts_analyzed', 0)
            pain_points = result.get('pain_points', [])
            opportunities = result.get('ranked_opportunities', [])
            concepts = result.get('concepts', [])
            
            # Store stats
            subreddit_stats[subreddit] = {
                'posts_analyzed': posts_analyzed,
                'pain_points_found': len(pain_points),
                'opportunities_generated': len(opportunities),
                'concepts_generated': len(concepts)
            }
            
            # Add subreddit tag to all items
            for pain_point in pain_points:
                pain_point['source_subreddit'] = subreddit
                all_pain_points.append(pain_point)
            
            for opportunity in opportunities:
                opportunity['source_subreddit'] = subreddit
                all_opportunities.append(opportunity)
            
            for concept in concepts:
                concept['source_subreddit'] = subreddit
                all_concepts.append(concept)
            
            # Show immediate results
            print(f"   📊 Posts: {posts_analyzed}")
            print(f"   ⚠️ Pain Points: {len(pain_points)}")
            print(f"   🌟 Opportunities: {len(opportunities)}")
            print(f"   💡 Concepts: {len(concepts)}")
            
            # Show top pain point from this subreddit
            if pain_points:
                top_pain = pain_points[0]
                print(f"   🏆 Top Pain: {top_pain.get('title', 'Unknown')[:60]}...")
            
            # Small delay to be respectful to Reddit
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"   ❌ Error scraping r/{subreddit}: {str(e)}")
            subreddit_stats[subreddit] = {
                'posts_analyzed': 0,
                'pain_points_found': 0,
                'opportunities_generated': 0,
                'concepts_generated': 0,
                'error': str(e)
            }
    
    # Comprehensive analysis
    print(f"\n🎉 MULTI-SUBREDDIT SCRAPING COMPLETE!")
    print("=" * 60)
    
    # Overall stats
    total_posts = sum(stats['posts_analyzed'] for stats in subreddit_stats.values())
    total_pain_points = len(all_pain_points)
    total_opportunities = len(all_opportunities)
    total_concepts = len(all_concepts)
    
    print(f"📊 OVERALL STATISTICS:")
    print(f"   📝 Total Posts Analyzed: {total_posts}")
    print(f"   ⚠️ Total Pain Points Found: {total_pain_points}")
    print(f"   🌟 Total Opportunities Generated: {total_opportunities}")
    print(f"   💡 Total SaaS Concepts: {total_concepts}")
    print(f"   📈 Pain Point Discovery Rate: {(total_pain_points/total_posts*100):.1f}%")
    
    # Subreddit performance ranking
    print(f"\n🏆 SUBREDDIT PERFORMANCE RANKING:")
    sorted_subreddits = sorted(
        subreddit_stats.items(), 
        key=lambda x: x[1]['pain_points_found'], 
        reverse=True
    )
    
    for i, (subreddit, stats) in enumerate(sorted_subreddits[:10], 1):
        if 'error' not in stats:
            print(f"   #{i} r/{subreddit}: {stats['pain_points_found']} pain points from {stats['posts_analyzed']} posts")
        else:
            print(f"   #{i} r/{subreddit}: ERROR - {stats['error']}")
    
    # Top pain points across all subreddits
    print(f"\n⚠️ TOP 10 PAIN POINTS ACROSS ALL SUBREDDITS:")
    sorted_pain_points = sorted(all_pain_points, key=lambda x: x.get('score', 0), reverse=True)
    
    for i, pain_point in enumerate(sorted_pain_points[:10], 1):
        title = pain_point.get('title', 'Unknown')
        score = pain_point.get('score', 0)
        subreddit = pain_point.get('source_subreddit', 'unknown')
        industry = pain_point.get('business_context', {}).get('industry', 'Unknown')
        
        print(f"\n   #{i} 📈 {title[:70]}...")
        print(f"       📊 Score: {score}/10 | 🏭 Industry: {industry} | 📍 r/{subreddit}")
    
    # Top opportunities
    print(f"\n🌟 TOP 10 SAAS OPPORTUNITIES:")
    sorted_opportunities = sorted(all_opportunities, key=lambda x: x.get('score', 0), reverse=True)
    
    for i, opp in enumerate(sorted_opportunities[:10], 1):
        title = opp.get('title', 'Unknown')
        score = opp.get('score', 0)
        domain = opp.get('domain', 'Unknown')
        subreddit = opp.get('source_subreddit', 'unknown')
        potential = opp.get('business_potential', 'Unknown')
        
        print(f"\n   #{i} 💡 {title[:70]}...")
        print(f"       📊 Score: {score}/10 | 🏭 Domain: {domain} | 💰 Potential: {potential} | 📍 r/{subreddit}")
    
    # Industry analysis
    print(f"\n🏭 INDUSTRY BREAKDOWN:")
    industry_counts = defaultdict(int)
    for pain_point in all_pain_points:
        industry = pain_point.get('business_context', {}).get('industry', 'Unknown')
        industry_counts[industry] += 1
    
    sorted_industries = sorted(industry_counts.items(), key=lambda x: x[1], reverse=True)
    for industry, count in sorted_industries[:8]:
        print(f"   🎯 {industry.title()}: {count} pain points")
    
    # Save comprehensive results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"multi_subreddit_results_{timestamp}.json"
    
    comprehensive_results = {
        'timestamp': timestamp,
        'subreddits_analyzed': target_subreddits,
        'overall_stats': {
            'total_posts': total_posts,
            'total_pain_points': total_pain_points,
            'total_opportunities': total_opportunities,
            'total_concepts': total_concepts,
            'discovery_rate': total_pain_points/total_posts if total_posts > 0 else 0
        },
        'subreddit_stats': subreddit_stats,
        'all_pain_points': all_pain_points,
        'all_opportunities': all_opportunities,
        'all_concepts': all_concepts,
        'industry_breakdown': dict(industry_counts)
    }
    
    with open(results_file, 'w') as f:
        json.dump(comprehensive_results, f, indent=2, default=str)
    
    print(f"\n💾 RESULTS SAVED TO: {results_file}")
    print(f"🎯 Multi-subreddit pain point discovery complete!")
    
    return comprehensive_results

if __name__ == "__main__":
    results = asyncio.run(scrape_multiple_subreddits())
    
    print(f"\n🚀 SCRAPING MISSION ACCOMPLISHED!")
    print(f"   📊 {results['overall_stats']['total_posts']} posts analyzed")
    print(f"   ⚠️ {results['overall_stats']['total_pain_points']} pain points discovered")
    print(f"   🌟 {results['overall_stats']['total_opportunities']} opportunities generated")
    print(f"   📈 {results['overall_stats']['discovery_rate']:.1%} success rate") 