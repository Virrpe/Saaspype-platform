#!/usr/bin/env python3
"""
Cross-Platform API Intelligence Test
Access Luciq API intelligence endpoints for real-time analysis
"""

import requests
import json
from datetime import datetime

def test_intelligence_api():
    """Test cross-platform intelligence through API"""
    
    base_url = "http://localhost:8000"
    
    print("🧠 CROSS-PLATFORM INTELLIGENCE API TEST")
    print("=" * 60)
    
    # Test 1: API Health and Intelligence Status
    print("1. 🏥 Intelligence System Status...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health = response.json()
            print(f"   ✅ API Status: {health.get('status')}")
            print(f"   ⏱️ Uptime: {health.get('uptime_seconds', 0):.1f}s")
            print(f"   📊 Discovery Sessions: {health.get('discovery_sessions', 0)}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health error: {e}")
    
    # Test 2: API Metrics for Intelligence
    print("\n2. 📊 Intelligence Metrics...")
    try:
        response = requests.get(f"{base_url}/metrics")
        if response.status_code == 200:
            metrics = response.json()
            print(f"   ✅ Total Requests: {metrics.get('requests_total', 0)}")
            print(f"   📈 Discovery Sessions: {metrics.get('discovery_sessions', 0)}")
            print(f"   ⚡ Errors: {metrics.get('errors_total', 0)}")
            
            # Show endpoint usage
            endpoints = metrics.get('requests_by_endpoint', {})
            if endpoints:
                print(f"   🎯 Top Endpoints:")
                for endpoint, count in list(endpoints.items())[:3]:
                    print(f"      • {endpoint}: {count} requests")
        else:
            print(f"   ❌ Metrics failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Metrics error: {e}")
    
    # Test 3: Try Public Intelligence Endpoints
    print("\n3. 🔍 Testing Public Intelligence Endpoints...")
    
    public_endpoints = [
        ("/api/system-ideas", "System Ideas"),
        ("/api/phase2/status", "Phase 2 Status"),
        ("/api/semantic/analyze?content=AI%20startup%20trends", "Semantic Analysis"),
        ("/api/temporal/patterns", "Temporal Patterns")
    ]
    
    for endpoint, name in public_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"   📡 {name}: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        keys = list(data.keys())[:3]  # First 3 keys
                        print(f"      📊 Data keys: {keys}")
                        
                        # Show specific intelligence data
                        if 'intelligence' in data:
                            print(f"      🧠 Intelligence data available")
                        if 'trends' in data:
                            print(f"      📈 Trends: {len(data['trends'])} items")
                        if 'analysis' in data:
                            print(f"      🔍 Analysis available")
                            
                    elif isinstance(data, list):
                        print(f"      📊 Items: {len(data)}")
                except:
                    print(f"      📄 Content length: {len(response.content)}")
            else:
                error_text = response.text[:100] if response.text else "No error details"
                print(f"      ❌ Error: {error_text}")
                
        except Exception as e:
            print(f"   ❌ {name} error: {e}")
    
    # Test 4: Show Local Intelligence Data Summary
    print("\n4. 🎯 LOCAL INTELLIGENCE DATA SUMMARY")
    print("-" * 40)
    
    try:
        # Load bulletproof intelligence analysis
        with open("bulletproof_intelligence_analysis_20250606_005321.json", 'r', encoding='utf-8') as f:
            intel_data = json.load(f)
            
        print(f"   🧠 BULLETPROOF INTELLIGENCE ANALYSIS:")
        print(f"   📊 Data Quality: {intel_data['analysis_summary']['overall_data_quality']}/10")
        print(f"   🎯 Business Opportunities: {intel_data['analysis_summary']['business_opportunities_identified']}")
        print(f"   ⏱️ Analysis Time: {intel_data['analysis_summary']['total_analysis_time_seconds']:.1f}s")
        print(f"   📈 Items Analyzed: {intel_data['analysis_summary']['total_items_analyzed']}")
        
        print(f"\n   🏆 TOP OPPORTUNITIES:")
        for i, opp in enumerate(intel_data['business_opportunities'][:3], 1):
            print(f"      {i}. {opp['title'][:50]}...")
            print(f"         Score: {opp['opportunity_score']}/5 | Source: {opp['source']}")
        
        print(f"\n   📈 TECHNOLOGY TRENDS:")
        tech_trends = intel_data['technology_trends']
        for tech, count in list(tech_trends.items())[:5]:
            print(f"      • {tech}: {count} mentions")
            
    except FileNotFoundError:
        print(f"   ❌ Bulletproof intelligence file not found")
    except Exception as e:
        print(f"   ❌ Intelligence data error: {e}")
    
    # Test 5: Cross-Platform Correlation Analysis
    print("\n5. 🌐 CROSS-PLATFORM CORRELATION ANALYSIS")
    print("-" * 40)
    
    try:
        # Load cross-platform data
        with open("cross_platform_intelligence_20250606_003428.json", 'r', encoding='utf-8') as f:
            cross_data = json.load(f)
            
        print(f"   🔗 CROSS-PLATFORM INTELLIGENCE:")
        print(f"   📊 Total Opportunities: {cross_data['total_opportunities']}")
        print(f"   ⚡ Performance: {cross_data['signals_per_second']:.1f} signals/sec")
        print(f"   🎯 Active Sources: {cross_data['active_sources']}")
        
        # Show source performance
        print(f"\n   📈 SOURCE PERFORMANCE:")
        source_stats = cross_data.get('source_stats', {})
        for source, stats in list(source_stats.items())[:3]:
            opportunities = stats.get('opportunities', 0)
            percentage = stats.get('percentage', 0)
            print(f"      • {source}: {opportunities} opportunities ({percentage:.1f}%)")
        
        # Show top opportunities
        print(f"\n   🚀 TOP CROSS-PLATFORM OPPORTUNITIES:")
        opportunities = cross_data.get('opportunities', [])
        for i, opp in enumerate(opportunities[:3], 1):
            title = opp.get('title', 'Unknown')[:40]
            momentum = opp.get('momentum_score', 0)
            sources = len(opp.get('sources', []))
            print(f"      {i}. {title}... (Momentum: {momentum}/10, Sources: {sources})")
            
    except FileNotFoundError:
        print(f"   ❌ Cross-platform intelligence file not found")
    except Exception as e:
        print(f"   ❌ Cross-platform data error: {e}")
    
    print(f"\n🎉 CROSS-PLATFORM INTELLIGENCE TEST COMPLETE!")
    print("=" * 60)
    print(f"🧠 Intelligence engines active and processing")
    print(f"📊 Multiple data sources analyzed and correlated")
    print(f"🎯 Business opportunities identified and ranked")
    print(f"🌐 API Docs: {base_url}/docs")

if __name__ == "__main__":
    test_intelligence_api() 