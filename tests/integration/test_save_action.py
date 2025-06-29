#!/usr/bin/env python3
"""
Test Save Action - Verify save_idea actions work
"""

import requests
import json

def test_save_action():
    print("🧪 Testing Save Action Processing")
    print("=" * 50)
    
    # Test 1: Direct save via demo endpoint
    print("\n1. Testing direct save via demo endpoint...")
    try:
        response = requests.post(
            'http://127.0.0.1:8002/api/chat/demo/save-idea',
            json={
                'title': 'Test Direct Save',
                'description': 'This is a direct save test',
                'category': 'testing'
            },
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Direct save working!")
            print(f"Message: {data.get('message', 'No message')}")
            print(f"Idea ID: {data.get('idea_id', 'No ID')}")
        else:
            print(f"❌ Direct save failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Direct save error: {e}")
    
    # Test 2: Check if idea was saved
    print("\n2. Checking if idea was saved...")
    try:
        response = requests.get(
            'http://127.0.0.1:8002/api/chat/demo/ideas',
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Ideas retrieval working!")
            print(f"Total ideas: {data.get('total', 0)}")
            
            ideas = data.get('ideas', [])
            for i, idea in enumerate(ideas, 1):
                print(f"  {i}. {idea.get('title', 'Untitled')} ({idea.get('category', 'uncategorized')})")
                print(f"     Created: {idea.get('created_at', 'Unknown')}")
                
        else:
            print(f"❌ Ideas retrieval failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Ideas retrieval error: {e}")
    
    # Test 3: Generate ideas and check actions
    print("\n3. Testing generate ideas and checking actions...")
    try:
        response = requests.post(
            'http://127.0.0.1:8002/api/chat/demo/message',
            json={'message': 'generate ideas about healthcare'},
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Generate ideas working!")
            print(f"Intent: {data.get('intent', 'Unknown')}")
            
            actions = data.get('actions', [])
            save_actions = [a for a in actions if a.get('type') == 'save_idea']
            
            print(f"Total actions: {len(actions)}")
            print(f"Save idea actions: {len(save_actions)}")
            
            # Show the save actions
            for i, action in enumerate(save_actions, 1):
                idea_data = action.get('data', {})
                print(f"  Action {i}:")
                print(f"    Title: {idea_data.get('title', 'No title')}")
                print(f"    Category: {idea_data.get('category', 'No category')}")
                print(f"    Description: {idea_data.get('description', 'No description')[:50]}...")
                
                # Try to save this idea directly
                try:
                    save_response = requests.post(
                        'http://127.0.0.1:8002/api/chat/demo/save-idea',
                        json=idea_data,
                        timeout=10
                    )
                    if save_response.status_code == 200:
                        save_result = save_response.json()
                        print(f"    ✅ Saved: {save_result.get('idea_id', 'No ID')}")
                    else:
                        print(f"    ❌ Save failed: {save_response.status_code}")
                except Exception as save_error:
                    print(f"    ❌ Save error: {save_error}")
                
        else:
            print(f"❌ Generate ideas failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Generate ideas error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Save Action Test Complete!")

if __name__ == "__main__":
    test_save_action() 