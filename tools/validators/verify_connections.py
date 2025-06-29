#!/usr/bin/env python3
"""
Luciq Connection Verification Script
Tests all interconnections before server startup
"""

import sys
import os
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    
    try:
        # Test streaming router imports
        from src.api.domains.streaming.endpoints.streaming_router import router as streaming_router
        print("  ✅ Streaming router imports successfully")
        
        # Test multimodal fusion engine
        from src.api.domains.intelligence.services.multimodal_fusion_engine import fusion_engine, MultiModalSignal, SignalType
        print("  ✅ Multimodal fusion engine imports successfully")
        
        # Test streaming pipeline
        from src.api.domains.streaming.services.streaming_trend_pipeline import GroundbreakingStreamingPipeline
        print("  ✅ Streaming pipeline imports successfully")
        
        # Test websocket broadcaster
        from src.api.domains.streaming.services.websocket_broadcaster import websocket_broadcaster
        print("  ✅ WebSocket broadcaster imports successfully")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Import error: {e}")
        return False

def test_pipeline_methods():
    """Test pipeline has correct methods"""
    print("🔍 Testing pipeline methods...")
    
    try:
        from src.api.domains.streaming.services.streaming_trend_pipeline import GroundbreakingStreamingPipeline
        
        pipeline = GroundbreakingStreamingPipeline()
        
        # Check required methods exist
        required_methods = [
            'get_pipeline_status',
            'ingest_signal_stream', 
            'start_streaming_pipeline',
            'stop_streaming_pipeline'
        ]
        
        for method_name in required_methods:
            if hasattr(pipeline, method_name):
                print(f"  ✅ {method_name} method exists")
            else:
                print(f"  ❌ {method_name} method missing")
                return False
        
        # Test get_pipeline_status returns correct structure
        status = pipeline.get_pipeline_status()
        expected_keys = ['is_streaming', 'uptime_seconds', 'statistics', 'windows']
        
        for key in expected_keys:
            if key in status:
                print(f"  ✅ Status contains '{key}'")
            else:
                print(f"  ❌ Status missing '{key}'")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Pipeline method test error: {e}")
        return False

def test_fusion_engine():
    """Test fusion engine functionality"""
    print("🔍 Testing fusion engine...")
    
    try:
        from src.api.domains.intelligence.services.multimodal_fusion_engine import fusion_engine
        
        # Check required methods
        required_methods = [
            'get_fusion_statistics',
            'process_multimodal_signal'
        ]
        
        for method_name in required_methods:
            if hasattr(fusion_engine, method_name):
                print(f"  ✅ {method_name} method exists")
            else:
                print(f"  ❌ {method_name} method missing")
                return False
        
        # Test get_fusion_statistics
        stats = fusion_engine.get_fusion_statistics()
        if isinstance(stats, dict):
            print("  ✅ Fusion statistics returns dict")
        else:
            print("  ❌ Fusion statistics returns wrong type")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Fusion engine test error: {e}")
        return False

def test_file_structure():
    """Test file structure is correct"""
    print("🔍 Testing file structure...")
    
    required_files = [
        'src/frontend/index.html',
        'src/frontend/pages/performance-showcase.html',
        'src/api/main.py',
        'start_api.py'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path} exists")
        else:
            print(f"  ❌ {file_path} missing")
            all_exist = False
    
    return all_exist

async def test_api_startup():
    """Test API can start without errors"""
    print("🔍 Testing API startup simulation...")
    
    try:
        # Import main API components
        from src.api.main import app
        print("  ✅ FastAPI app imports successfully")
        
        # Test streaming router integration
        from src.api.domains.streaming.endpoints.streaming_router import router
        print("  ✅ Streaming router ready for integration")
        
        return True
        
    except Exception as e:
        print(f"  ❌ API startup test error: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🚀 Luciq Connection Verification Starting...\n")
    
    tests = [
        ("Import Tests", test_imports),
        ("Pipeline Method Tests", test_pipeline_methods), 
        ("Fusion Engine Tests", test_fusion_engine),
        ("File Structure Tests", test_file_structure),
        ("API Startup Tests", lambda: asyncio.run(test_api_startup()))
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        
        try:
            result = test_func()
            if result:
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
            all_passed = False
    
    print("\n" + "="*50)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED! System ready for startup.")
        print("\n📋 Startup Instructions:")
        print("1. Terminal 1: python start_api.py")
        print("2. Terminal 2: cd src/frontend; python -m http.server 3000")
        print("3. Open: http://localhost:3000/")
        print("4. Performance Demo: http://localhost:3000/pages/performance-showcase.html")
    else:
        print("❌ SOME TESTS FAILED! Fix issues before startup.")
    
    print("="*50)
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 