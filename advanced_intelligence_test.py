#!/usr/bin/env python3
"""
Advanced Intelligence Test for Luciq
"""

import requests
import json
import time

def test_intelligence():
    print("🧠 LUCIQ INTELLIGENCE TEST")
    print("=" * 50)
    
    scenarios = [
        "Tell me about market opportunities in AI-powered fitness apps for busy professionals",
        "How can I differentiate my SaaS product in the project management space?",
        "What's the best tech stack for a real-time analytics dashboard startup?"
    ]
    
    for i, query in enumerate(scenarios, 1):
        print(f"\n🎯 TEST {i}: {query[:50]}...")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/chat/demo/message",
                json={"message": query},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('response', '') or data.get('ai_response', '')
                
                # Analyze intelligence
                intelligence_words = ["analysis", "data", "market", "competitive", "strategic", "insights", "trends"]
                intelligence_score = sum(1 for word in intelligence_words if word.lower() in ai_response.lower())
                
                print(f"✅ Response Length: {len(ai_response)} chars")
                print(f"🧠 Intelligence Score: {intelligence_score}/7")
                print(f"💭 Snippet: {ai_response[:150]}...")
                print(f"🎯 Feels Intelligent: {'YES' if intelligence_score >= 3 else 'NO'}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    test_intelligence() 