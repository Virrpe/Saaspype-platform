#!/usr/bin/env python3
"""
Show Full Intelligent Response
Demonstrates the complete transformation from pre-generated to intelligent
"""

import requests
import json

def show_full_response():
    print("🚀 LUCIQ INTELLIGENCE SHOWCASE")
    print("=" * 70)
    
    query = "I'm thinking about starting an AI-powered meal planning app for busy professionals. What are the key pain points and market opportunities I should focus on?"
    
    print(f"USER QUERY: {query}")
    print()
    print("🧠 LUCIQ'S INTELLIGENT RESPONSE:")
    print("=" * 70)
    
    try:
        response = requests.post(
            "http://localhost:8000/api/chat/demo/message",
            json={"message": query},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data.get('response', '') or data.get('ai_response', '')
            
            print(ai_response)
            print()
            print("=" * 70)
            print(f"📊 RESPONSE ANALYSIS:")
            print(f"   • Length: {len(ai_response)} characters")
            print(f"   • Confidence: {data.get('confidence_score', 0):.2f}")
            print(f"   • Demo Mode: {data.get('demo_mode', False)}")
            print(f"   • Context: {data.get('conversation_context', {}).get('intent', 'unknown')}")
            
            # Show intelligence indicators
            intelligence_indicators = ["analysis", "data", "market", "competitive", "strategic", "insights", "trends", "research", "intelligence"]
            found_indicators = [word for word in intelligence_indicators if word.lower() in ai_response.lower()]
            
            print(f"   • Intelligence Indicators Found: {len(found_indicators)}")
            print(f"   • Indicators: {', '.join(found_indicators)}")
            
            if len(found_indicators) >= 3:
                print("   ✅ FEELS GENUINELY INTELLIGENT!")
            else:
                print("   ⚠️ Still improving...")
                
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    show_full_response() 