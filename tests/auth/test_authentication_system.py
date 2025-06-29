#!/usr/bin/env python3
"""
Authentication System Test
Comprehensive testing of the new authentication infrastructure
"""
import sys
import requests
import json
import time
from datetime import datetime

# Test configuration
API_BASE_URL = "http://localhost:8000"
TEST_USER_EMAIL = "test@gmail.com"
TEST_USER_PASSWORD = "SecureP@ss2024!"
TEST_USER_DATA = {
    "email": TEST_USER_EMAIL,
    "password": TEST_USER_PASSWORD,
    "first_name": "Test",
    "last_name": "User",
    "username": "testuser"
}

class AuthenticationTester:
    """Authentication system testing suite"""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = requests.Session()
        self.access_token = None
        self.refresh_token = None
        self.test_results = {}
    
    def test_api_health(self) -> bool:
        """Test if API is running and accessible"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                print("✅ API Health Check: PASSED")
                return True
            else:
                print(f"❌ API Health Check: FAILED (Status: {response.status_code})")
                return False
        except Exception as e:
            print(f"❌ API Health Check: FAILED (Error: {e})")
            return False
    
    def test_user_registration(self) -> bool:
        """Test user registration functionality"""
        try:
            response = self.session.post(
                f"{self.base_url}/auth/register",
                json=TEST_USER_DATA
            )
            
            if response.status_code == 201:
                data = response.json()
                if data.get("success") and data.get("user"):
                    print("✅ User Registration: PASSED")
                    print(f"   User ID: {data['user']['user_id']}")
                    print(f"   Email: {data['user']['email']}")
                    return True
            elif response.status_code == 409:
                print("⚠️  User Registration: USER_ALREADY_EXISTS (Expected for repeat tests)")
                return True
            else:
                print(f"❌ User Registration: FAILED (Status: {response.status_code})")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ User Registration: FAILED (Error: {e})")
            return False
    
    def test_user_login(self) -> bool:
        """Test user login functionality"""
        try:
            # First, verify the user's email (simulate email verification)
            # In a real system, this would come from an email
            self.simulate_email_verification()
            
            response = self.session.post(
                f"{self.base_url}/auth/login",
                json={
                    "email": TEST_USER_EMAIL,
                    "password": TEST_USER_PASSWORD
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("access_token"):
                    self.access_token = data["access_token"]
                    self.refresh_token = data["refresh_token"]
                    print("✅ User Login: PASSED")
                    print(f"   Token Type: {data.get('token_type', 'Bearer')}")
                    print(f"   Expires At: {data.get('expires_at')}")
                    return True
            elif response.status_code == 403:
                print("⚠️  User Login: EMAIL_NOT_VERIFIED (Expected for new users)")
                # Try to verify email and login again
                if self.simulate_email_verification():
                    return self.test_user_login()
                return False
            else:
                print(f"❌ User Login: FAILED (Status: {response.status_code})")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ User Login: FAILED (Error: {e})")
            return False
    
    def simulate_email_verification(self) -> bool:
        """Simulate email verification process"""
        try:
            # In a real system, we'd get this token from the registration response
            # For testing, we'll use the auth service directly
            from src.api.services.auth_service import auth_service
            
            # Get the user from database to get verification token
            result = auth_service.verify_email(TEST_USER_EMAIL, "dummy_token")
            
            # If user is already verified, that's fine
            if result.get("success") or "already verified" in result.get("message", "").lower():
                print("✅ Email Verification: PASSED (or already verified)")
                return True
            
            # Try to verify by directly setting verification status
            # This is a test shortcut - in production, use real verification tokens
            try:
                from src.shared.database.connection import db_service
                
                conn = db_service.get_connection()
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE users 
                    SET is_verified = 1, verification_token = NULL, verification_sent_at = NULL
                    WHERE email = ?
                """, (TEST_USER_EMAIL.lower(),))
                
                conn.commit()
                conn.close()
                
                print("✅ Email Verification: SIMULATED SUCCESSFULLY")
                return True
                
            except Exception as e:
                print(f"❌ Email Verification: DATABASE UPDATE FAILED ({e})")
                return False
                
        except Exception as e:
            print(f"❌ Email Verification: FAILED (Error: {e})")
            return False
    
    def test_protected_endpoint(self) -> bool:
        """Test accessing a protected endpoint with token"""
        if not self.access_token:
            print("❌ Protected Endpoint Test: NO ACCESS TOKEN")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = self.session.get(f"{self.base_url}/auth/me", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("email") == TEST_USER_EMAIL:
                    print("✅ Protected Endpoint Access: PASSED")
                    print(f"   User Email: {data.get('email')}")
                    print(f"   User ID: {data.get('user_id')}")
                    return True
            else:
                print(f"❌ Protected Endpoint Access: FAILED (Status: {response.status_code})")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Protected Endpoint Access: FAILED (Error: {e})")
            return False
    
    def test_token_refresh(self) -> bool:
        """Test token refresh functionality"""
        if not self.refresh_token:
            print("❌ Token Refresh Test: NO REFRESH TOKEN")
            return False
        
        try:
            response = self.session.post(
                f"{self.base_url}/auth/refresh-token",
                json={"refresh_token": self.refresh_token}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("access_token"):
                    old_token = self.access_token
                    self.access_token = data["access_token"]
                    self.refresh_token = data["refresh_token"]
                    print("✅ Token Refresh: PASSED")
                    print(f"   New token generated successfully")
                    return True
            else:
                print(f"❌ Token Refresh: FAILED (Status: {response.status_code})")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Token Refresh: FAILED (Error: {e})")
            return False
    
    def test_token_validation(self) -> bool:
        """Test token validation endpoint"""
        if not self.access_token:
            print("❌ Token Validation Test: NO ACCESS TOKEN")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = self.session.get(f"{self.base_url}/auth/validate-token", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("valid") and data.get("user_id"):
                    print("✅ Token Validation: PASSED")
                    print(f"   Token is valid for user: {data.get('email')}")
                    return True
            else:
                print(f"❌ Token Validation: FAILED (Status: {response.status_code})")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Token Validation: FAILED (Error: {e})")
            return False
    
    def test_logout(self) -> bool:
        """Test user logout functionality"""
        if not self.refresh_token:
            print("❌ Logout Test: NO REFRESH TOKEN")
            return False
        
        try:
            response = self.session.post(
                f"{self.base_url}/auth/logout",
                json={"refresh_token": self.refresh_token}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print("✅ User Logout: PASSED")
                    print(f"   Message: {data.get('message')}")
                    return True
            else:
                print(f"❌ User Logout: FAILED (Status: {response.status_code})")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ User Logout: FAILED (Error: {e})")
            return False
    
    def test_invalid_token_access(self) -> bool:
        """Test that invalid tokens are rejected"""
        try:
            headers = {"Authorization": "Bearer invalid_token_123"}
            response = self.session.get(f"{self.base_url}/auth/me", headers=headers)
            
            if response.status_code == 401:
                print("✅ Invalid Token Rejection: PASSED")
                print("   Invalid tokens properly rejected")
                return True
            else:
                print(f"❌ Invalid Token Rejection: FAILED (Status: {response.status_code})")
                print("   Invalid tokens should be rejected with 401")
                return False
                
        except Exception as e:
            print(f"❌ Invalid Token Rejection: FAILED (Error: {e})")
            return False
    
    def run_full_test_suite(self) -> bool:
        """Run the complete authentication test suite"""
        print("🚀 STARTING AUTHENTICATION SYSTEM TEST SUITE")
        print("=" * 60)
        print(f"Testing API at: {self.base_url}")
        print(f"Test User: {TEST_USER_EMAIL}")
        print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        tests = [
            ("API Health Check", self.test_api_health),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("Protected Endpoint Access", self.test_protected_endpoint),
            ("Token Refresh", self.test_token_refresh),
            ("Token Validation", self.test_token_validation),
            ("Invalid Token Rejection", self.test_invalid_token_access),
            ("User Logout", self.test_logout),
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🧪 Testing: {test_name}")
            try:
                if test_func():
                    passed_tests += 1
                    self.test_results[test_name] = "PASSED"
                else:
                    self.test_results[test_name] = "FAILED"
            except Exception as e:
                print(f"❌ {test_name}: CRASHED (Error: {e})")
                self.test_results[test_name] = "CRASHED"
            
            time.sleep(0.5)  # Small delay between tests
        
        print("\n" + "=" * 60)
        print("🏁 AUTHENTICATION TEST SUITE COMPLETE")
        print("=" * 60)
        print(f"Tests Passed: {passed_tests}/{total_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print("\n📊 DETAILED RESULTS:")
        for test_name, result in self.test_results.items():
            status_emoji = "✅" if result == "PASSED" else "❌"
            print(f"   {status_emoji} {test_name}: {result}")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! Authentication system is ready for production.")
            return True
        else:
            print(f"\n⚠️  {total_tests - passed_tests} tests failed. Please review and fix issues before production.")
            return False

def main():
    """Main test execution"""
    print("Luciq Authentication System Test")
    print("This test will verify the complete authentication infrastructure")
    print()
    
    # Check if API is accessible
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ API is not accessible at {API_BASE_URL}")
            print("   Please ensure the API server is running:")
            print("   python -c \"import uvicorn; uvicorn.run('src.api.main:app', host='localhost', port=8000)\"")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API at {API_BASE_URL}")
        print(f"   Error: {e}")
        print("   Please ensure the API server is running on port 8000")
        sys.exit(1)
    
    # Run tests
    tester = AuthenticationTester()
    success = tester.run_full_test_suite()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 