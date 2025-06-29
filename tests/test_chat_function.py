#!/usr/bin/env python3
"""
Test script for Luciq Chat Function with Credibility Framework
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_chat_function():
    """Test the AI-powered chat function"""
    print("🤖 Testing Luciq Chat Function with Credibility Framework")
    print("=" * 60)
    
    # Wait for API to start
    print("\n⏳ Waiting for API to start...")
    time.sleep(8)
    
    # Step 1: Health check
    print("\n1. 🔍 Checking API health...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        if response.status_code == 200:
            print("✅ API is healthy and running")
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to API: {e}")
        return False
    
    # Step 2: Register a test user
    print("\n2. 👤 Creating test user...")
    user_data = {
        "username": "chat_tester",
        "email": "test@luciq.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data, timeout=10)
        if response.status_code in [200, 201]:
            print("✅ Test user created successfully")
        elif response.status_code == 400 and "already exists" in response.text:
            print("✅ Test user already exists")
        else:
            print(f"⚠️ User creation issue: {response.status_code}")
    except Exception as e:
        print(f"⚠️ User creation error: {e}")
    
    # Step 3: Login to get token
    print("\n3. 🔐 Logging in...")
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data, timeout=10)
        if response.status_code == 200:
            auth_data = response.json()
            access_token = auth_data.get("access_token")
            print("✅ Login successful")
            print(f"   Token: {access_token[:20]}...")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Step 4: Test chat function
    print("\n4. 💬 Testing Chat Function...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Test messages to try
    test_messages = [
        "What are the main pain points in SaaS onboarding?",
        "I'm looking to start a productivity app. What should I know about the market?",
        "Tell me about opportunities in the AI automation space"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n   Test {i}: {message}")
        
        chat_data = {"message": message}
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/chat/message", 
                json=chat_data, 
                headers=headers, 
                timeout=30
            )
            
            if response.status_code == 200:
                chat_response = response.json()
                print("✅ Chat response received")
                print(f"   📊 Confidence Score: {chat_response.get('confidence_score', 'N/A')}")
                print(f"   🎯 Intent: {chat_response.get('analysis_summary', {}).get('intent', 'N/A')}")
                print(f"   🏢 Industry: {chat_response.get('analysis_summary', {}).get('industry', 'N/A')}")
                
                # Show first part of response
                ai_response = chat_response.get('response', '')
                if ai_response:
                    print(f"   💬 Response Preview: {ai_response[:200]}...")
                    # Check for credibility framework indicators
                    if "CREDIBILITY ASSESSMENT" in ai_response:
                        print("   🛡️ ✅ Credibility Framework Active!")
                    if "Confidence:" in ai_response:
                        print("   📊 ✅ Confidence Scoring Active!")
                    if "Sources:" in ai_response:
                        print("   📚 ✅ Source Attribution Active!")
                else:
                    print("   ⚠️ No response content received")
                    
            else:
                print(f"   ❌ Chat failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Chat error: {e}")
    
    print(f"\n🎉 Chat Function Test Complete!")
    return True

if __name__ == "__main__":
    test_chat_function() 