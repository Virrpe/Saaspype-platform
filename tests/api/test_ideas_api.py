#!/usr/bin/env python3
import requests
import json

def test_generate_ideas():
    url = "http://localhost:8000/api/orchestration/generate-ideas"
    payload = {
        "request_type": "business_idea_generation",
        "data": {
            "content": "SaaS ideas for small businesses",
            "focus": "saas_solutions",
            "target_market": "SMB",
            "analysis_depth": "comprehensive"
        }
    }
    
    try:
        print("🚀 Testing business idea generation...")
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"Business Ideas Generated: {len(result.get('business_ideas', []))}")
            
            # Show first idea as example
            if result.get('business_ideas'):
                first_idea = result['business_ideas'][0]
                print(f"\nExample Idea: {first_idea.get('idea_title', 'N/A')}")
                print(f"Problem: {first_idea.get('problem_statement', 'N/A')[:100]}...")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_generate_ideas() 