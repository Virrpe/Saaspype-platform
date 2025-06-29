#!/usr/bin/env python3
"""
Phase 3 Integration Test Suite
Tests complete Phase 1 → Phase 2 → Phase 3 system integration
"""

import requests
import json
import time

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_CONTENT = """
I'm struggling with managing customer data across multiple platforms. We have customer information in Salesforce, support tickets in Zendesk, marketing data in HubSpot, and product usage in our internal database. 

It's taking hours to get a complete view of any customer, and our team is making decisions with incomplete information. We need a unified customer data platform that can pull from all these sources in real-time.

The manual work is killing our productivity. Our sales team is missing opportunities because they can't see the full customer journey. Our support team can't see past purchase history. Marketing can't see support issues when creating campaigns.

We've looked at existing solutions but they're either too expensive ($50k+ annually) or don't integrate with all our tools. Most solutions require months of implementation and custom development.

Is there a way to build a unified dashboard that could automatically sync and correlate data from all these platforms? Something that could give us a 360-degree customer view without breaking the bank?
"""

def test_api_status():
    """Test basic API connectivity"""
    print("🔍 Testing API Status...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Master API is running")
            return True
        else:
            print(f"❌ API Status Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Connection Failed: {e}")
        return False

def test_phase1_pain_point_detection():
    """Test Phase 1: PainPointDetectionEngine"""
    print("\n🎯 Testing Phase 1: Pain Point Detection...")
    try:
        payload = {
            "content": TEST_CONTENT,
            "platform": "reddit",
            "context": {"test_phase": "phase_1_integration"}
        }
        
        response = requests.post(
            f"{BASE_URL}/api/intelligence/pain-point-detection",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            validation_score = result.get('validation_score', 0)
            print(f"✅ Phase 1 Success - Validation Score: {validation_score:.3f}")
            print(f"   Pain Points Detected: {len(result.get('pain_points', []))}")
            print(f"   Business Opportunity: {result.get('business_opportunity', {}).get('market_size', 'Unknown')}")
            return result
        else:
            print(f"❌ Phase 1 Failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Phase 1 Error: {e}")
        return None

def test_phase2_solution_gap_analysis():
    """Test Phase 2: SolutionGapAnalyzer"""
    print("\n🔬 Testing Phase 2: Solution Gap Analysis...")
    try:
        payload = {
            "content": TEST_CONTENT,
            "platform": "reddit", 
            "context": {"test_phase": "phase_2_integration"}
        }
        
        response = requests.post(
            f"{BASE_URL}/api/intelligence/solution-gap-analysis",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            opportunity_score = result.get('opportunity_score', 0)
            print(f"✅ Phase 2 Success - Opportunity Score: {opportunity_score:.3f}")
            print(f"   Existing Solutions: {len(result.get('existing_solutions', []))}")
            print(f"   Bootstrap Feasibility: {result.get('bootstrap_feasibility', {}).get('feasibility_score', 'Unknown')}")
            return result
        else:
            print(f"❌ Phase 2 Failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Phase 2 Error: {e}")
        return None

def test_phase3_market_validation():
    """Test Phase 3: MarketValidationEngine"""
    print("\n🚀 Testing Phase 3: Market Validation...")
    try:
        payload = {
            "content": TEST_CONTENT,
            "platform": "reddit",
            "context": {"test_phase": "phase_3_integration"}
        }
        
        response = requests.post(
            f"{BASE_URL}/api/intelligence/market-validation",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            validation_score = result.get('validation_score', 0)
            print(f"✅ Phase 3 Success - Market Validation Score: {validation_score:.3f}")
            
            # Display market metrics
            market_metrics = result.get('market_metrics', {})
            print(f"   Market Size Score: {market_metrics.get('market_size_score', 'N/A')}")
            print(f"   Growth Rate Score: {market_metrics.get('growth_rate_score', 'N/A')}")
            print(f"   Competition Density: {market_metrics.get('competition_density', 'N/A')}")
            print(f"   Timing Score: {market_metrics.get('timing_score', 'N/A')}")
            
            # Display integration results
            integration = result.get('integration_results', {})
            print(f"   Phase 1 Integration: {integration.get('phase_1_pain_point_score', 'N/A')}")
            print(f"   Phase 2 Integration: {integration.get('phase_2_solution_gap_score', 'N/A')}")
            print(f"   Phase 3 Score: {integration.get('phase_3_market_validation_score', 'N/A')}")
            
            return result
        else:
            print(f"❌ Phase 3 Failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Phase 3 Error: {e}")
        return None

def test_api_capabilities():
    """Test API capabilities endpoints"""
    print("\n📋 Testing API Capabilities...")
    
    endpoints = [
        "/api/intelligence/pain-point-capabilities",
        "/api/intelligence/solution-gap-capabilities", 
        "/api/intelligence/market-validation-capabilities"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            if response.status_code == 200:
                print(f"✅ {endpoint.split('/')[-1].replace('-', ' ').title()}")
            else:
                print(f"❌ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")

def comprehensive_integration_test():
    """Run comprehensive 3-phase integration test"""
    print("=" * 80)
    print("🧪 PHASE 3 INTEGRATION TEST SUITE")
    print("=" * 80)
    print("Testing complete Phase 1 → Phase 2 → Phase 3 integration")
    print("Enterprise-grade Luciq Business Intelligence Platform")
    print("=" * 80)
    
    # Test API connectivity
    if not test_api_status():
        print("\n❌ CRITICAL: Master API not running. Please start the server first.")
        return False
    
    # Test each phase sequentially
    phase1_result = test_phase1_pain_point_detection()
    phase2_result = test_phase2_solution_gap_analysis()
    phase3_result = test_phase3_market_validation()
    
    # Test API capabilities
    test_api_capabilities()
    
    # Integration summary
    print("\n" + "=" * 80)
    print("🎯 INTEGRATION TEST SUMMARY")
    print("=" * 80)
    
    phases_success = 0
    if phase1_result:
        print("✅ Phase 1 (Pain Point Detection): OPERATIONAL")
        phases_success += 1
    else:
        print("❌ Phase 1 (Pain Point Detection): FAILED")
    
    if phase2_result:
        print("✅ Phase 2 (Solution Gap Analysis): OPERATIONAL")
        phases_success += 1
    else:
        print("❌ Phase 2 (Solution Gap Analysis): FAILED")
    
    if phase3_result:
        print("✅ Phase 3 (Market Validation): OPERATIONAL")
        phases_success += 1
    else:
        print("❌ Phase 3 (Market Validation): FAILED")
    
    print(f"\n🎯 SYSTEM STATUS: {phases_success}/3 Phases Operational")
    
    if phases_success == 3:
        print("🚀 REVOLUTIONARY PLATFORM STATUS: COMPLETE AND OPERATIONAL")
        print("💰 $10B+ Market Disruption Platform: READY FOR DEPLOYMENT")
        
        # Display comprehensive scoring
        if phase1_result and phase2_result and phase3_result:
            p1_score = phase1_result.get('validation_score', 0)
            p2_score = phase2_result.get('opportunity_score', 0) 
            p3_score = phase3_result.get('validation_score', 0)
            avg_score = (p1_score + p2_score + p3_score) / 3
            
            print(f"\n📊 COMPREHENSIVE INTELLIGENCE SCORES:")
            print(f"   Phase 1 (Pain Point): {p1_score:.3f}")
            print(f"   Phase 2 (Solution Gap): {p2_score:.3f}")
            print(f"   Phase 3 (Market Validation): {p3_score:.3f}")
            print(f"   🎯 OVERALL SYSTEM SCORE: {avg_score:.3f}")
            
        return True
    else:
        print("⚠️  INTEGRATION ISSUES DETECTED - Some phases need attention")
        return False

if __name__ == "__main__":
    comprehensive_integration_test() 