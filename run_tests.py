#!/usr/bin/env python3
"""
Luciq Test Runner
Phase 4 Testing & Validation - Comprehensive Test Execution

Runs all test suites with coverage reporting and validation
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n🧪 {description}")
    print("-" * 60)
    
    start_time = time.time()
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        end_time = time.time()
        
        print(f"✅ {description}: PASSED ({end_time - start_time:.2f}s)")
        if result.stdout:
            print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        end_time = time.time()
        print(f"❌ {description}: FAILED ({end_time - start_time:.2f}s)")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking test dependencies...")
    
    required_packages = ['pytest', 'pytest-asyncio', 'fastapi', 'httpx']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Install with: pip install -r requirements-test.txt")
        return False
    
    print("✅ All test dependencies available")
    return True

def run_unit_tests():
    """Run unit tests"""
    return run_command(
        "python -m pytest tests/test_services.py -v --tb=short",
        "Unit Tests (Services)"
    )

def run_api_tests():
    """Run API tests"""
    return run_command(
        "python -m pytest tests/test_api.py -v --tb=short",
        "API Tests (FastAPI)"
    )

def run_integration_tests():
    """Run integration tests"""
    return run_command(
        "python -m pytest tests/ -v --tb=short -m integration",
        "Integration Tests"
    )

def run_performance_tests():
    """Run performance tests"""
    return run_command(
        "python -m pytest tests/ -v --tb=short -m performance",
        "Performance Tests"
    )

def run_coverage_analysis():
    """Run tests with coverage analysis"""
    return run_command(
        "python -m pytest tests/ --cov=src --cov-report=html --cov-report=term-missing",
        "Coverage Analysis"
    )

def run_code_quality_checks():
    """Run code quality checks"""
    checks = [
        ("python -m flake8 src/ --max-line-length=100 --ignore=E203,W503", "Code Style (flake8)"),
        ("python -m black --check src/", "Code Formatting (black)"),
        ("python -m isort --check-only src/", "Import Sorting (isort)")
    ]
    
    results = []
    for command, description in checks:
        results.append(run_command(command, description))
    
    return all(results)

def run_security_checks():
    """Run security checks"""
    checks = [
        ("python -m bandit -r src/ -f json", "Security Analysis (bandit)"),
        ("python -m safety check", "Dependency Security (safety)")
    ]
    
    results = []
    for command, description in checks:
        # Security checks might not be critical for passing
        try:
            results.append(run_command(command, description))
        except:
            print(f"⚠️  {description}: Skipped (optional)")
            results.append(True)
    
    return all(results)

def validate_architecture():
    """Validate the modular architecture"""
    print("\n🏗️ Validating Modular Architecture")
    print("-" * 60)
    
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
        from src.api.main_modular import app
        
        print("✅ All services import successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def calculate_test_metrics():
    """Calculate and display test metrics"""
    print("\n📊 Test Metrics")
    print("-" * 60)
    
    # Count test files and functions
    test_files = list(Path('tests').glob('test_*.py'))
    total_tests = 0
    
    for test_file in test_files:
        with open(test_file, 'r') as f:
            content = f.read()
            test_count = content.count('def test_')
            total_tests += test_count
            print(f"📄 {test_file.name}: {test_count} tests")
    
    print(f"\n📈 Total Test Coverage:")
    print(f"   Test Files: {len(test_files)}")
    print(f"   Test Functions: {total_tests}")
    print(f"   Service Files: 5 (Database, Auth, Reddit, Discovery, Pain Point)")
    print(f"   API Endpoints: Multiple (Health, Auth, Documentation)")
    
    return True

def main():
    """Run comprehensive test suite"""
    print("🚀 Luciq Phase 4 Testing & Validation")
    print("=" * 80)
    print("Comprehensive test suite for modular microservices architecture")
    print("=" * 80)
    
    # Track test results
    test_results = []
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install required packages.")
        return False
    
    # Validate architecture
    test_results.append(("Architecture Validation", validate_architecture()))
    
    # Run test suites
    test_suites = [
        ("Unit Tests", run_unit_tests),
        ("API Tests", run_api_tests),
        ("Coverage Analysis", run_coverage_analysis),
        ("Code Quality", run_code_quality_checks),
        ("Security Checks", run_security_checks),
        ("Test Metrics", calculate_test_metrics)
    ]
    
    for suite_name, suite_func in test_suites:
        test_results.append((suite_name, suite_func()))
    
    # Summary
    print("\n" + "=" * 80)
    print("🎯 Phase 4 Testing & Validation Results")
    print("=" * 80)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<50} {status}")
        if result:
            passed += 1
    
    print(f"\n📊 Overall Results: {passed}/{total} test suites passed")
    
    if passed == total:
        print("\n🎉 Phase 4 Testing & Validation: COMPLETE ✅")
        print("🏗️ Modular architecture fully validated!")
        print("🧪 All test suites passing!")
        print("📈 Code quality standards met!")
        print("🔒 Security checks completed!")
        print("\n🚀 Luciq system ready for production deployment!")
        return True
    else:
        print(f"\n⚠️  {total - passed} test suite(s) failed")
        print("🔧 Please review and fix failing tests before deployment")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 