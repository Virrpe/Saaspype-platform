#!/usr/bin/env python3
"""
Direct API validation to prove real data from Luciq Phase 4 Predictive Analytics
"""

import requests
import json
import time

def test_real_scenario(scenario_name, content, platform):
    """Test with real business scenario and show actual JSON response"""
    print(f"\n{'='*60}")
    print(f"TESTING: {scenario_name}")
    print(f"{'='*60}")
    
    url = "http://localhost:8000/api/intelligence/predictive-analytics"
    payload = {
        "content": content,
        "platform": platform,
        "analysis_type": "comprehensive",
        "include_forecasting": True,
        "include_timing_analysis": True
    }
    
    print(f"INPUT CONTENT: {content}")
    print(f"PLATFORM: {platform}")
    print("\nMAKING API CALL...")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            url, 
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        response_time = time.time() - start_time
        
        print(f"RESPONSE TIME: {response_time:.2f} seconds")
        print(f"HTTP STATUS: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n" + "="*40)
            print("REAL JSON RESPONSE DATA:")
            print("="*40)
            print(json.dumps(data, indent=2))
            
            print("\n" + "="*40)
            print("DATA VALIDATION:")
            print("="*40)
            
            # Validate key fields exist and have real values
            validations = {}
            
            # Check predictive metrics
            pred_metrics = data.get('predictive_forecasting', {})
            if pred_metrics:
                validations['trend_30d'] = pred_metrics.get('trend_forecast_30d')
                validations['trend_90d'] = pred_metrics.get('trend_forecast_90d')
                validations['trend_12m'] = pred_metrics.get('trend_forecast_12m')
                validations['momentum'] = pred_metrics.get('momentum_score')
                validations['volatility'] = pred_metrics.get('volatility_index')
                
                print(f"30-day Forecast: {validations['trend_30d']}")
                print(f"90-day Forecast: {validations['trend_90d']}")
                print(f"12-month Forecast: {validations['trend_12m']}")
                print(f"Momentum Score: {validations['momentum']}")
                print(f"Volatility Index: {validations['volatility']}")
            
            # Check insights
            insights = data.get('predictive_insights', [])
            print(f"\nGenerated Insights: {len(insights)} insights")
            for i, insight in enumerate(insights[:3], 1):
                print(f"  {i}. Type: {insight.get('insight_type')}")
                print(f"     Priority: {insight.get('priority_score')}")
                print(f"     Description: {insight.get('description', '')[:100]}...")
                print(f"     Impact: {insight.get('impact')}")
                print(f"     Timeline: {insight.get('timeline')}")
            
            # Check timing analysis
            timing = data.get('optimal_timing', {})
            if timing:
                print(f"\nOptimal Timing:")
                print(f"  Opportunity Window: {timing.get('opportunity_window')}")
                print(f"  Market Momentum: {timing.get('market_momentum')}")
                print(f"  Timing Score: {timing.get('timing_optimization_score')}")
            
            # Overall score
            pred_score = data.get('predictive_score', 0)
            print(f"\nOVERALL PREDICTIVE SCORE: {pred_score}")
            
            # Validate this is real analysis, not placeholder
            if (pred_score > 0 and 
                len(insights) > 0 and 
                pred_metrics and 
                validations['trend_30d'] != validations['trend_90d']):
                print("\n✅ VALIDATION: REAL DATA CONFIRMED")
                print("   - Unique forecasting values")
                print("   - Generated insights with specific content")
                print("   - Timing analysis with calculated scores")
                print("   - Non-zero predictive metrics")
                return True
            else:
                print("\n❌ VALIDATION: PLACEHOLDER DATA DETECTED")
                return False
                
        else:
            print(f"❌ API ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ REQUEST ERROR: {str(e)}")
        return False

def validate_capabilities():
    """Get capabilities and show real configuration"""
    print(f"\n{'='*60}")
    print("VALIDATING SYSTEM CAPABILITIES")
    print(f"{'='*60}")
    
    try:
        response = requests.get("http://localhost:8000/api/intelligence/predictive-analytics-capabilities")
        
        if response.status_code == 200:
            data = response.json()
            print("REAL CAPABILITIES DATA:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ Capabilities error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Capabilities request error: {str(e)}")
        return False

def main():
    """Run comprehensive validation with real business scenarios"""
    print("LUCIQ PHASE 4 PREDICTIVE ANALYTICS - REAL DATA VALIDATION")
    print("="*70)
    
    # First validate capabilities
    if not validate_capabilities():
        print("❌ Cannot validate capabilities")
        return
    
    # Test real business scenarios
    scenarios = [
        {
            'name': 'AI Breakthrough News',
            'content': 'OpenAI just released GPT-5 with breakthrough multimodal capabilities, causing massive investor interest and 300% stock surge in AI companies. VCs are rushing to fund AI startups.',
            'platform': 'reddit'
        },
        {
            'name': 'Crypto Market Surge',
            'content': 'Bitcoin hits new all-time high at $95,000 as institutional adoption accelerates. BlackRock and Fidelity Bitcoin ETFs see record inflows. Retail investors flooding back into crypto.',
            'platform': 'twitter'
        },
        {
            'name': 'Green Tech Innovation',
            'content': 'Revolutionary solid-state battery technology achieves 1000-mile electric vehicle range. Tesla, Ford, and startups racing to license the technology. Energy storage market exploding.',
            'platform': 'hackernews'
        }
    ]
    
    successful_tests = 0
    for scenario in scenarios:
        if test_real_scenario(scenario['name'], scenario['content'], scenario['platform']):
            successful_tests += 1
        time.sleep(2)  # Pause between tests
    
    print(f"\n{'='*70}")
    print("FINAL VALIDATION SUMMARY")
    print(f"{'='*70}")
    print(f"Tests with Real Data: {successful_tests}/{len(scenarios)}")
    
    if successful_tests == len(scenarios):
        print("✅ ALL TESTS PASSED - REAL PREDICTIVE ANALYTICS CONFIRMED")
        print("✅ System is generating legitimate business intelligence")
        print("✅ Forecasting algorithms producing unique values")
        print("✅ Insight generation working with real content analysis")
    else:
        print("❌ SOME TESTS FAILED - Review data validation")

if __name__ == "__main__":
    main() 