#!/usr/bin/env python3
"""
Test Enhanced Analysis Fix
"""

import asyncio
from multi_platform_pain_analyzer import MultiPlatformPainAnalyzer

async def test_enhanced_analysis():
    """Test the enhanced analysis with real sample data"""
    
    print("🧠 TESTING ENHANCED ANALYSIS AFTER TEMPLATE FIX")
    print("=" * 60)
    
    analyzer = MultiPlatformPainAnalyzer()
    
    # Test with real pain point
    sample_content = {
        'title': 'Customer support is overwhelming our small team',
        'description': 'We have 500 customers but only 2 support people. Tickets are piling up and response times are terrible. Need automation but existing tools are too expensive.',
        'source': 'reddit',
        'url': 'https://reddit.com/r/startups/test',
        'score': 45,
        'platform_type': 'test'
    }
    
    print("📝 Testing sample content:")
    print(f"   Title: {sample_content['title']}")
    print(f"   Description: {sample_content['description'][:80]}...")
    print()
    
    try:
        analysis = await analyzer._analyze_content_item(sample_content)
        
        if analysis:
            print("✅ ENHANCED ANALYSIS SUCCESS!")
            print(f"   🎯 Pain Point: {analysis['pain_point'][:80]}...")
            print(f"   📊 Total Score: {analysis['total_score']}/10")
            print(f"   🏭 Domain: {analysis['domain']}")
            print(f"   💡 Opportunity: {analysis['opportunity_description'][:80]}...")
            print(f"   ✅ Validation: {', '.join(analysis['validation_signals'][:2])}")
            print(f"   🎯 Confidence: {analysis['confidence']:.2f}")
            print()
            print("🎉 TEMPLATE ELIMINATION FIX: SUCCESSFUL!")
            print("🚀 Enhanced analysis now works with real content!")
        else:
            print("❌ Enhanced analysis still failing")
            print("🔍 Debugging needed...")
            
            # Debug step by step
            print("\n🔍 DEBUGGING ENHANCED ANALYSIS:")
            
            # Test pain detection
            combined_text = f"{sample_content['title']}\n\n{sample_content['description']}"
            has_pain, indicators = analyzer._detect_pain_indicators(combined_text)
            print(f"   Pain detected: {has_pain}")
            print(f"   Indicators: {indicators}")
            print(f"   Indicators type: {type(indicators)}")
            
            # Test quality filter
            passes_quality = analyzer._passes_quality_filter(sample_content)
            print(f"   Passes quality filter: {passes_quality}")
            
            if has_pain and passes_quality:
                print("   🔍 Both checks passed, testing individual components...")
                
                # Test pain point extraction
                pain_point = analyzer._extract_pain_point_description(combined_text)
                print(f"   Pain point: {pain_point}")
                
                # Test scoring
                market_size = analyzer._score_market_size(combined_text)
                urgency = analyzer._score_urgency(combined_text)
                solution_gap = analyzer._score_solution_gap(combined_text)
                monetization = analyzer._score_monetization(combined_text)
                print(f"   Scores: market={market_size}, urgency={urgency}, gap={solution_gap}, monetization={monetization}")
                
                # Test validation signals
                try:
                    validation_signals = analyzer._extract_validation_signals(sample_content, combined_text, indicators)
                    print(f"   Validation signals: {validation_signals}")
                except Exception as e:
                    print(f"   ❌ Error in validation signals: {e}")
            
            if not has_pain:
                print("   ❌ Issue: Pain indicators not detected")
            elif not passes_quality:
                print("   ❌ Issue: Quality filter failed")
            else:
                print("   ❌ Issue: Unknown problem in analysis")
            
    except Exception as e:
        print(f"❌ Error in enhanced analysis: {e}")
        import traceback
        traceback.print_exc()
    
    await analyzer.close()

if __name__ == "__main__":
    asyncio.run(test_enhanced_analysis()) 