#!/usr/bin/env python3
"""
Comprehensive Master API Testing Script
Tests all major functionality and shows real data examples
"""

import requests
import json
import time
import sys
from datetime import datetime

# API Configuration
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "username": "test_user_demo",
    "email": "demo@luciq.com", 
    "password": "TestPassword123!"
}

class MasterAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.test_results = []
        
    def log_test(self, test_name, success, data=None, error=None):
        """Log test results with real data examples"""
        result = {
            "test": test_name,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "error": str(error) if error else None
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"\n{status} {test_name}")
        if success and data:
            print(f"📊 Result Preview: {str(data)[:200]}...")
        if error:
            print(f"🚨 Error: {error}")
    
    def test_api_health(self):
        """Test API health endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/api/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("API Health Check", True, data)
                return True
            else:
                self.log_test("API Health Check", False, error=f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Health Check", False, error=e)
            return False
    
    def test_authentication(self):
        """Test user registration and authentication"""
        try:
            # Register user
            reg_response = self.session.post(
                f"{BASE_URL}/api/auth/register",
                json=TEST_USER,
                timeout=10
            )
            
            if reg_response.status_code in [200, 201, 409]:  # 409 = user exists
                # Login user
                login_response = self.session.post(
                    f"{BASE_URL}/api/auth/login",
                    data={
                        "username": TEST_USER["username"],
                        "password": TEST_USER["password"]
                    },
                    timeout=10
                )
                
                if login_response.status_code == 200:
                    auth_data = login_response.json()
                    self.auth_token = auth_data.get("access_token")
                    self.session.headers.update({
                        "Authorization": f"Bearer {self.auth_token}"
                    })
                    self.log_test("Authentication System", True, {
                        "user_id": auth_data.get("user_id"),
                        "token_type": auth_data.get("token_type"),
                        "has_token": bool(self.auth_token)
                    })
                    return True
                else:
                    self.log_test("Authentication System", False, error=f"Login failed: {login_response.status_code}")
                    return False
            else:
                self.log_test("Authentication System", False, error=f"Registration failed: {reg_response.status_code}")
                return False
        except Exception as e:
            self.log_test("Authentication System", False, error=e)
            return False
    
    def test_discovery_service(self):
        """Test discovery service with real Reddit data"""
        try:
            discovery_data = {
                "query": "startup business ideas",
                "subreddit": "entrepreneur",
                "limit": 5
            }
            
            response = self.session.post(
                f"{BASE_URL}/api/discovery/analyze",
                json=discovery_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Discovery Service - Reddit Analysis", True, {
                    "posts_analyzed": len(data.get("posts", [])),
                    "business_opportunities": len(data.get("opportunities", [])),
                    "sample_opportunity": data.get("opportunities", [{}])[0] if data.get("opportunities") else None,
                    "pain_points_detected": len(data.get("pain_points", [])),
                    "engagement_metrics": data.get("engagement_summary", {})
                })
                return True
            else:
                self.log_test("Discovery Service - Reddit Analysis", False, error=f"Status: {response.status_code}, Response: {response.text[:200]}")
                return False
        except Exception as e:
            self.log_test("Discovery Service - Reddit Analysis", False, error=e)
            return False
    
    def test_intelligence_engine(self):
        """Test intelligence engine with text analysis"""
        try:
            analysis_data = {
                "text": "Our startup is struggling with customer acquisition costs. We need a better way to reach potential customers without spending too much on advertising. The current market is very competitive.",
                "analysis_type": "comprehensive"
            }
            
            response = self.session.post(
                f"{BASE_URL}/api/intelligence/analyze",
                json=analysis_data,
                timeout=20
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Intelligence Engine - Text Analysis", True, {
                    "sentiment_score": data.get("sentiment", {}).get("compound"),
                    "key_entities": data.get("entities", [])[:3],
                    "business_keywords": data.get("business_keywords", [])[:5],
                    "pain_points": data.get("pain_points", []),
                    "opportunities": data.get("opportunities", []),
                    "analysis_confidence": data.get("confidence_score")
                })
                return True
            else:
                self.log_test("Intelligence Engine - Text Analysis", False, error=f"Status: {response.status_code}, Response: {response.text[:200]}")
                return False
        except Exception as e:
            self.log_test("Intelligence Engine - Text Analysis", False, error=e)
            return False
    
    def test_mega_scraper(self):
        """Test mega scraper functionality"""
        try:
            scraper_data = {
                "keywords": ["business automation", "saas tools"],
                "platforms": ["reddit", "hackernews"],
                "limit": 3
            }
            
            response = self.session.post(
                f"{BASE_URL}/api/scraper/mega-scan",
                json=scraper_data,
                timeout=25
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Mega Scraper - Multi-Platform", True, {
                    "platforms_scanned": len(data.get("platforms", [])),
                    "total_results": data.get("total_results", 0),
                    "sample_result": data.get("results", [{}])[0] if data.get("results") else None,
                    "correlation_insights": data.get("correlations", [])[:2],
                    "scan_duration": data.get("scan_duration")
                })
                return True
            else:
                self.log_test("Mega Scraper - Multi-Platform", False, error=f"Status: {response.status_code}, Response: {response.text[:200]}")
                return False
        except Exception as e:
            self.log_test("Mega Scraper - Multi-Platform", False, error=e)
            return False
    
    def test_chat_service(self):
        """Test AI chat service"""
        try:
            chat_data = {
                "message": "What are the current trends in the SaaS market? Give me insights about business opportunities."
            }
            
            response = self.session.post(
                f"{BASE_URL}/api/chat/message",
                json=chat_data,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Chat Service - AI Assistant", True, {
                    "response_length": len(data.get("response", "")),
                    "response_preview": data.get("response", "")[:150],
                    "confidence": data.get("confidence"),
                    "processing_time": data.get("processing_time"),
                    "context_awareness": bool(data.get("context"))
                })
                return True
            else:
                self.log_test("Chat Service - AI Assistant", False, error=f"Status: {response.status_code}, Response: {response.text[:200]}")
                return False
        except Exception as e:
            self.log_test("Chat Service - AI Assistant", False, error=e)
            return False
    
    def test_system_capabilities(self):
        """Test system stats and capabilities"""
        try:
            response = self.session.get(f"{BASE_URL}/api/system/stats", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("System Capabilities", True, {
                    "total_endpoints": data.get("total_endpoints"),
                    "active_services": data.get("active_services", []),
                    "system_uptime": data.get("uptime"),
                    "memory_usage": data.get("memory_usage"),
                    "performance_metrics": data.get("performance", {})
                })
                return True
            else:
                self.log_test("System Capabilities", False, error=f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("System Capabilities", False, error=e)
            return False
    
    def run_comprehensive_test(self):
        """Run all tests and show results"""
        print("🚀 Starting Comprehensive Master API Testing...")
        print("=" * 60)
        
        test_methods = [
            self.test_api_health,
            self.test_authentication,
            self.test_discovery_service,
            self.test_intelligence_engine,
            self.test_mega_scraper,
            self.test_chat_service,
            self.test_system_capabilities
        ]
        
        passed = 0
        total = len(test_methods)
        
        for test_method in test_methods:
            if test_method():
                passed += 1
            time.sleep(1)  # Brief pause between tests
        
        print("\n" + "=" * 60)
        print(f"📊 TEST SUMMARY: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED - Master API is fully operational!")
        elif passed > total * 0.7:
            print("✅ MOSTLY OPERATIONAL - Core functionality working")
        else:
            print("⚠️  PARTIAL FUNCTIONALITY - Some services need attention")
        
        return self.test_results

def main():
    """Main testing function"""
    print("🔬 Luciq Master API Comprehensive Testing")
    print(f"🎯 Testing API at: {BASE_URL}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = MasterAPITester()
    results = tester.run_comprehensive_test()
    
    # Save detailed results
    with open("master_api_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📁 Detailed results saved to: master_api_test_results.json")
    return results

if __name__ == "__main__":
    main() 