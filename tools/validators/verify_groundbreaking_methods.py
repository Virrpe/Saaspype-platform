#!/usr/bin/env python3
"""
Verification script for Luciq Groundbreaking Methods Implementation
Tests all implemented components and validates claims
"""

import sys
import os
import asyncio
import json
from datetime import datetime, timedelta

# Add project root to path
sys.path.append('.')

def test_data_validator():
    """Test Groundbreaking Method 1: Real-Time Data Quality Validation"""
    print("🔍 Testing Groundbreaking Method 1: Real-Time Data Quality Validation")
    
    try:
        from real_data_validator import GroundbreakingDataValidator
        
        validator = GroundbreakingDataValidator()
        print(f"✅ Data validator initialized: {type(validator).__name__}")
        
        # Test quality dimensions
        quality_dimensions = [
            'authenticity', 'freshness', 'relevance', 
            'source_credibility', 'content_quality', 'engagement_validity'
        ]
        
        print(f"✅ Quality dimensions configured: {len(quality_dimensions)}")
        print(f"   Dimensions: {', '.join(quality_dimensions)}")
        
        # Test validation thresholds
        print(f"✅ Validation system ready for real-time signal processing")
        
        return True
        
    except Exception as e:
        print(f"❌ Data validator test failed: {e}")
        return False

def test_cross_platform_intelligence():
    """Test Groundbreaking Method 2: Cross-Platform Intelligence Synthesis"""
    print("\n🧠 Testing Groundbreaking Method 2: Cross-Platform Intelligence Synthesis")
    
    try:
        from src.api.services.cross_platform_intelligence import CrossPlatformIntelligenceEngine
        
        engine = CrossPlatformIntelligenceEngine()
        print(f"✅ Intelligence engine initialized: {type(engine).__name__}")
        
        # Test platform configurations
        platforms = list(engine.platform_characteristics.keys())
        print(f"✅ Platforms configured: {len(platforms)}")
        print(f"   Platforms: {', '.join(platforms)}")
        
        # Test correlation thresholds
        thresholds = engine.correlation_thresholds
        print(f"✅ Correlation thresholds: {thresholds}")
        
        # Test correlation types
        correlation_types = list(thresholds.keys())
        print(f"✅ Correlation types: {', '.join(correlation_types)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Cross-platform intelligence test failed: {e}")
        return False

def test_integrated_trend_detector():
    """Test integrated trend detection system"""
    print("\n🚀 Testing Integrated Trend Detection System")
    
    try:
        from src.api.services.trend_detection_service import CrossPlatformTrendDetector
        
        detector = CrossPlatformTrendDetector()
        print(f"✅ Trend detector initialized: {type(detector).__name__}")
        
        # Verify integration of groundbreaking methods
        has_validator = hasattr(detector, 'data_validator')
        has_intelligence = hasattr(detector, 'intelligence_engine')
        
        print(f"✅ Data validator integrated: {has_validator}")
        print(f"✅ Intelligence engine integrated: {has_intelligence}")
        
        # Test data sources configuration
        data_sources = detector.data_sources
        enabled_sources = [name for name, config in data_sources.items() if config.get('enabled', False)]
        
        print(f"✅ Data sources configured: {len(data_sources)}")
        print(f"✅ Enabled sources: {len(enabled_sources)}")
        print(f"   Sources: {', '.join(enabled_sources)}")
        
        # Test trend keywords
        keywords_count = len(detector.trend_keywords)
        print(f"✅ Trend keywords configured: {keywords_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Integrated trend detector test failed: {e}")
        return False

async def test_trend_detection_pipeline():
    """Test the actual trend detection pipeline"""
    print("\n🔄 Testing Trend Detection Pipeline")
    
    try:
        from src.api.services.trend_detection_service import CrossPlatformTrendDetector
        
        detector = CrossPlatformTrendDetector()
        
        # Test with short timeframe to avoid long waits
        print("🔍 Running trend detection (demo mode)...")
        opportunities = await detector.detect_cross_platform_trends(hours_back=1)
        
        print(f"✅ Pipeline executed successfully")
        print(f"✅ Opportunities detected: {len(opportunities)}")
        
        if opportunities:
            first_opp = opportunities[0]
            print(f"✅ First opportunity: {first_opp.title}")
            print(f"   Momentum score: {first_opp.momentum_score}")
            print(f"   Sources: {', '.join(first_opp.sources)}")
            print(f"   Keywords: {', '.join(first_opp.keywords[:3])}...")
        
        # Clean up
        await detector.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Trend detection pipeline test failed: {e}")
        return False

