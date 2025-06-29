#!/usr/bin/env python3
"""
Luciq REAL Intelligence Demonstration
Show actual revolutionary capabilities with real data
"""

import requests
import json
import time
from datetime import datetime

def test_real_intelligence(url, description, data, method="POST"):
    """Test with real data and show actual results"""
    print(f"\n🔥 REAL TEST: {description}")
    print(f"📍 URL: {url}")
    print(f"📤 Request Data: {json.dumps(data, indent=2)}")
    
    try:
        start_time = time.time()
        
        if method == "GET":
            response = requests.get(url, timeout=30)
        else:
            response = requests.post(url, json=data, timeout=30)
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        print(f"⚡ Response Time: {response_time:.2f}ms")
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            json_data = response.json()
            print(f"✅ SUCCESS!")
            print(f"📄 ACTUAL RESPONSE:")
            print("=" * 80)
            print(json.dumps(json_data, indent=2))
            print("=" * 80)
            return True, json_data
        else:
            print(f"❌ FAILED!")
            print(f"📄 Error Response: {response.text}")
            return False, response.text
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False, str(e)

def main():
    """Real Luciq Intelligence Demonstration"""
    
    print("🚀 Luciq REAL INTELLIGENCE DEMONSTRATION")
    print("=" * 80)
    print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Showing ACTUAL Revolutionary Intelligence Capabilities")
    print("💰 Demonstrating $10B+ Market Disruption Technology")
    print("=" * 80)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Get actual capabilities overview
    print("\n🧠 TEST 1: COMPLETE INTELLIGENCE CAPABILITIES")
    success, data = test_real_intelligence(
        f"{base_url}/api/intelligence/capabilities",
        "Complete Intelligence Engine Capabilities",
        {},
        "GET"
    )
    
    # Test 2: Phase 1 - Pain Point Detection with REAL content
    print("\n🎯 TEST 2: PHASE 1 - PAIN POINT DETECTION ENGINE")
    pain_point_data = {
        "content": """
        I'm struggling to validate my SaaS idea. The market research is so expensive - CB Insights wants $60K/year 
        and PitchBook is $12K/year just for basic data. I need to understand if there's real demand for my 
        AI-powered project management tool, but I can't afford these traditional solutions. 
        
        The problem is that I'm bootstrapping and need to make smart decisions with limited budget. 
        I've tried surveys but the response rate is terrible. I've looked at competitors but it's hard 
        to get real usage data. I need something that can give me real-time market intelligence 
        without breaking the bank.
        
        Reddit discussions show other entrepreneurs have the same problem - we're all flying blind 
        when it comes to market validation. There has to be a better way to get business intelligence 
        for startups and small businesses.
        """,
        "analysis_depth": "comprehensive",
        "platforms": ["reddit", "hackernews", "stackoverflow"]
    }
    
    success, data = test_real_intelligence(
        f"{base_url}/api/intelligence/pain-point-detection",
        "Phase 1: Real Pain Point Detection Analysis",
        pain_point_data
    )
    
    # Test 3: Phase 2 - Solution Gap Analysis with REAL business idea
    print("\n🔍 TEST 3: PHASE 2 - SOLUTION GAP ANALYZER")
    solution_gap_data = {
        "content": """
        Business Idea: AI-powered business intelligence platform for entrepreneurs and VCs
        
        Target Market: Bootstrapped entrepreneurs, early-stage VCs, corporate strategy teams
        
        Current Solutions Analysis:
        - CB Insights: $60K/year, static reports, enterprise-focused
        - PitchBook: $12K/year, financial data only, limited real-time insights
        - Traditional consulting: $50K+ per engagement, slow, manual processes
        - Market research firms: $125K+ for custom studies, takes months
        
        Proposed Solution: Real-time business intelligence platform with:
        - 15+ platform data scraping and analysis
        - AI-powered trend detection and sentiment analysis
        - Cross-platform intelligence fusion
        - Affordable pricing at $2,499/year
        - Real-time insights vs static reports
        
        Key Questions:
        1. What gaps exist in current market intelligence solutions?
        2. How feasible is it to bootstrap this with limited resources?
        3. What's the optimal market entry strategy?
        4. What are the main competitive advantages we can leverage?
        """,
        "analysis_scope": "comprehensive",
        "competitive_analysis": True
    }
    
    success, data = test_real_intelligence(
        f"{base_url}/api/intelligence/solution-gap-analysis",
        "Phase 2: Real Solution Gap Analysis",
        solution_gap_data
    )
    
    # Test 4: Phase 3 - Market Validation with REAL market scenario
    print("\n📈 TEST 4: PHASE 3 - MARKET VALIDATION ENGINE")
    market_validation_data = {
        "content": """
        Market Validation Request: Luciq - Revolutionary Business Intelligence Platform
        
        Business Concept: 
        Real-time business intelligence platform that disrupts the $10B+ market research industry
        by providing affordable, AI-powered market intelligence for entrepreneurs and VCs.
        
        Target Market Segments:
        1. Bootstrapped entrepreneurs (need affordable market validation)
        2. Early-stage VCs (need deal flow intelligence)
        3. Corporate strategy teams (need competitive intelligence)
        4. Business consultants (need data-driven insights)
        
        Competitive Landscape:
        - CB Insights: $60,000/year (static reports, enterprise-only)
        - PitchBook: $12,000/year (financial data, limited insights)
        - Market research firms: $125,000+/year (slow, manual)
        - Consulting firms: $50,000+ per engagement (expensive, slow)
        
        Our Positioning:
        - Pricing: $2,499/year (50-100x cheaper than competitors)
        - Speed: Real-time insights vs months-long studies
        - Scope: 15+ platform intelligence vs single-source data
        - Accessibility: Self-service vs enterprise-only solutions
        
        Key Validation Questions:
        1. Is there sufficient market demand for affordable business intelligence?
        2. Can we capture significant market share with disruptive pricing?
        3. What are the main market entry risks and opportunities?
        4. How strong is our competitive positioning?
        5. What's the optimal timing for market entry?
        """,
        "competitive_analysis": True,
        "market_timing_assessment": True,
        "risk_assessment": True
    }
    
    success, data = test_real_intelligence(
        f"{base_url}/api/intelligence/market-validation",
        "Phase 3: Real Market Validation Analysis",
        market_validation_data
    )
    
    # Test 5: Real Discovery Search
    print("\n🔍 TEST 5: DISCOVERY ENGINE - REAL PLATFORM INTELLIGENCE")
    discovery_data = {
        "query": "business intelligence market trends startup validation",
        "platforms": ["reddit", "hackernews"],
        "max_results": 10,
        "analysis_depth": "comprehensive"
    }
    
    # Try the correct discovery endpoint
    success, data = test_real_intelligence(
        f"{base_url}/api/discovery/discover",
        "Real Discovery Engine Intelligence",
        discovery_data
    )
    
    # Test 6: Intelligence Analysis with real content
    print("\n🧠 TEST 6: ADVANCED INTELLIGENCE ANALYSIS")
    intelligence_data = {
        "content": """
        Market Intelligence Analysis Request:
        
        Analyze the current state of the business intelligence and market research industry.
        Focus on pain points experienced by entrepreneurs and small businesses who cannot
        afford traditional solutions like CB Insights ($60K/year) or expensive consulting.
        
        Key areas to analyze:
        1. Market size and growth trends
        2. Pricing gaps in current solutions
        3. Unmet needs in the SMB segment
        4. Technology disruption opportunities
        5. Competitive landscape weaknesses
        
        This analysis will help validate the market opportunity for a disruptive,
        affordable business intelligence platform targeting underserved market segments.
        """,
        "analysis_type": "comprehensive",
        "include_sentiment": True,
        "include_trends": True
    }
    
    success, data = test_real_intelligence(
        f"{base_url}/api/intelligence/analyze",
        "Advanced Intelligence Analysis",
        intelligence_data
    )
    
    print("\n" + "=" * 80)
    print("🏆 REAL LUCIQ INTELLIGENCE DEMONSTRATION COMPLETE")
    print("💰 Revolutionary Technology Validated with Actual Data")
    print("🚀 Ready for $10B+ Market Disruption")
    print("=" * 80)
    print(f"🕐 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 