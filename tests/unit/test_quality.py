#!/usr/bin/env python3
import sys
import asyncio
sys.path.append('tools/analyzers')

from signal_quality_enhancer import AdvancedSignalQualityEnhancer

async def test_quality():
    enhancer = AdvancedSignalQualityEnhancer()
    print("Quality thresholds:", enhancer.enhanced_thresholds)
    
    # Create test signals
    class TestSignal:
        def __init__(self, content):
            self.content = content
            self.source = "test"
            self.engagement_score = 50
            self.credibility_weight = 0.7
    
    test_signals = [
        TestSignal("Looking for SaaS solution to automate customer onboarding. Current manual process costs $200 and takes 3 hours."),
        TestSignal("Need automation tool for project management. Current system is inefficient and expensive."),
        TestSignal("Just had lunch today"),
        TestSignal("Weather is nice"),
        TestSignal("Building AI-powered analytics platform for small businesses. Early traction with 50 users.")
    ]
    
    enhanced = await enhancer.enhance_signals(test_signals)
    print(f"Input signals: {len(test_signals)}")
    print(f"Output signals: {len(enhanced)}")
    print(f"Retention rate: {len(enhanced)/len(test_signals)*100:.1f}%")
    
    for signal in enhanced:
        print(f"Quality: {signal.quality_score:.2f} - {signal.original_signal.content[:50]}...")

if __name__ == "__main__":
    asyncio.run(test_quality()) 