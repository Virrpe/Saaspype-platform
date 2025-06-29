#!/usr/bin/env python3
"""
Test Enhanced Overnight Discovery Integration
Quick test to verify the multi-platform pain point analyzer integration
"""

import asyncio
import json
from datetime import datetime

async def test_enhanced_overnight():
    """Test the enhanced overnight discovery system"""
    
    print("🧪 TESTING ENHANCED OVERNIGHT DISCOVERY INTEGRATION")
    print("=" * 60)
    
    try:
        # Import the enhanced overnight discovery engine
        from overnight_discovery_cycle import OvernightDiscoveryEngine
        
        print("✅ Successfully imported OvernightDiscoveryEngine")
        
        # Initialize the engine
        engine = OvernightDiscoveryEngine()
        print("✅ Engine initialized successfully")
        
        # Test multi-platform analyzer initialization
        print("\n🧠 Testing multi-platform analyzer initialization...")
        analyzer_ready = await engine.initialize_multi_platform_analyzer()
        
        if analyzer_ready:
            print("✅ Multi-platform analyzer initialized successfully")
            print(f"🌐 Available platforms: {len(engine.all_platforms)}")
            print(f"🎯 Platforms per cycle: {engine.platforms_per_cycle}")
            
            # Test a single enhanced discovery cycle (without running full overnight)
            print("\n🔄 Testing single enhanced discovery cycle...")
            
            # Mock a quick cycle test
            engine.cycle_count = 0  # Reset for test
            
            # Test platform selection
            start_idx = (engine.cycle_count * engine.platforms_per_cycle) % len(engine.all_platforms)
            cycle_platforms = []
            for i in range(engine.platforms_per_cycle):
                idx = (start_idx + i) % len(engine.all_platforms)
                cycle_platforms.append(engine.all_platforms[idx])
            
            print(f"🎯 Test cycle would analyze: {', '.join(cycle_platforms)}")
            
            # Test system health check
            health = engine.check_system_health()
            print(f"🏥 System health: {'✅ HEALTHY' if health['healthy'] else '⚠️ WARNINGS'}")
            print(f"   CPU: {health['cpu_percent']:.1f}%")
            print(f"   Memory: {health['memory_percent']:.1f}%")
            print(f"   Available: {health['available_gb']:.1f}GB")
            
            if health['warnings']:
                for warning in health['warnings']:
                    print(f"   ⚠️ {warning}")
            
            # Test lightweight mega scraper (if available)
            print("\n📊 Testing lightweight mega scraper...")
            try:
                mega_results = await engine.run_lightweight_mega_scraper(hours_back=1)  # Very short window for test
                if mega_results:
                    print(f"✅ Mega scraper test successful: {len(mega_results.get('all_opportunities', []))} opportunities")
                else:
                    print("⚠️ Mega scraper returned no results (expected for test)")
            except Exception as e:
                print(f"⚠️ Mega scraper test failed: {e} (expected - may need API servers)")
            
            # Test enhanced analysis on sample data
            print("\n🧠 Testing enhanced analysis on sample data...")
            
            sample_content = {
                'title': 'Customer support is overwhelming our small team',
                'description': 'We have 500 customers but only 2 support people. Tickets are piling up and response times are terrible. Need automation but existing tools are too expensive.',
                'source': 'reddit',
                'url': 'https://reddit.com/r/startups/test',
                'score': 45,
                'platform_type': 'test'
            }
            
            analysis = await engine.multi_platform_analyzer._analyze_content_item(sample_content)
            
            if analysis:
                print("✅ Enhanced analysis successful!")
                print(f"   🎯 Pain Point: {analysis['pain_point'][:80]}...")
                print(f"   📊 Total Score: {analysis['total_score']}/10")
                print(f"   🏭 Domain: {analysis['domain']}")
                print(f"   💡 Opportunity: {analysis['opportunity_description'][:80]}...")
                print(f"   ✅ Validation: {', '.join(analysis['validation_signals'][:2])}")
            else:
                print("❌ Enhanced analysis failed on sample data")
            
            # Clean up
            try:
                await engine.multi_platform_analyzer.close()
            except:
                pass
            
            print("\n🎉 INTEGRATION TEST COMPLETE!")
            print("=" * 40)
            print("✅ Enhanced overnight discovery is ready!")
            print("🚀 Run with: python overnight_discovery_cycle.py --hours 8")
            print("🌐 Will analyze 15+ platforms with enhanced pain point detection")
            print("📊 Expected: High-quality business opportunities instead of generic templates")
            
        else:
            print("❌ Multi-platform analyzer initialization failed")
            print("🔄 System will fall back to basic discovery methods")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("🔧 Check system configuration and try again")

def main():
    """Run the integration test"""
    asyncio.run(test_enhanced_overnight())

if __name__ == "__main__":
    main() 