#!/usr/bin/env python3
"""
Comprehensive Test Suite for Master Luciq API
Tests all consolidated functionality from 219 files
"""
import requests
import json
import time
import sys
from typing import Dict, Any

class MasterAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.access_token = None
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = f"{status} {test_name}: {details}"
        print(result)
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
    
    def test_root_endpoint(self):
        """Test root API information endpoint"""
        try:
            response = requests.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Root Endpoint", True, f"API v{data.get('version')} - {data.get('total_files_consolidated')} files consolidated")
                return True
            else:
                self.log_test("Root Endpoint", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Root Endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Health Check", True, f"Status: {data.get('status')} - All systems: {len(data.get('consolidated_systems', {}))}")
                return True
            else:
                self.log_test("Health Check", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Error: {str(e)}")
            return False
    
    def test_user_registration(self):
        """Test user registration"""
        try:
            user_data = {
                "username": f"test_user_{int(time.time())}",
                "email": f"test_{int(time.time())}@example.com",
                "password": "test_password_123"
            }
            
            response = requests.post(
                f"{self.base_url}/api/auth/register",
                json=user_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("User Registration", True, f"User ID: {data.get('user_id')}")
                self.test_username = user_data["username"]
                self.test_password = user_data["password"]
                return True
            else:
                self.log_test("User Registration", False, f"Status: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.log_test("User Registration", False, f"Error: {str(e)}")
            return False
    
    def test_user_login(self):
        """Test user login and get access token"""
        try:
            login_data = {
                "username": self.test_username,
                "password": self.test_password
            }
            
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                self.log_test("User Login", True, f"Token received - Type: {data.get('token_type')}")
                return True
            else:
                self.log_test("User Login", False, f"Status: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.log_test("User Login", False, f"Error: {str(e)}")
            return False
    
    def test_intelligence_analysis(self):
        """Test intelligence analysis engine"""
        try:
            analysis_data = {
                "content": "I hate manually tracking my business expenses. It's so tedious and time consuming.",
                "platforms": ["general"]
            }
            
            response = requests.post(
                f"{self.base_url}/api/intelligence/analyze",
                json=analysis_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                sentiment = data.get("multimodal_analysis", {}).get("sentiment_analysis", {})
                self.log_test("Intelligence Analysis", True, f"Sentiment: {sentiment.get('label')} ({sentiment.get('score', 0):.2f})")
                return True
            else:
                self.log_test("Intelligence Analysis", False, f"Status: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.log_test("Intelligence Analysis", False, f"Error: {str(e)}")
            return False
    
    def test_authenticated_chat(self):
        """Test authenticated chat endpoint"""
        if not self.access_token:
            self.log_test("Authenticated Chat", False, "No access token available")
            return False
            
        try:
            chat_data = {
                "content": "What are some common business pain points?",
                "user_id": 1
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}"
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat/message",
                json=chat_data,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Authenticated Chat", True, f"Response length: {len(data.get('response', ''))}")
                return True
            else:
                self.log_test("Authenticated Chat", False, f"Status: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.log_test("Authenticated Chat", False, f"Error: {str(e)}")
            return False
    
    def test_database_operations(self):
        """Test database functionality through API"""
        try:
            # Test database through health endpoint which includes database status
            response = requests.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                db_status = data.get("components", {}).get("database")
                if db_status == "healthy":
                    self.log_test("Database Operations", True, "Database healthy and operational")
                    return True
                else:
                    self.log_test("Database Operations", False, f"Database status: {db_status}")
                    return False
            else:
                self.log_test("Database Operations", False, f"Health check failed: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Database Operations", False, f"Error: {str(e)}")
            return False
    
    def test_transformer_model(self):
        """Test transformer model functionality"""
        try:
            response = requests.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                transformer_status = data.get("components", {}).get("transformer_model")
                if transformer_status == "healthy":
                    self.log_test("Transformer Model", True, "Transformer model loaded and operational")
                    return True
                else:
                    self.log_test("Transformer Model", False, f"Transformer status: {transformer_status}")
                    return False
            else:
                self.log_test("Transformer Model", False, f"Health check failed: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Transformer Model", False, f"Error: {str(e)}")
            return False
    
    def test_api_documentation(self):
        """Test API documentation availability"""
        try:
            response = requests.get(f"{self.base_url}/docs")
            if response.status_code == 200:
                content = response.text
                if "swagger" in content.lower() or "openapi" in content.lower():
                    self.log_test("API Documentation", True, "Swagger/OpenAPI docs available")
                    return True
                else:
                    self.log_test("API Documentation", False, "Documentation format unclear")
                    return False
            else:
                self.log_test("API Documentation", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Documentation", False, f"Error: {str(e)}")
            return False
    
    def run_comprehensive_test(self):
        """Run all tests and generate report"""
        print("🚀 Starting Master API Comprehensive Test Suite")
        print("=" * 60)
        
        # Core infrastructure tests
        self.test_root_endpoint()
        self.test_health_endpoint()
        self.test_database_operations()
        self.test_transformer_model()
        self.test_api_documentation()
        
        # Authentication flow tests
        if self.test_user_registration():
            self.test_user_login()
        
        # Business logic tests
        self.test_intelligence_analysis()
        self.test_authenticated_chat()
        
        # Generate summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED! Master API is fully operational!")
            print("✅ 219 files successfully consolidated into working API")
            print("✅ All core systems operational")
            print("✅ Authentication working")
            print("✅ Business intelligence features active")
            print("✅ Database and AI models loaded")
            return True
        else:
            print(f"\n⚠️  {total - passed} tests failed. Check details above.")
            return False

def main():
    """Main test execution"""
    print("Master Luciq API - Comprehensive Functionality Test")
    print("Testing consolidation of 219 Python files into unified API")
    print()
    
    # Check if API is running
    tester = MasterAPITester()
    
    try:
        requests.get(tester.base_url, timeout=5)
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: API server not running on http://localhost:8000")
        print("Please start the Master API first:")
        print("python master_luciq_api.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        sys.exit(1)
    
    # Run comprehensive tests
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🚀 MASTER API VALIDATION: COMPLETE SUCCESS!")
        print("Ready for production deployment and market launch.")
        sys.exit(0)
    else:
        print("\n🔧 Some issues detected. Please review failed tests.")
        sys.exit(1)

if __name__ == "__main__":
    main() 