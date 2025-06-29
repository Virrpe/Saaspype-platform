#!/usr/bin/env python3
"""
Debug Chat Credibility Integration
==================================
"""

import requests
import json

def test_chat_credibility():
    """Debug chat credibility integration"""
    
    # Login first
    print("🔐 Logging in...")
    login_data = {
        "username": "credibility_test_user",
        "password": "testpass123"
    }
    
    try:
        response = requests.post('http://localhost:8000/api/auth/login', json=login_data)
        if response.status_code != 200:
            print(f"❌ Login failed: {response.status_code}")
            return
        
        token = response.json().get('access_token')
        print(f"✅ Login successful")
        
        # Test chat message
        print("\n💬 Testing chat message...")
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        chat_data = {"message": "I need help with customer retention in my SaaS"}
        
        response = requests.post('http://localhost:8000/api/chat/message', 
                               json=chat_data, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat response received")
            print(f"📝 Response keys: {list(data.keys())}")
            
            chat_response = data.get('response', '')
            print(f"\n📋 Response preview (first 300 chars):")
            print(chat_response[:300])
            print("...")
            
            # Check for credibility indicators
            credibility_indicators = [
                'CREDIBILITY ASSESSMENT',
                'Confidence',
                'Sources:',
                'Methodology:',
                'Validation Status:'
            ]
            
            found_indicators = []
            for indicator in credibility_indicators:
                if indicator in chat_response:
                    found_indicators.append(indicator)
            
            print(f"\n🔍 Credibility indicators found: {len(found_indicators)}/{len(credibility_indicators)}")
            for indicator in found_indicators:
                print(f"   ✅ {indicator}")
            
            missing_indicators = [i for i in credibility_indicators if i not in found_indicators]
            for indicator in missing_indicators:
                print(f"   ❌ {indicator}")
                
            print(f"\n📊 Full response structure:")
            for key, value in data.items():
                if key == 'response':
                    print(f"   {key}: {len(str(value))} characters")
                else:
                    print(f"   {key}: {value}")
        
        else:
            print(f"❌ Chat failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_chat_credibility() 