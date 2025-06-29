#!/usr/bin/env python3
"""
Detailed Chat Quality Assessment for Luciq
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def detailed_chat_quality_test():
    """Test and analyze the full quality of chat responses"""
    print("🔍 DETAILED CHAT QUALITY ASSESSMENT")
    print("=" * 70)
    
    # Login first
    login_data = {"username": "chat_tester", "password": "testpass123"}
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    access_token = response.json().get("access_token")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Test scenarios with different complexity levels
    test_scenarios = [
        {
            "name": "Simple Business Question",
            "message": "What are the main challenges in SaaS customer onboarding?",
            "expected_quality": "High - should provide specific pain points and solutions"
        },
        {
            "name": "Market Research Query", 
            "message": "I want to build a project management tool for remote teams. What's the competitive landscape like?",
            "expected_quality": "Very High - should analyze market, competitors, opportunities"
        },
        {
            "name": "Strategic Business Planning",
            "message": "How can I validate demand for an AI-powered email automation tool before building it?",
            "expected_quality": "Expert Level - should provide validation framework and actionable steps"
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}: {scenario['name']}")
        print(f"{'='*70}")
        print(f"📝 Query: {scenario['message']}")
        print(f"🎯 Expected: {scenario['expected_quality']}")
        print(f"{'─'*70}")
        
        # Send chat message
        chat_data = {"message": scenario["message"]}
        response = requests.post(f"{BASE_URL}/api/chat/message", json=chat_data, headers=headers, timeout=45)
        
        if response.status_code == 200:
            result = response.json()
            
            # Response quality metrics
            ai_response = result.get('response', '')
            confidence = result.get('confidence_score', 0)
            intent = result.get('analysis_summary', {}).get('intent', 'unknown')
            industry = result.get('analysis_summary', {}).get('industry', 'unknown')
            
            print(f"✅ RESPONSE RECEIVED")
            print(f"📊 Confidence Score: {confidence}")
            print(f"🎯 Detected Intent: {intent}")
            print(f"🏢 Industry Classification: {industry}")
            print(f"📏 Response Length: {len(ai_response)} characters")
            
            # Quality indicators
            quality_indicators = {
                "Has Credibility Framework": "CREDIBILITY ASSESSMENT" in ai_response,
                "Has Confidence Scoring": "Confidence:" in ai_response,
                "Has Source Attribution": "Sources:" in ai_response or "Analysis Method" in ai_response,
                "Has Structured Format": "**" in ai_response and "•" in ai_response,
                "Has Actionable Insights": any(word in ai_response.lower() for word in ["recommend", "should", "consider", "strategy", "next steps"]),
                "Has Business Context": any(word in ai_response.lower() for word in ["market", "competitive", "opportunity", "revenue", "customer"]),
                "Professional Tone": ai_response.startswith("**") and len(ai_response) > 500
            }
            
            print(f"\n🛡️ QUALITY INDICATORS:")
            for indicator, present in quality_indicators.items():
                status = "✅" if present else "❌"
                print(f"   {status} {indicator}")
            
            quality_score = sum(quality_indicators.values()) / len(quality_indicators) * 100
            print(f"\n📈 OVERALL QUALITY SCORE: {quality_score:.1f}%")
            
            # Show full response
            print(f"\n💬 FULL RESPONSE:")
            print("─" * 70)
            print(ai_response)
            print("─" * 70)
            
            # Assessment
            if quality_score >= 85:
                print("🌟 ASSESSMENT: EXCELLENT - Enterprise-grade response")
            elif quality_score >= 70:
                print("⭐ ASSESSMENT: GOOD - Professional quality")
            elif quality_score >= 50:
                print("📝 ASSESSMENT: ADEQUATE - Needs improvement")
            else:
                print("⚠️ ASSESSMENT: POOR - Requires significant enhancement")
                
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Error: {response.text}")
    
    print(f"\n{'='*70}")
    print("🎯 QUALITY ASSESSMENT COMPLETE")
    print("='*70")

if __name__ == "__main__":
    detailed_chat_quality_test() 