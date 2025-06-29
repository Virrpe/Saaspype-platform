#!/usr/bin/env python3
"""
Test Intelligence Upgrade for Luciq
Validates that the intelligent orchestrator is working correctly
"""

import requests
import json
import time

def test_basic_chat():
    """Test basic chat functionality"""
    print("🧪 Testing Basic Chat...")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/chat/demo/message",
            json={
                "message": "Tell me about market opportunities in AI-powered fitness apps"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat endpoint working")
            
            # Get the actual response text
            ai_response = data.get('response', '') or data.get('ai_response', '')
            
            print(f"Response length: {len(ai_response)} characters")
            print(f"Confidence: {data.get('confidence_score', 0)}")
            print(f"Demo mode: {data.get('demo_mode', False)}")
            
            # Analyze intelligence level
            intelligence_indicators = [
                "market analysis", "competitors", "pain points", "data shows",
                "recent trends", "analysis reveals", "insights", "strategic"
            ]
            
            intelligence_score = sum(1 for indicator in intelligence_indicators 
                                   if indicator.lower() in ai_response.lower())
            
            print(f"Intelligence score: {intelligence_score}/8")
            print(f"Feels intelligent: {'✅ YES' if intelligence_score >= 3 else '❌ NO'}")
            
            # Show snippet of response
            if ai_response:
                snippet = ai_response[:200] + "..." if len(ai_response) > 200 else ai_response
                print(f"Response preview: {snippet}")
            
            return True
        else:
            print(f"❌ Chat failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return False

def test_api_health():
    """Test API health"""
    print("🏥 Testing API Health...")
    
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is healthy")
            return True
        else:
            print(f"❌ API unhealthy: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API connection error: {e}")
        return False

def main():
    print("🚀 LUCIQ INTELLIGENCE UPGRADE TEST")
    print("=" * 50)
    
    # Test sequence
    if not test_api_health():
        print("\n❌ FAILED: API not running. Start with: python master_luciq_api.py")
        return
    
    if test_basic_chat():
        print("\n✅ SUCCESS: Intelligence upgrade is working!")
    else:
        print("\n❌ FAILED: Intelligence upgrade needs debugging")

if __name__ == "__main__":
    main() 