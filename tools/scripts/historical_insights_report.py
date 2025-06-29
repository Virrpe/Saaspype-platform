#!/usr/bin/env python3
"""
Historical Insights Report for Luciq
Analyzes deep historical pain point data to identify persistent problems and seasonal patterns
"""

import json
from datetime import datetime

def load_historical_data():
    """Load historical pain point trends data"""
    try:
        with open("luciq/memory/historical-pain-trends.json", 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading historical data: {e}")
        return {}

def analyze_persistence_patterns(data):
    """Analyze persistence patterns and long-standing problems"""
    persistent_problems = []
    
    for keyword, trend_data in data.items():
        persistence_score = trend_data.get('persistence_score', 0)
        max_age_days = trend_data.get('max_age_days', 0)
        long_term_trend = trend_data.get('long_term_trend', 'stable')
        total_occurrences = trend_data.get('total_occurrences', 0)
        
        if persistence_score >= 3:  # 6+ months old
            persistent_problems.append({
                'keyword': keyword,
                'persistence_score': persistence_score,
                'max_age_days': max_age_days,
                'long_term_trend': long_term_trend,
                'total_occurrences': total_occurrences,
                'subreddits': list(trend_data.get('subreddit_distribution', {}).keys()),
                'business_potential': trend_data.get('business_potential_distribution', {}),
                'historical_depth': trend_data.get('historical_depth', {})
            })
    
    # Sort by persistence score and age
    persistent_problems.sort(key=lambda x: (x['persistence_score'], x['max_age_days']), reverse=True)
    return persistent_problems

def analyze_seasonal_patterns(data):
    """Analyze seasonal patterns in pain points"""
    seasonal_insights = []
    
    for keyword, trend_data in data.items():
        seasonal_patterns = trend_data.get('seasonal_patterns', {})
        seasonal_relevance = trend_data.get('seasonal_relevance', 'none')
        
        if seasonal_relevance != 'none' or max(seasonal_patterns.values()) > 1:
            dominant_season = max(seasonal_patterns.items(), key=lambda x: x[1])
            
            seasonal_insights.append({
                'keyword': keyword,
                'seasonal_relevance': seasonal_relevance,
                'dominant_season': dominant_season[0],
                'season_count': dominant_season[1],
                'seasonal_distribution': seasonal_patterns,
                'total_occurrences': trend_data.get('total_occurrences', 0)
            })
    
    seasonal_insights.sort(key=lambda x: x['season_count'], reverse=True)
    return seasonal_insights

def analyze_cross_community_patterns(data):
    """Analyze pain points that appear across multiple communities"""
    cross_community = []
    
    for keyword, trend_data in data.items():
        subreddit_dist = trend_data.get('subreddit_distribution', {})
        
        if len(subreddit_dist) >= 3:  # Appears in 3+ subreddits
            cross_community.append({
                'keyword': keyword,
                'community_count': len(subreddit_dist),
                'subreddits': list(subreddit_dist.keys()),
                'distribution': subreddit_dist,
                'total_occurrences': trend_data.get('total_occurrences', 0),
                'business_potential': trend_data.get('business_potential_distribution', {})
            })
    
    cross_community.sort(key=lambda x: x['community_count'], reverse=True)
    return cross_community

def generate_report():
    """Generate comprehensive historical insights report"""
    print("🕰️ LUCIQ DEEP HISTORICAL INSIGHTS REPORT")
    print("=" * 80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    data = load_historical_data()
    if not data:
        print("No historical data available.")
        return
    
    print(f"📊 OVERVIEW: {len(data)} pain point categories analyzed")
    print()
    
    # 1. Persistent Problems Analysis
    print("🔍 PERSISTENT PROBLEMS (6+ months old)")
    print("-" * 50)
    persistent = analyze_persistence_patterns(data)
    
    if persistent:
        for i, problem in enumerate(persistent[:10], 1):
            age_years = problem['max_age_days'] / 365
            print(f"{i}. '{problem['keyword']}' - {problem['long_term_trend'].upper()}")
            print(f"   Age: {problem['max_age_days']:.0f} days ({age_years:.1f} years)")
            print(f"   Persistence Score: {problem['persistence_score']}/5")
            print(f"   Total Occurrences: {problem['total_occurrences']}")
            print(f"   Communities: {', '.join(problem['subreddits'])}")
            
            # Business potential analysis
            bp = problem['business_potential']
            high_potential = bp.get('high', 0)
            total_potential = sum(bp.values())
            if total_potential > 0:
                high_percentage = (high_potential / total_potential) * 100
                print(f"   High Business Potential: {high_percentage:.0f}% ({high_potential}/{total_potential})")
            print()
    else:
        print("No persistent problems found (all pain points are recent)")
    
    print()
    
    # 2. Seasonal Patterns Analysis
    print("🌍 SEASONAL PATTERNS")
    print("-" * 30)
    seasonal = analyze_seasonal_patterns(data)
    
    if seasonal:
        for pattern in seasonal[:5]:
            print(f"'{pattern['keyword']}' - {pattern['seasonal_relevance'].upper()} seasonal relevance")
            print(f"   Dominant Season: {pattern['dominant_season']} ({pattern['season_count']} occurrences)")
            print(f"   Distribution: {pattern['seasonal_distribution']}")
            print()
    else:
        print("No clear seasonal patterns detected yet")
    
    print()
    
    # 3. Cross-Community Analysis
    print("🌐 CROSS-COMMUNITY PAIN POINTS")
    print("-" * 40)
    cross_community = analyze_cross_community_patterns(data)
    
    if cross_community:
        for pattern in cross_community[:5]:
            print(f"'{pattern['keyword']}' - Appears in {pattern['community_count']} communities")
            print(f"   Communities: {', '.join(pattern['subreddits'])}")
            print(f"   Distribution: {pattern['distribution']}")
            
            # Business potential
            bp = pattern['business_potential']
            high_potential = bp.get('high', 0)
            total_potential = sum(bp.values())
            if total_potential > 0:
                high_percentage = (high_potential / total_potential) * 100
                print(f"   High Business Potential: {high_percentage:.0f}%")
            print()
    else:
        print("No cross-community patterns found yet")
    
    print()
    
    # 4. Key Insights Summary
    print("💡 KEY INSIGHTS")
    print("-" * 20)
    
    if persistent:
        oldest_problem = max(persistent, key=lambda x: x['max_age_days'])
        print(f"• Oldest persistent problem: '{oldest_problem['keyword']}' ({oldest_problem['max_age_days']:.0f} days old)")
        
        most_frequent = max(persistent, key=lambda x: x['total_occurrences'])
        print(f"• Most frequent persistent issue: '{most_frequent['keyword']}' ({most_frequent['total_occurrences']} occurrences)")
    
    if cross_community:
        most_widespread = max(cross_community, key=lambda x: x['community_count'])
        print(f"• Most widespread issue: '{most_widespread['keyword']}' (across {most_widespread['community_count']} communities)")
    
    # Calculate total historical depth
    total_deep_historical = sum(
        trend_data.get('historical_depth', {}).get('deep_historical', 0) 
        for trend_data in data.values()
    )
    total_yearly = sum(
        trend_data.get('historical_depth', {}).get('yearly', 0) 
        for trend_data in data.values()
    )
    
    print(f"• Deep historical posts analyzed: {total_deep_historical} (2+ years old)")
    print(f"• Yearly historical posts analyzed: {total_yearly} (1+ year old)")
    
    print()
    print("🎯 OPPORTUNITY RECOMMENDATIONS")
    print("-" * 35)
    
    if persistent:
        high_value_persistent = [p for p in persistent if p['business_potential'].get('high', 0) > 0]
        if high_value_persistent:
            top_opportunity = high_value_persistent[0]
            print(f"• TOP OPPORTUNITY: '{top_opportunity['keyword']}' - Long-standing problem with high business potential")
            print(f"  - Persistent for {top_opportunity['max_age_days']:.0f} days across {len(top_opportunity['subreddits'])} communities")
            print(f"  - High business potential in {top_opportunity['business_potential'].get('high', 0)} cases")

if __name__ == "__main__":
    generate_report() 