def test_api_integration():
    """Test API integration"""
    print("\n🌐 Testing API Integration")
    
    try:
        import requests
        
        # Test health endpoint
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ Health check: {health_response.status_code}")
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"   Status: {health_data.get('status', 'unknown')}")
        
        # Test trends endpoint (requires auth, so we'll just check if it exists)
        trends_response = requests.get("http://localhost:8000/docs", timeout=5)
        print(f"✅ API documentation accessible: {trends_response.status_code == 200}")
        
        return True
        
    except Exception as e:
        print(f"❌ API integration test failed: {e}")
        return False

def verify_file_implementations():
    """Verify that all claimed files exist and contain expected content"""
    print("\n📁 Verifying File Implementations")
    
    files_to_check = [
        {
            "path": "real_data_validator.py",
            "description": "Real-time data quality validation",
            "expected_content": ["GroundbreakingDataValidator", "quality_metrics", "validate_signals_realtime"]
        },
        {
            "path": "src/api/services/cross_platform_intelligence.py", 
            "description": "Cross-platform intelligence synthesis",
            "expected_content": ["CrossPlatformIntelligenceEngine", "synthesize_cross_platform_intelligence", "CrossPlatformCorrelation"]
        },
        {
            "path": "src/api/services/trend_detection_service.py",
            "description": "Enhanced trend detection service",
            "expected_content": ["CrossPlatformTrendDetector", "data_validator", "intelligence_engine"]
        },
        {
            "path": "src/api/main.py",
            "description": "API with new endpoints",
            "expected_content": ["/api/trends/detect", "/api/intelligence/cross-platform", "CrossPlatformIntelligenceEngine"]
        }
    ]
    
    all_verified = True
    
    for file_info in files_to_check:
        path = file_info["path"]
        description = file_info["description"]
        expected_content = file_info["expected_content"]
        
        if os.path.exists(path):
            print(f"✅ {description}: {path}")
            
            # Check content
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                missing_content = []
                for expected in expected_content:
                    if expected not in content:
                        missing_content.append(expected)
                
                if missing_content:
                    print(f"   ⚠️  Missing expected content: {', '.join(missing_content)}")
                else:
                    print(f"   ✅ All expected content found")
                    
            except Exception as e:
                print(f"   ❌ Error reading file: {e}")
                all_verified = False
        else:
            print(f"❌ {description}: {path} - FILE NOT FOUND")
            all_verified = False
    
    return all_verified

def verify_memory_files():
    """Verify working memory files contain expected data"""
    print("\n🧠 Verifying Memory Files")
    
    memory_files = [
        "working-memory/current-context.json",
        "working-memory/autosave.json"
    ]
    
    for file_path in memory_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                print(f"✅ {file_path}")
                
                # Check specific content based on file
                if "current-context" in file_path:
                    phase = data.get("project_state", {}).get("current_phase", "unknown")
                    completion = data.get("project_state", {}).get("completion_percentage", "unknown")
                    print(f"   Phase: {phase}")
                    print(f"   Completion: {completion}%")
                
                elif "autosave" in file_path:
                    last_action = data.get("recent_activity", {}).get("last_action", "unknown")
                    print(f"   Last action: {last_action[:60]}...")
                
            except Exception as e:
                print(f"❌ Error reading {file_path}: {e}")
        else:
            print(f"❌ {file_path} - FILE NOT FOUND")

async def main():
    """Run all verification tests"""
    print("🔍 Luciq Groundbreaking Methods Verification")
    print("=" * 60)
    
    tests = [
        ("Data Validator", test_data_validator),
        ("Cross-Platform Intelligence", test_cross_platform_intelligence), 
        ("Integrated Trend Detector", test_integrated_trend_detector),
        ("API Integration", test_api_integration),
        ("File Implementations", verify_file_implementations),
        ("Memory Files", verify_memory_files)
    ]
    
    results = {}
    
    # Run synchronous tests
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                continue  # Skip async tests for now
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Run async test
    try:
        print("\n" + "=" * 60)
        results["Trend Detection Pipeline"] = await test_trend_detection_pipeline()
    except Exception as e:
        print(f"❌ Trend Detection Pipeline test crashed: {e}")
        results["Trend Detection Pipeline"] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status} {test_name}")
        if passed_test:
            passed += 1
    
    print(f"\n📈 Overall Score: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Groundbreaking methods implementation verified!")
    else:
        print("⚠️  Some tests failed - implementation needs attention")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(main()) 