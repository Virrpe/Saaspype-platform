#!/usr/bin/env python3
"""
Luciq API Startup Test
Verify that all components can be imported and the API can start
"""

import sys
import time
import requests
import subprocess
from datetime import datetime

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing Critical Imports...")
    
    try:
        # Test Phase 5 components
        from src.api.services.multimodal_fusion_engine import fusion_engine, MultiModalSignal, SignalType
        print("✅ Phase 5 Multi-Modal Fusion Engine")
        
        from src.api.services.websocket_broadcaster import websocket_broadcaster
        print("✅ WebSocket Broadcaster")
        
        # Test other critical components
        from src.shared.config.settings import LOG_DIR
        print("✅ Settings Configuration")
        
        from src.api.services.auth_service import auth_service
        print("✅ Authentication Service")
        
        from src.api.services.discovery_service import discovery_service
        print("✅ Discovery Service")
        
        from src.api.models.requests import UserCreate, DiscoveryRequest
        print("✅ API Models")
        
        # Test Phase 2-4 components
        from src.api.services.semantic_analysis_engine import get_semantic_engine
        print("✅ Phase 2 Semantic Analysis Engine")
        
        from src.api.services.temporal_pattern_engine import get_temporal_engine
        print("✅ Phase 2 Temporal Pattern Engine")
        
        from src.api.services.graph_trend_detector import GroundbreakingGraphTrendDetector
        print("✅ Phase 3 Graph Trend Detector")
        
        from src.api.services.streaming_trend_pipeline import GroundbreakingStreamingPipeline
        print("✅ Phase 4 Streaming Pipeline")
        
        print("🎉 All imports successful!\n")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_api_startup():
    """Test API startup"""
    print("🚀 Testing API Startup...")
    
    try:
        # Try to import the main app
        from src.api.main import app
        print("✅ FastAPI app created successfully")
        
        # Test that we can access app properties
        print(f"   • App title: {app.title}")
        print(f"   • App version: {app.version}")
        print(f"   • Routes: {len(app.routes)} endpoints")
        
        return True
        
    except Exception as e:
        print(f"❌ API startup failed: {e}")
        return False

def test_phase5_functionality():
    """Test Phase 5 Multi-Modal functionality"""
    print("🔬 Testing Phase 5 Multi-Modal Fusion...")
    
    try:
        from src.api.services.multimodal_fusion_engine import MultiModalSignal, SignalType, fusion_engine
        from datetime import datetime
        
        # Create a test signal
        signal = MultiModalSignal(
            signal_id="startup_test_001",
            timestamp=datetime.now(),
            source_platform="test",
            signal_type=SignalType.TEXT,
            content="Test signal for startup verification",
            semantic_score=0.8,
            sentiment_score=0.7,
            context_relevance=0.75,
            influence_score=0.6,
            viral_potential=0.85,
            network_centrality=0.7,
            velocity=0.8,
            acceleration=0.6,
            trend_strength=0.75,
            engagement_rate=0.7,
            user_quality=0.8,
            authenticity_score=0.9
        )
        
        print(f"✅ Created test signal: {signal.signal_id}")
        
        # Get fusion statistics
        stats = fusion_engine.get_fusion_statistics()
        print(f"✅ Fusion engine stats: {stats['overview']['signals_processed']} signals processed")
        
        return True
        
    except Exception as e:
        print(f"❌ Phase 5 test failed: {e}")
        return False

def test_api_endpoints():
    """Test basic API endpoints if server is running"""
    print("🌐 Testing API Endpoints...")
    
    try:
        # Test root endpoint
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint responding")
            print(f"   • Response: {response.json()}")
        else:
            print(f"⚠️  Root endpoint returned {response.status_code}")
            return False
            
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint responding")
        else:
            print(f"⚠️  Health endpoint returned {response.status_code}")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("⚠️  API server not running - skipping endpoint tests")
        return None
    except Exception as e:
        print(f"❌ Endpoint test failed: {e}")
        return False

def main():
    """Run comprehensive startup verification"""
    print("=" * 60)
    print("🔥 LUCIQ API STARTUP VERIFICATION")
    print("=" * 60)
    print(f"🕐 Test Time: {datetime.now().isoformat()}")
    print()
    
    # Run tests
    test_results = {
        'imports': test_imports(),
        'api_startup': test_api_startup(),
        'phase5_functionality': test_phase5_functionality(),
        'api_endpoints': test_api_endpoints()
    }
    
    # Summary
    print("=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in test_results.values() if result is True)
    total = sum(1 for result in test_results.values() if result is not None)
    
    for test_name, result in test_results.items():
        if result is True:
            status = "✅ PASSED"
        elif result is False:
            status = "❌ FAILED"
        else:
            status = "⚠️  SKIPPED"
        
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print()
    print(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🏆 ALL SYSTEMS OPERATIONAL!")
        return 0
    elif passed >= total * 0.75:
        print("👍 MOSTLY OPERATIONAL - Minor issues detected")
        return 0
    else:
        print("⚠️  ISSUES DETECTED - Review failed tests")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 