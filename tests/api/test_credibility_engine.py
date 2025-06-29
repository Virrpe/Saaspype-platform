#!/usr/bin/env python3
"""
Test script for Source Credibility Engine
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_credibility_engine():
    """Test the Source Credibility Engine"""
    try:
        print("🎯 Testing Source Credibility Engine")
        print("=" * 50)
        
        # Import and initialize
        from src.api.services.source_credibility_engine import SourceCredibilityEngine
        engine = SourceCredibilityEngine()
        print("✅ Engine initialized successfully")
        
        # Test platform scoring
        print("\n📊 Platform Credibility Scores:")
        platforms = ['reddit', 'twitter', 'github', 'hackernews', 'producthunt']
        
        for platform in platforms:
            score = engine.calculate_platform_credibility(platform)
            weight = engine.get_source_weight(platform)
            print(f"  {platform:12}: {score.overall_score:.3f} (weight: {weight:.2f}x)")
        
        # Generate comprehensive report
        print("\n📋 Generating credibility report...")
        report = engine.get_platform_credibility_report()
        
        print(f"✅ Report generated:")
        print(f"  Total platforms: {report['total_platforms']}")
        print(f"  Average credibility: {report['summary']['average_credibility']:.3f}")
        
        if report['summary']['highest_credibility']:
            best = report['summary']['highest_credibility']
            print(f"  Highest credibility: {best['platform']} ({best['score']:.3f})")
        
        if report['summary']['lowest_credibility']:
            worst = report['summary']['lowest_credibility']
            print(f"  Lowest credibility: {worst['platform']} ({worst['score']:.3f})")
        
        # Test signal verification
        print(f"\n🔍 Testing signal verification...")
        engine.record_signal_verification(
            signal_id="test_signal_001",
            platform="reddit",
            source_id="r/entrepreneur",
            predicted_trend="AI automation tools",
            actual_outcome="Confirmed trending",
            accuracy_score=0.85
        )
        print("✅ Signal verification recorded")
        
        print(f"\n🎉 All tests passed! Source Credibility Engine operational.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_credibility_engine()
    sys.exit(0 if success else 1) 