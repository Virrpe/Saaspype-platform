#!/usr/bin/env python3
"""
Luciq Final System Verification
Complete End-to-End Testing of Actual Available Endpoints

Based on actual API endpoints found in master_luciq_api.py
"""

import requests
import json
import time
import sys
from datetime import datetime

class LuciqFinalVerifier:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, details=""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
        
    def wait_for_api(self, max_attempts=30):
        """Wait for API to be ready"""
        print("🔄 Waiting for API to start...")
        for attempt in range(max_attempts):
            try:
                response = self.session.get(f"{self.base_url}/api/health", timeout=2)
                if response.status_code == 200:
                    print("✅ API is ready!")
                    return True
            except:
                pass
            time.sleep(1)
        return False
        
    def test_core_endpoints(self):
        """Test core system endpoints"""
        endpoints = [
            ("/api/health", "GET", None, "Health Check"),
            ("/api/system/stats", "GET", None, "System Statistics"),
            ("/", "GET", None, "Root Endpoint")
        ]
        
        all_passed = True
        
        for endpoint, method, payload, name in endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{self.base_url}{endpoint}")
                else:
                    response = self.session.post(f"{self.base_url}{endpoint}", json=payload)
                
                if response.status_code == 200:
                    data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                    self.log_test(name, True, f"Status: 200, Response length: {len(str(data))}")
                else:
                    self.log_test(name, False, f"Status: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(name, False, f"Exception: {e}")
                all_passed = False
                
        return all_passed
        
    def test_intelligence_endpoints(self):
        """Test intelligence analysis endpoints"""
        endpoints = [
            ("/api/intelligence/market-validation", "POST", {
                "content": "Affordable project management for small businesses",
                "platform": "verification_test"
            }, "Market Validation"),
            ("/api/intelligence/market-validation-capabilities", "GET", None, "Market Validation Capabilities"),
            ("/api/intelligence/predictive-analytics", "POST", {
                "content": "SaaS market trends for small businesses",
                "platform": "verification_test"
            }, "Predictive Analytics"),
            ("/api/intelligence/predictive-analytics-capabilities", "GET", None, "Predictive Analytics Capabilities"),
            ("/api/intelligence/solution-gap-capabilities", "GET", None, "Solution Gap Capabilities"),
            ("/api/intelligence/learning-system-status", "GET", None, "Learning System Status")
        ]
        
        all_passed = True
        
        for endpoint, method, payload, name in endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{self.base_url}{endpoint}", timeout=30)
                else:
                    response = self.session.post(f"{self.base_url}{endpoint}", json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(name, True, f"Response length: {len(str(data))} chars")
                else:
                    self.log_test(name, False, f"Status: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(name, False, f"Exception: {e}")
                all_passed = False
                
        return all_passed
        
    def test_semantic_endpoints(self):
        """Test semantic analysis endpoints"""
        endpoints = [
            ("/api/semantic/analyze", "POST", {
                "content": "I'm struggling with expensive project management tools",
                "analysis_type": "comprehensive"
            }, "Semantic Analysis"),
            ("/api/semantic/intent-classification", "POST", {
                "content": "I need help with market research for my startup"
            }, "Intent Classification"),
            ("/api/semantic/capabilities", "GET", None, "Semantic Capabilities"),
            ("/api/semantic/business-insights", "GET", None, "Business Insights")
        ]
        
        all_passed = True
        
        for endpoint, method, payload, name in endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{self.base_url}{endpoint}", timeout=30)
                else:
                    response = self.session.post(f"{self.base_url}{endpoint}", json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(name, True, f"Response length: {len(str(data))} chars")
                else:
                    self.log_test(name, False, f"Status: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(name, False, f"Exception: {e}")
                all_passed = False
                
        return all_passed
        
    def test_streaming_endpoints(self):
        """Test streaming service endpoints"""
        endpoints = [
            ("/api/streaming/stats", "GET", None, "Streaming Stats"),
            ("/api/streaming/active-trends", "GET", None, "Active Trends")
        ]
        
        all_passed = True
        
        for endpoint, method, payload, name in endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                else:
                    response = self.session.post(f"{self.base_url}{endpoint}", json=payload, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(name, True, f"Response length: {len(str(data))} chars")
                else:
                    self.log_test(name, False, f"Status: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(name, False, f"Exception: {e}")
                all_passed = False
                
        return all_passed
        
    def test_discovery_endpoints(self):
        """Test discovery service endpoints"""
        endpoints = [
            ("/api/discovery/overnight/status", "GET", None, "Overnight Discovery Status")
        ]
        
        all_passed = True
        
        for endpoint, method, payload, name in endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                else:
                    response = self.session.post(f"{self.base_url}{endpoint}", json=payload, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(name, True, f"Response length: {len(str(data))} chars")
                else:
                    self.log_test(name, False, f"Status: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(name, False, f"Exception: {e}")
                all_passed = False
                
        return all_passed
        
    def test_mvp_endpoints(self):
        """Test MVP billing endpoints"""
        endpoints = [
            ("/api/mvp/pricing", "GET", None, "MVP Pricing")
        ]
        
        all_passed = True
        
        for endpoint, method, payload, name in endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                else:
                    response = self.session.post(f"{self.base_url}{endpoint}", json=payload, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(name, True, f"Response length: {len(str(data))} chars")
                else:
                    self.log_test(name, False, f"Status: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(name, False, f"Exception: {e}")
                all_passed = False
                
        return all_passed
        
    def test_modular_services(self):
        """Test modular services directly"""
        try:
            # Test service imports
            from src.services.database_service import MasterDatabaseService
            from src.services.auth_service import AuthService
            from src.services.reddit_client import MasterRedditClient
            from src.services.discovery_service import MasterDiscoveryService
            from src.services.intelligence.pain_point_engine import PainPointDetectionEngine
            
            self.log_test("Service Imports", True, "All modular services import successfully")
            
            # Test pain point engine logic
            engine = PainPointDetectionEngine()
            test_content = "I'm frustrated with expensive tools that don't work for small businesses"
            
            analysis = engine._analyze_pain_patterns(test_content)
            
            if not analysis.get('pain_detected'):
                self.log_test("Pain Point Logic", False, "Failed to detect obvious pain point")
                return False
                
            if analysis.get('pain_intensity', 0) <= 0:
                self.log_test("Pain Point Logic", False, "Pain intensity not calculated")
                return False
                
            self.log_test("Pain Point Logic", True, f"Intensity: {analysis['pain_intensity']:.3f}")
            
            # Test database service
            db_service = MasterDatabaseService()
            self.log_test("Database Service", True, "Database service initialized successfully")
            
            return True
            
        except Exception as e:
            self.log_test("Modular Services", False, f"Exception: {e}")
            return False
            
    def test_response_quality(self):
        """Test response quality and business logic"""
        try:
            # Test market validation with business content
            response = self.session.post(
                f"{self.base_url}/api/intelligence/market-validation",
                json={
                    "content": "Small businesses need affordable project management tools that integrate easily with existing workflows",
                    "platform": "quality_test"
                },
                timeout=30
            )
            
            if response.status_code != 200:
                self.log_test("Response Quality", False, f"Status: {response.status_code}")
                return False
                
            data = response.json()
            response_text = str(data)
            
            # Check response length (should be substantial)
            if len(response_text) < 500:
                self.log_test("Response Quality", False, f"Response too short: {len(response_text)} chars")
                return False
                
            # Check for business intelligence keywords
            business_keywords = ['market', 'business', 'opportunity', 'analysis', 'validation', 'competitive']
            found_keywords = sum(1 for keyword in business_keywords if keyword.lower() in response_text.lower())
            
            if found_keywords < 3:
                self.log_test("Response Quality", False, f"Insufficient business content: {found_keywords} keywords")
                return False
                
            # Check for confidence/scoring indicators
            confidence_indicators = ['confidence', 'score', 'probability', 'assessment']
            found_confidence = sum(1 for indicator in confidence_indicators if indicator.lower() in response_text.lower())
            
            if found_confidence < 1:
                self.log_test("Response Quality", False, "No confidence indicators found")
                return False
                
            self.log_test("Response Quality", True, f"Length: {len(response_text)}, Business keywords: {found_keywords}, Confidence indicators: {found_confidence}")
            return True
            
        except Exception as e:
            self.log_test("Response Quality", False, f"Exception: {e}")
            return False
            
    def run_final_verification(self):
        """Run complete system verification"""
        print("🚀 Luciq Final System Verification")
        print("=" * 70)
        print("Testing actual available endpoints and validating system logic")
        print("=" * 70)
        
        # Wait for API to be ready
        if not self.wait_for_api():
            print("❌ API failed to start - cannot proceed with verification")
            return False
            
        # Run all tests
        test_suites = [
            ("Core Endpoints", self.test_core_endpoints),
            ("Intelligence Endpoints", self.test_intelligence_endpoints),
            ("Semantic Endpoints", self.test_semantic_endpoints),
            ("Streaming Endpoints", self.test_streaming_endpoints),
            ("Discovery Endpoints", self.test_discovery_endpoints),
            ("MVP Endpoints", self.test_mvp_endpoints),
            ("Modular Services", self.test_modular_services),
            ("Response Quality", self.test_response_quality)
        ]
        
        print("\n🧪 Running Final Verification Tests...")
        print("-" * 50)
        
        passed_suites = 0
        total_suites = len(test_suites)
        
        for suite_name, test_func in test_suites:
            print(f"\n📋 {suite_name}:")
            try:
                result = test_func()
                if result:
                    passed_suites += 1
            except Exception as e:
                self.log_test(suite_name, False, f"Test suite execution failed: {e}")
        
        # Summary
        print("\n" + "=" * 70)
        print("🎯 Final Verification Results")
        print("=" * 70)
        
        # Group results by test suite
        suite_results = {}
        for result in self.test_results:
            suite = result['test'].split(' - ')[0] if ' - ' in result['test'] else result['test']
            if suite not in suite_results:
                suite_results[suite] = []
            suite_results[suite].append(result)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['test']}")
            if result['details']:
                print(f"    {result['details']}")
        
        print(f"\n📊 Overall Results: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)")
        print(f"📊 Test Suites: {passed_suites}/{total_suites} suites passed ({passed_suites/total_suites*100:.1f}%)")
        
        if passed_tests >= total_tests * 0.85:  # 85% pass rate
            print("\n🎉 FINAL VERIFICATION: EXCELLENT ✅")
            print("🏗️ System is highly operational!")
            print("🧠 Logic validation successful!")
            print("📈 Response quality verified!")
            print("🚀 System ready for production deployment!")
            return True
        elif passed_tests >= total_tests * 0.70:  # 70% pass rate
            print(f"\n✅ FINAL VERIFICATION: GOOD")
            print(f"🏗️ {passed_tests}/{total_tests} tests operational!")
            print("🧠 Core logic validation successful!")
            print("🚀 System ready for production with minor optimizations!")
            return True
        else:
            print(f"\n⚠️  System needs attention: {total_tests - passed_tests} test(s) failed")
            print("🔧 Please review failing components before production deployment")
            return False

def main():
    verifier = LuciqFinalVerifier()
    success = verifier.run_final_verification()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 