#!/usr/bin/env python3
"""
Cross-Platform Intelligence Analyzer
Deep analysis of market opportunities from 8-source scraping system
"""

import json
import glob
from datetime import datetime
from collections import defaultdict, Counter
import statistics

def analyze_cross_platform_intelligence():
    """Comprehensive analysis of cross-platform market intelligence"""
    
    print("🧠 CROSS-PLATFORM INTELLIGENCE ANALYZER")
    print("=" * 60)
    
    # Find latest intelligence file
    files = glob.glob('cross_platform_intelligence_*.json')
    if not files:
        print("❌ No intelligence files found!")
        return
    
    latest_file = max(files)
    print(f"📊 Analyzing: {latest_file}")
    
    with open(latest_file, 'r') as f:
        data = json.load(f)
    
    # Basic metrics
    print(f"\n📈 PERFORMANCE METRICS:")
    print(f"   ⏱️ Scraping Duration: {data['scraping_duration_seconds']:.1f} seconds")
    print(f"   🔍 Total Opportunities: {data['total_opportunities']}")
    print(f"   📊 Active Sources: {len(data['active_sources'])}")
    print(f"   🎯 Signals per Second: {108/data['scraping_duration_seconds']:.1f}")
    
    # Source performance analysis
    print(f"\n🎯 SOURCE PERFORMANCE RANKING:")
    source_analysis = data['source_analysis']
    total_contributions = sum(source_analysis.values())
    
    for i, (source, count) in enumerate(sorted(source_analysis.items(), key=lambda x: x[1], reverse=True), 1):
        percentage = (count / total_contributions) * 100
        print(f"   #{i} {source.upper()}: {count} opportunities ({percentage:.1f}%)")
    
    # Opportunity quality analysis
    opportunities = data['opportunities']
    
    print(f"\n🏆 OPPORTUNITY QUALITY ANALYSIS:")
    
    # Momentum scores
    momentum_scores = [opp['momentum_score'] for opp in opportunities]
    avg_momentum = statistics.mean(momentum_scores)
    print(f"   📊 Average Momentum: {avg_momentum:.1f}/10")
    print(f"   🔥 High Momentum (≥8.0): {len([s for s in momentum_scores if s >= 8.0])}")
    
    # Confidence levels
    confidence_levels = [opp['confidence_level'] for opp in opportunities]
    avg_confidence = statistics.mean(confidence_levels)
    print(f"   🎯 Average Confidence: {avg_confidence:.2f}")
    print(f"   ✅ High Confidence (≥0.8): {len([c for c in confidence_levels if c >= 0.8])}")
    
    # Credibility analysis
    credibility_scores = [opp['average_credibility'] for opp in opportunities]
    avg_credibility = statistics.mean(credibility_scores)
    print(f"   ⭐ Average Credibility: {avg_credibility:.2f}")
    print(f"   🏅 High Credibility (≥1.2): {len([c for c in credibility_scores if c >= 1.2])}")
    
    # Market size distribution
    print(f"\n📈 MARKET SIZE DISTRIBUTION:")
    market_sizes = [opp['estimated_market_size'] for opp in opportunities]
    market_counter = Counter(market_sizes)
    for market_size, count in market_counter.most_common():
        print(f"   💰 {market_size}: {count} opportunities")
    
    # Technical complexity analysis
    print(f"\n🔧 TECHNICAL COMPLEXITY BREAKDOWN:")
    complexity_levels = [opp['technical_complexity'] for opp in opportunities]
    complexity_counter = Counter(complexity_levels)
    for complexity, count in complexity_counter.most_common():
        print(f"   ⚙️ {complexity}: {count} opportunities")
    
    # Cross-platform correlation analysis
    print(f"\n🌐 CROSS-PLATFORM CORRELATION ANALYSIS:")
    
    # Multi-source opportunities (higher confidence)
    multi_source_opps = [opp for opp in opportunities if len(opp['sources']) > 2]
    print(f"   🔗 Multi-Source Opportunities: {len(multi_source_opps)}")
    
    if multi_source_opps:
        print(f"   📊 Top Multi-Source Opportunities:")
        for opp in sorted(multi_source_opps, key=lambda x: len(x['sources']), reverse=True)[:3]:
            sources_count = len(opp['sources'])
            title = opp['title']
            print(f"      🎯 {title} ({sources_count} sources)")
    
    # Source combination patterns
    print(f"\n🔄 SOURCE COMBINATION PATTERNS:")
    source_combinations = defaultdict(int)
    for opp in opportunities:
        sources = tuple(sorted(opp['sources']))
        source_combinations[sources] += 1
    
    for sources, count in sorted(source_combinations.items(), key=lambda x: x[1], reverse=True)[:5]:
        sources_str = " + ".join(sources)
        print(f"   🤝 {sources_str}: {count} opportunities")
    
    # Keyword trend analysis
    print(f"\n🔑 KEYWORD TREND ANALYSIS:")
    keyword_analysis = data['keyword_analysis']
    
    # Business category mapping
    business_categories = {
        'ai': 'Artificial Intelligence',
        'api': 'Developer Tools',
        'app': 'Mobile/Web Apps',
        'productivity': 'Productivity Tools',
        'broken': 'Problem Solving',
        'need': 'Market Gaps'
    }
    
    for keyword, count in sorted(keyword_analysis.items(), key=lambda x: x[1], reverse=True):
        category = business_categories.get(keyword, 'Other')
        print(f"   🏷️ {keyword.upper()} ({category}): {count} mentions")
    
    # Investment attractiveness scoring
    print(f"\n💎 INVESTMENT ATTRACTIVENESS ANALYSIS:")
    
    for i, opp in enumerate(opportunities, 1):
        # Calculate investment score
        momentum = opp['momentum_score']
        confidence = opp['confidence_level']
        credibility = opp['average_credibility']
        sources_count = len(opp['sources'])
        
        # Market size scoring
        market_size = opp['estimated_market_size']
        if 'Large' in market_size:
            market_score = 3
        elif 'Medium' in market_size:
            market_score = 2
        else:
            market_score = 1
        
        # Technical complexity scoring (lower is better for quick wins)
        complexity = opp['technical_complexity']
        if complexity == 'Low':
            complexity_score = 3
        elif complexity == 'Medium':
            complexity_score = 2
        else:
            complexity_score = 1
        
        # Investment attractiveness formula
        investment_score = (
            (momentum / 10) * 0.3 +
            confidence * 0.25 +
            (credibility / 2) * 0.2 +
            (sources_count / 5) * 0.1 +
            (market_score / 3) * 0.1 +
            (complexity_score / 3) * 0.05
        ) * 10
        
        title = opp['title']
        print(f"   #{i} {title}")
        print(f"       💎 Investment Score: {investment_score:.1f}/10")
        print(f"       📊 Momentum: {momentum}/10 | 🎯 Confidence: {confidence:.2f}")
        print(f"       ⭐ Credibility: {credibility:.2f} | 🌐 Sources: {sources_count}")
        print(f"       📈 Market: {market_size} | 🔧 Complexity: {complexity}")
    
    # Strategic recommendations
    print(f"\n🎯 STRATEGIC RECOMMENDATIONS:")
    
    # Best opportunities for immediate action
    high_confidence_opps = [opp for opp in opportunities if opp['confidence_level'] >= 0.8]
    if high_confidence_opps:
        print(f"   🚀 IMMEDIATE ACTION OPPORTUNITIES:")
        for opp in high_confidence_opps[:3]:
            print(f"      ⚡ {opp['title']} (Confidence: {opp['confidence_level']:.2f})")
    
    # Multi-platform validated opportunities
    validated_opps = [opp for opp in opportunities if len(opp['sources']) >= 3]
    if validated_opps:
        print(f"   ✅ CROSS-PLATFORM VALIDATED:")
        for opp in validated_opps[:3]:
            sources_count = len(opp['sources'])
            print(f"      🌐 {opp['title']} ({sources_count} sources)")
    
    # Low complexity, high market opportunities
    quick_wins = [opp for opp in opportunities 
                  if opp['technical_complexity'] == 'Low' and 'Large' in opp['estimated_market_size']]
    if quick_wins:
        print(f"   🎯 QUICK WIN OPPORTUNITIES:")
        for opp in quick_wins:
            print(f"      ⚡ {opp['title']} (Low complexity, Large market)")
    
    # Market timing insights
    print(f"\n⏰ MARKET TIMING INSIGHTS:")
    timing_analysis = data['timing_analysis']
    for timing, count in timing_analysis.items():
        if timing == 'emerging':
            print(f"   🌱 {count} EMERGING markets - Perfect timing for entry!")
        elif timing == 'hot':
            print(f"   🔥 {count} HOT markets - High competition but proven demand")
        elif timing == 'early':
            print(f"   🌟 {count} EARLY markets - High risk, high reward potential")
    
    print(f"\n🎉 ANALYSIS COMPLETE!")
    print(f"📊 {len(opportunities)} opportunities analyzed across {len(data['active_sources'])} sources")
    print(f"⏱️ Total intelligence gathering: {data['scraping_duration_seconds']:.1f} seconds")

if __name__ == "__main__":
    analyze_cross_platform_intelligence() 