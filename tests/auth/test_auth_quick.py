#!/usr/bin/env python3
"""
Quick Authentication Test - Verify signup/login endpoints work
"""

import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8000"

def test_auth_endpoints():
    print("🔐 Testing Luciq Authentication System...")
    print("=" * 50)
    
    # Test data
    test_user = {
        "email": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@gmail.com",
        "password": "TestPass123!",
        "first_name": "Test",
        "last_name": "User",
        "username": f"testuser_{datetime.now().strftime('%H%M%S')}"
    }
    
    try:
        # Test Health
        print("1. Testing API Health...")
        health_response = requests.get(f"{API_BASE}/health")
        print(f"   Health Status: {health_response.status_code}")
        
        # Test Signup/Register
        print("\n2. Testing User Registration...")
        signup_response = requests.post(
            f"{API_BASE}/auth/register",
            headers={"Content-Type": "application/json"},
            json=test_user
        )
        
        if signup_response.status_code == 200:
            signup_data = signup_response.json()
            print(f"   ✅ Registration successful!")
            print(f"   User ID: {signup_data.get('user', {}).get('user_id')}")
            print(f"   Email: {signup_data.get('user', {}).get('email')}")
            print(f"   Success: {signup_data.get('success')}")
            
            # Auto-verify the user for testing (development only)
            print(f"\n💡 Auto-verifying user for testing...")
            try:
                from src.shared.database.connection import db_service
                conn = db_service.get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET is_verified = 1, verification_token = NULL, verification_sent_at = NULL
                    WHERE email = ?
                """, (test_user["email"],))
                conn.commit()
                conn.close()
                print(f"   ✅ User auto-verified for testing")
                
                # Now test login
                print("\n3. Testing Login...")
                login_response = requests.post(
                    f"{API_BASE}/auth/login",
                    headers={"Content-Type": "application/json"},
                    json={
                        "email": test_user["email"],
                        "password": test_user["password"]
                    }
                )
                
                if login_response.status_code == 200:
                    login_data = login_response.json()
                    print(f"   ✅ Login successful!")
                    print(f"   Access token received: {'access_token' in login_data}")
                    
                    # Test Profile Access
                    if 'access_token' in login_data:
                        print("\n4. Testing Profile Access...")
                        token = login_data.get('access_token')
                        profile_response = requests.get(
                            f"{API_BASE}/api/me",
                            headers={"Authorization": f"Bearer {token}"}
                        )
                        
                        if profile_response.status_code == 200:
                            profile_data = profile_response.json()
                            print(f"   ✅ Profile access successful!")
                            print(f"   Profile: {profile_data.get('email')}")
                        else:
                            print(f"   ❌ Profile access failed: {profile_response.status_code}")
                            print(f"   Error: {profile_response.text}")
                else:
                    print(f"   ❌ Login failed: {login_response.status_code}")
                    print(f"   Error: {login_response.text}")
                    
            except Exception as e:
                print(f"   ❌ Auto-verification failed: {e}")
                print(f"   Note: Email verification may be required before login")
            
        else:
            print(f"   ❌ Registration failed: {signup_response.status_code}")
            print(f"   Error: {signup_response.text}")
            
            # Try to test login anyway with the credentials
            print("\n3. Testing Login (in case user already exists)...")
            login_response = requests.post(
                f"{API_BASE}/auth/login",
                headers={"Content-Type": "application/json"},
                json={
                    "email": test_user["email"],
                    "password": test_user["password"]
                }
            )
            
            if login_response.status_code == 200:
                login_data = login_response.json()
                print(f"   ✅ Login successful!")
                print(f"   Access token received: {'access_token' in login_data}")
                
                # Test Profile Access
                if 'access_token' in login_data:
                    print("\n4. Testing Profile Access...")
                    token = login_data.get('access_token')
                    profile_response = requests.get(
                        f"{API_BASE}/api/me",
                        headers={"Authorization": f"Bearer {token}"}
                    )
                    
                    if profile_response.status_code == 200:
                        profile_data = profile_response.json()
                        print(f"   ✅ Profile access successful!")
                        print(f"   Profile: {profile_data.get('email')}")
                    else:
                        print(f"   ❌ Profile access failed: {profile_response.status_code}")
                        print(f"   Error: {profile_response.text}")
            else:
                print(f"   ❌ Login failed: {login_response.status_code}")
                print(f"   Error: {login_response.text}")
                
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Authentication test complete!")
    print("\n💡 Correct endpoint usage:")
    print("   Registration: POST /auth/register")
    print("   Login: POST /auth/login") 
    print("   Profile: GET /api/me (with Bearer token)")
    print("\n💡 Frontend should use these endpoints:")
    print(f"   Email: {test_user['email']}")
    print(f"   Password: {test_user['password']}")

if __name__ == "__main__":
    test_auth_endpoints() 