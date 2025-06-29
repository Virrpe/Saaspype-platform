#!/usr/bin/env python3
"""
Simple API Test - Test the demo endpoint
"""

import requests
import json

def test_api():
    print("🧪 Testing Luciq API Demo Endpoint")
    print("=" * 50)
    
    # Test demo endpoint
    try:
        print("\n1. Testing demo chat endpoint...")
        response = requests.post(
            'http://127.0.0.1:8002/api/chat/demo/message',
            json={'message': 'generate ideas about fintech'},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API is working!")
            print(f"Response: {data.get('response', 'No response')[:100]}...")
            print(f"Intent: {data.get('intent', 'Unknown')}")
            print(f"Actions: {len(data.get('actions', []))}")
            
            # Check if ideas were generated
            actions = data.get('actions', [])
            for action in actions:
                if action.get('type') == 'save_idea':
                    print(f"💡 Idea generated: {action.get('data', {}).get('title', 'Untitled')}")
        else:
            print(f"❌ API failed with status {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test orchestration endpoint
    try:
        print("\n2. Testing orchestration endpoint...")
        response = requests.post(
            'http://127.0.0.1:8002/api/orchestration/generate-ideas',
            json={
                'topic': 'fintech',
                'count': 3
            },
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Orchestration is working!")
            print(f"Generated {len(data.get('ideas', []))} ideas")
            for i, idea in enumerate(data.get('ideas', [])[:3], 1):
                print(f"  {i}. {idea.get('idea_title', 'Untitled')}")
        else:
            print(f"❌ Orchestration failed with status {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Orchestration error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 API Test Complete!")

if __name__ == "__main__":
    test_api() 