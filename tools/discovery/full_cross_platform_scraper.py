#!/usr/bin/env python3
"""
Full Cross-Platform Market Intelligence Scraper
Uses the complete CrossPlatformTrendDetector to scrape 8 sources simultaneously
"""

import sys
import os
sys.path.append('src')

import asyncio
import json
from datetime import datetime
from collections import defaultdict

from api.domains.streaming.services.trend_detection_service import CrossPlatformTrendDetector

async def run_full_cross_platform_scraper():
    """Run the complete cross-platform scraper across all 8 sources"""
    
    print("🚀 FULL CROSS-PLATFORM MARKET INTELLIGENCE SCRAPER")
    print("=" * 70)
    
    # Initialize the complete trend detector
    detector = CrossPlatformTrendDetector()
    
    # Show all active sources
    active_sources = [source for source, config in detector.data_sources.items() if config['enabled']]
    print(f"🎯 Active Sources ({len(active_sources)}):")
    for source in active_sources:
        config = detector.data_sources[source]
        weight = config.get('weight', config.get('base_weight', 0))
        credibility = config.get('credibility_multiplier', 1.0)
        print(f"   ✅ {source.upper()}: Weight {weight:.3f} (Credibility: {credibility:.2f}x)")
    
    print(f"\n📊 Expected Data Collection:")
    print(f"   🔴 Reddit: 8 subreddits × 15 posts = 120 posts")
    print(f"   🐦 Twitter: Real-time business trends")
    print(f"   🐙 GitHub: Trending repositories")
    print(f"   🚀 Product Hunt: Daily launches")
    print(f"   📰 Hacker News: Top stories")
    print(f"   👨‍💻 Dev.to: Trending posts")
    print(f"   📚 Stack Overflow: Trending questions")
    print(f"   🏗️ Indie Hackers: Community posts")
    
    print(f"\n🔄 Starting comprehensive data collection...")
    print("=" * 70)
    
    try:
        # Run the full cross-platform trend detection
        start_time = datetime.now()
        opportunities = await detector.detect_cross_platform_trends(hours_back=24)
        end_time = datetime.now()
        
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n🎉 CROSS-PLATFORM SCRAPING COMPLETE!")
        print(f"⏱️ Duration: {duration:.1f} seconds")
        print(f"🔍 Opportunities Found: {len(opportunities)}")
        
        if not opportunities:
            print("⚠️ No opportunities found - checking for issues...")
            return
        
        # Analyze results by source
        source_analysis = defaultdict(int)
        keyword_analysis = defaultdict(int)
        timing_analysis = defaultdict(int)
        competition_analysis = defaultdict(int)
        
        for opp in opportunities:
            # Count sources
            for source in opp.sources:
                source_analysis[source] += 1
            
            # Count keywords
            for keyword in opp.keywords[:5]:  # Top 5 keywords
                keyword_analysis[keyword] += 1
            
            # Count timing
            timing_analysis[opp.market_timing] += 1
            
            # Count competition
            competition_analysis[opp.competition_density] += 1
        
        # Display comprehensive analysis
        print(f"\n📊 SOURCE CONTRIBUTION ANALYSIS:")
        sorted_sources = sorted(source_analysis.items(), key=lambda x: x[1], reverse=True)
        for source, count in sorted_sources:
            print(f"   🎯 {source.upper()}: {count} opportunities")
        
        print(f"\n🔥 TOP TRENDING KEYWORDS:")
        sorted_keywords = sorted(keyword_analysis.items(), key=lambda x: x[1], reverse=True)
        for keyword, count in sorted_keywords[:10]:
            print(f"   🔑 {keyword}: {count} mentions")
        
        print(f"\n⏰ MARKET TIMING DISTRIBUTION:")
        for timing, count in sorted(timing_analysis.items(), key=lambda x: x[1], reverse=True):
            print(f"   📈 {timing.upper()}: {count} opportunities")
        
        print(f"\n🏆 COMPETITION DENSITY:")
        for competition, count in sorted(competition_analysis.items(), key=lambda x: x[1], reverse=True):
            print(f"   🥊 {competition.upper()}: {count} opportunities")
        
        # Show top opportunities with full details
        print(f"\n🌟 TOP 10 CROSS-PLATFORM OPPORTUNITIES:")
        print("=" * 70)
        
        sorted_opportunities = sorted(opportunities, key=lambda x: x.momentum_score, reverse=True)
        
        for i, opp in enumerate(sorted_opportunities[:10], 1):
            print(f"\n#{i} 🚀 {opp.title}")
            print(f"   📝 {opp.description}")
            print(f"   📊 Momentum: {opp.momentum_score:.1f}/10")
            print(f"   🎯 Confidence: {opp.confidence_level:.2f}")
            print(f"   ⏰ Timing: {opp.market_timing.upper()}")
            print(f"   🥊 Competition: {opp.competition_density.upper()}")
            print(f"   💰 Revenue: {opp.revenue_potential}")
            print(f"   📈 Market: {opp.estimated_market_size}")
            print(f"   🔧 Complexity: {opp.technical_complexity}")
            print(f"   📍 Sources: {', '.join(opp.sources)}")
            print(f"   🔑 Keywords: {', '.join(opp.keywords[:5])}")
            if hasattr(opp, 'average_credibility'):
                print(f"   ⭐ Credibility: {opp.average_credibility:.2f}")
        
        # Market intelligence summary
        print(f"\n🧠 MARKET INTELLIGENCE SUMMARY:")
        print("=" * 70)
        
        high_momentum = [opp for opp in opportunities if opp.momentum_score >= 8.0]
        emerging_markets = [opp for opp in opportunities if opp.market_timing == 'emerging']
        low_competition = [opp for opp in opportunities if opp.competition_density == 'low']
        high_revenue = [opp for opp in opportunities if 'high' in opp.revenue_potential.lower() or '1m+' in opp.revenue_potential.lower()]
        
        print(f"   🔥 High Momentum (≥8.0): {len(high_momentum)} opportunities")
        print(f"   🌱 Emerging Markets: {len(emerging_markets)} opportunities")
        print(f"   🎯 Low Competition: {len(low_competition)} opportunities")
        print(f"   💰 High Revenue Potential: {len(high_revenue)} opportunities")
        
        # Save comprehensive results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"cross_platform_intelligence_{timestamp}.json"
        
        # Prepare data for JSON serialization
        opportunities_data = []
        for opp in opportunities:
            opp_data = {
                'title': opp.title,
                'description': opp.description,
                'momentum_score': opp.momentum_score,
                'confidence_level': opp.confidence_level,
                'market_timing': opp.market_timing,
                'competition_density': opp.competition_density,
                'sources': opp.sources,
                'keywords': opp.keywords,
                'estimated_market_size': opp.estimated_market_size,
                'technical_complexity': opp.technical_complexity,
                'revenue_potential': opp.revenue_potential,
                'discovered_at': opp.discovered_at.isoformat() if hasattr(opp.discovered_at, 'isoformat') else str(opp.discovered_at),
                'average_credibility': getattr(opp, 'average_credibility', 0.0)
            }
            opportunities_data.append(opp_data)
        
        comprehensive_results = {
            'timestamp': timestamp,
            'scraping_duration_seconds': duration,
            'total_opportunities': len(opportunities),
            'active_sources': active_sources,
            'source_analysis': dict(source_analysis),
            'keyword_analysis': dict(keyword_analysis),
            'timing_analysis': dict(timing_analysis),
            'competition_analysis': dict(competition_analysis),
            'market_intelligence': {
                'high_momentum_count': len(high_momentum),
                'emerging_markets_count': len(emerging_markets),
                'low_competition_count': len(low_competition),
                'high_revenue_count': len(high_revenue)
            },
            'opportunities': opportunities_data
        }
        
        with open(results_file, 'w') as f:
            json.dump(comprehensive_results, f, indent=2, default=str)
        
        print(f"\n💾 COMPREHENSIVE RESULTS SAVED TO: {results_file}")
        print(f"🎯 Cross-platform market intelligence complete!")
        
        return comprehensive_results
        
    except Exception as e:
        print(f"❌ Cross-platform scraping failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    
    finally:
        # Clean up
        if hasattr(detector, 'close'):
            await detector.close()

if __name__ == "__main__":
    results = asyncio.run(run_full_cross_platform_scraper())
    
    if results:
        print(f"\n🚀 CROSS-PLATFORM SCRAPING MISSION ACCOMPLISHED!")
        print(f"   ⏱️ Duration: {results['scraping_duration_seconds']:.1f}s")
        print(f"   🔍 Opportunities: {results['total_opportunities']}")
        print(f"   📊 Sources: {len(results['active_sources'])}")
        print(f"   🔥 High Momentum: {results['market_intelligence']['high_momentum_count']}")
        print(f"   🌱 Emerging Markets: {results['market_intelligence']['emerging_markets_count']}")
        print(f"   🎯 Low Competition: {results['market_intelligence']['low_competition_count']}")
    else:
        print(f"\n❌ Cross-platform scraping mission failed!") 