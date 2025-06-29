#!/usr/bin/env python3
"""Test the cross-platform intelligence API endpoint"""

import requests
import json

def test_intelligence_endpoint():
    print('🧠 Testing Cross-Platform Intelligence API Endpoint...')
    
    try:
        # First get auth token
        login_data = {'email': 'test@example.com', 'password': 'testpass123'}
        login_response = requests.post('http://localhost:8000/api/login', json=login_data, timeout=5)
        
        if login_response.status_code == 200:
            token = login_response.json()['access_token']
            headers = {'Authorization': f'Bearer {token}'}
            
            # Test intelligence endpoint
            intel_response = requests.get('http://localhost:8000/api/intelligence/cross-platform', headers=headers, timeout=10)
            print(f'✅ Intelligence endpoint: {intel_response.status_code}')
            
            if intel_response.status_code == 200:
                intel_data = intel_response.json()
                print(f'   Status: {intel_data.get("status", "unknown")}')
                print(f'   Message: {intel_data.get("message", "No message")}')
                
                if intel_data.get("status") == "success":
                    intelligence_data = intel_data.get("intelligence_data", {})
                    print(f'   Platform intelligence: {len(intelligence_data.get("platform_intelligence", {}))} platforms')
                    print(f'   Correlations: {len(intelligence_data.get("cross_platform_correlations", []))}')
                    print(f'   Universal trends: {len(intelligence_data.get("universal_trends", []))}')
            
            print('✅ Cross-platform intelligence endpoint working!')
            return True
        else:
            print(f'❌ Could not authenticate: {login_response.status_code}')
            return False
            
    except Exception as e:
        print(f'❌ Intelligence endpoint test failed: {e}')
        return False

if __name__ == "__main__":
    test_intelligence_endpoint() 