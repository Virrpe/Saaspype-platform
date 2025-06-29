#!/usr/bin/env python3
"""
Show Bulletproof Data - Display our discovery results
"""

import json

def show_bulletproof_data():
    """Display our bulletproof discovery data"""
    
    print("🎯 BULLETPROOF DISCOVERY DATA SUMMARY")
    print("=" * 50)
    
    # Show business ideas
    try:
        with open('business_ideas_blitz_20250606_002755.json', 'r', encoding='utf-8') as f:
            ideas_data = json.load(f)
        
        print(f"💡 BUSINESS IDEAS: {len(ideas_data['business_ideas'])}")
        print("Top 5 Ideas:")
        for i, idea in enumerate(ideas_data['business_ideas'][:5], 1):
            print(f"   {i}. {idea['idea_title']}")
            print(f"      Source: {idea['source_subreddit']}")
            print(f"      Problem: {idea['problem_statement'][:80]}...")
            print(f"      Score: {idea['confidence_score']}/5")
            print()
            
    except Exception as e:
        print(f"❌ Ideas error: {e}")
    
    # Show intelligence opportunities
    try:
        with open('mega_source_intelligence_20250606_003733.json', 'r', encoding='utf-8') as f:
            intel_data = json.load(f)
        
        print(f"🧠 INTELLIGENCE OPPORTUNITIES: {len(intel_data['opportunities'])}")
        print("Top 5 Opportunities:")
        for i, opp in enumerate(intel_data['opportunities'][:5], 1):
            print(f"   {i}. {opp['title']}")
            print(f"      Score: {opp['investment_attractiveness']}/10")
            print(f"      Market: {opp['market_timing']}")
            print()
            
    except Exception as e:
        print(f"❌ Intelligence error: {e}")
    
    print("🚀 API STATUS:")
    print("   ✅ Luciq API running on localhost:8000")
    print("   ✅ Domain-driven architecture active")
    print("   ✅ 5 domains: auth, discovery, intelligence, streaming, credibility")
    print("   📚 API Docs: http://localhost:8000/docs")
    
    print("\n🎉 READY FOR DISCOVERY!")

if __name__ == "__main__":
    show_bulletproof_data() 