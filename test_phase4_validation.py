#!/usr/bin/env python3
"""
Phase 4 Testing & Validation - Simplified Validation Script
Luciq Modular Architecture Validation

Tests core functionality without external dependencies
"""

import sys
import os
import time
import tempfile
import asyncio
from pathlib import Path

def test_architecture_validation():
    """Test that all modular architecture files exist and can be imported"""
    print("🏗️ Testing Modular Architecture...")
    
    # Check that all service files exist
    service_files = [
        'src/services/__init__.py',
        'src/services/database_service.py',
        'src/services/auth_service.py',
        'src/services/reddit_client.py',
        'src/services/discovery_service.py',
        'src/services/intelligence/__init__.py',
        'src/services/intelligence/pain_point_engine.py',
        'src/api/main_modular.py',
        'src/api/routers/__init__.py',
        'src/api/routers/auth.py'
    ]
    
    missing_files = []
    for file_path in service_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing architecture files: {missing_files}")
        return False
    
    print("✅ All modular architecture files present")
    
    # Test imports
    try:
        from src.services.database_service import MasterDatabaseService
        from src.services.auth_service import AuthService
        from src.services.reddit_client import MasterRedditClient
        from src.services.discovery_service import MasterDiscoveryService
        from src.services.intelligence.pain_point_engine import PainPointDetectionEngine
        
        print("✅ All core services import successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_database_service():
    """Test database service functionality"""
    print("🗄️ Testing Database Service...")
    
    try:
        from src.services.database_service import MasterDatabaseService
        
        # Create temporary database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            # Test initialization
            db_service = MasterDatabaseService(db_path)
            assert db_service.db_path == db_path
            assert os.path.exists(db_path)
            
            print("✅ Database service initialization successful")
            return True
            
        finally:
            # Cleanup
            if os.path.exists(db_path):
                os.unlink(db_path)
                
    except Exception as e:
        print(f"❌ Database service test failed: {e}")
        return False

def test_auth_service():
    """Test authentication service functionality"""
    print("🔐 Testing Authentication Service...")
    
    try:
        from src.services.auth_service import AuthService
        from unittest.mock import Mock, AsyncMock
        
        # Mock database service
        mock_db = Mock()
        mock_db.get_user_by_username = AsyncMock()
        mock_db.create_user = AsyncMock()
        
        # Test initialization
        auth_service = AuthService(mock_db)
        assert auth_service.db_service == mock_db
        assert auth_service.pwd_context is not None
        
        # Test password hashing
        password = "test_password_123"
        hashed = auth_service.hash_password(password)
        
        assert hashed != password
        assert auth_service.verify_password(password, hashed)
        assert not auth_service.verify_password("wrong_password", hashed)
        
        # Test JWT token operations
        user_data = {"user_id": 1, "username": "testuser"}
        token = auth_service.create_access_token(user_data)
        assert token is not None
        assert isinstance(token, str)
        
        # Test token validation
        decoded = auth_service.verify_token(token)
        assert decoded is not None
        assert decoded["user_id"] == 1
        assert decoded["username"] == "testuser"
        
        print("✅ Authentication service tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Authentication service test failed: {e}")
        return False

def test_reddit_client():
    """Test Reddit client functionality"""
    print("🔍 Testing Reddit Client...")
    
    try:
        from src.services.reddit_client import MasterRedditClient
        
        # Test initialization
        client = MasterRedditClient()
        assert client.client_id is not None
        assert client.user_agent is not None
        assert client.access_token is None
        
        # Test that business keywords are defined
        assert hasattr(client, 'business_keywords')
        assert len(client.business_keywords) > 0
        
        print("✅ Reddit client tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Reddit client test failed: {e}")
        return False

def test_discovery_service():
    """Test discovery service functionality"""
    print("🔎 Testing Discovery Service...")
    
    try:
        from src.services.discovery_service import MasterDiscoveryService
        from unittest.mock import Mock, AsyncMock
        
        # Mock dependencies
        mock_db = Mock()
        mock_reddit = Mock()
        mock_db.save_pain_point = AsyncMock()
        mock_db.save_discovery_session = AsyncMock()
        mock_reddit.get_subreddit_posts = AsyncMock()
        
        # Test initialization
        service = MasterDiscoveryService(mock_db, mock_reddit)
        assert service.db_service == mock_db
        assert service.reddit_client == mock_reddit
        
        # Test pain point indicators
        pain_text = "this is so frustrating and difficult to use"
        assert service._has_pain_indicators(pain_text)
        
        normal_text = "this is a nice product that works well"
        assert not service._has_pain_indicators(normal_text)
        
        # Test market size scoring
        enterprise_text = "enterprise corporate solution for large companies"
        score = service._score_market_size(enterprise_text)
        assert score >= 2  # Should get high score
        
        small_text = "personal hobby project for individual use"
        score = service._score_market_size(small_text)
        assert score <= 2  # Should get lower score
        
        print("✅ Discovery service tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Discovery service test failed: {e}")
        return False

def test_pain_point_engine():
    """Test pain point detection engine"""
    print("🧠 Testing Pain Point Engine...")
    
    try:
        from src.services.intelligence.pain_point_engine import PainPointDetectionEngine
        
        # Test initialization
        engine = PainPointDetectionEngine()
        assert engine.pain_indicators is not None
        assert engine.opportunity_patterns is not None
        
        # Test pain pattern analysis
        pain_content = """
        I'm really frustrated with the current tools. They're expensive,
        difficult to use, and waste so much time. I've tried everything
        but nothing works well for small businesses.
        """
        
        analysis = engine._analyze_pain_patterns(pain_content)
        assert analysis['pain_detected'] is True
        assert analysis['pain_intensity'] > 0
        assert len(analysis['pain_categories']) > 0
        
        # Test business opportunity assessment
        pattern_analysis = {
            'pain_intensity': 0.7,
            'opportunity_types': ['saas_opportunity', 'productivity'],
            'pain_detected': True
        }
        
        opportunity = engine._assess_business_opportunity(
            "enterprise software automation solution",
            pattern_analysis
        )
        
        assert opportunity['opportunity_score'] > 0
        assert opportunity['market_size'] in ['small', 'medium', 'large']
        assert len(opportunity['opportunity_types']) > 0
        
        print("✅ Pain point engine tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Pain point engine test failed: {e}")
        return False

async def test_async_functionality():
    """Test async functionality of services"""
    print("⚡ Testing Async Functionality...")
    
    try:
        from src.services.intelligence.pain_point_engine import PainPointDetectionEngine
        
        engine = PainPointDetectionEngine()
        
        test_content = """
        As a startup founder, I'm struggling with project management.
        The current tools are too expensive for small businesses and
        difficult to integrate. We need something simple and affordable
        that actually helps with productivity and team collaboration.
        """
        
        result = await engine.detect_advanced_pain_points(
            content=test_content,
            platform="test_platform"
        )
        
        assert 'pain_point_detected' in result
        assert 'pain_intensity' in result
        assert 'business_opportunity' in result
        assert 'validation_score' in result
        assert result['analysis_metadata']['platform'] == "test_platform"
        
        print("✅ Async functionality tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Async functionality test failed: {e}")
        return False

def test_api_structure():
    """Test API structure and basic functionality"""
    print("🌐 Testing API Structure...")
    
    try:
        from src.api.main_modular import app
        
        # Test that app is created
        assert app is not None
        
        # Test that we can import FastAPI components
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test health endpoint
        response = client.get("/api/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        
        print("✅ API structure tests passed")
        return True
        
    except Exception as e:
        print(f"❌ API structure test failed: {e}")
        return False

def calculate_metrics():
    """Calculate and display metrics"""
    print("📊 Calculating Metrics...")
    
    # Count service files
    service_files = [
        'src/services/database_service.py',
        'src/services/auth_service.py',
        'src/services/reddit_client.py',
        'src/services/discovery_service.py',
        'src/services/intelligence/pain_point_engine.py'
    ]
    
    total_lines = 0
    for file_path in service_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
                total_lines += lines
                print(f"📄 {os.path.basename(file_path)}: {lines} lines")
    
    print(f"\n📈 Architecture Metrics:")
    print(f"   Modular Services: {len(service_files)}")
    print(f"   Total Service Lines: {total_lines}")
    print(f"   Average Lines per Service: {total_lines // len(service_files)}")
    
    # Calculate reduction from original monolithic file
    original_size = 7243  # From Phase 2 documentation
    reduction_percentage = ((original_size - total_lines) / original_size) * 100
    print(f"   File Size Reduction: {reduction_percentage:.1f}%")
    
    return True

def main():
    """Run Phase 4 validation"""
    print("🚀 Luciq Phase 4 Testing & Validation")
    print("=" * 60)
    print("Modular Architecture Validation Suite")
    print("=" * 60)
    
    # Test suites
    test_suites = [
        ("Architecture Validation", test_architecture_validation),
        ("Database Service", test_database_service),
        ("Authentication Service", test_auth_service),
        ("Reddit Client", test_reddit_client),
        ("Discovery Service", test_discovery_service),
        ("Pain Point Engine", test_pain_point_engine),
        ("API Structure", test_api_structure),
        ("Metrics Calculation", calculate_metrics)
    ]
    
    # Run async test separately
    async_test_result = False
    try:
        async_test_result = asyncio.run(test_async_functionality())
    except Exception as e:
        print(f"❌ Async test failed: {e}")
    
    # Run synchronous tests
    test_results = []
    for test_name, test_func in test_suites:
        print(f"\n🧪 Running {test_name}...")
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            test_results.append((test_name, False))
    
    # Add async test result
    test_results.append(("Async Functionality", async_test_result))
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 Phase 4 Validation Results")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
        if result:
            passed += 1
    
    print(f"\n📊 Overall Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 Phase 4 Testing & Validation: COMPLETE ✅")
        print("🏗️ Modular architecture fully validated!")
        print("🧪 All core functionality tests passing!")
        print("📈 Architecture metrics calculated!")
        print("\n🚀 Luciq system ready for production!")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("🔧 Please review failing tests")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 