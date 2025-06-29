#!/usr/bin/env python3
"""
Test Pipeline Fix - Verify pipeline generates and saves ideas
"""

import requests
import json
import time

def test_pipeline():
    print("🧪 Testing Fixed Pipeline")
    print("=" * 50)
    
    # Test 1: Run the pipeline
    print("\n1. Testing 'run the full pipeline' command...")
    try:
        response = requests.post(
            'http://127.0.0.1:8002/api/chat/demo/message',
            json={'message': 'run the full pipeline'},
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Pipeline command working!")
            print(f"Response: {data.get('response', 'No response')[:150]}...")
            print(f"Intent: {data.get('intent', 'Unknown')}")
            print(f"Actions: {len(data.get('actions', []))}")
            
            # Check actions
            actions = data.get('actions', [])
            save_actions = [a for a in actions if a.get('type') == 'save_idea']
            pipeline_actions = [a for a in actions if a.get('type') == 'run_pipeline']
            
            print(f"Save idea actions: {len(save_actions)}")
            print(f"Pipeline actions: {len(pipeline_actions)}")
            
            # Show generated ideas
            for i, action in enumerate(save_actions[:3], 1):
                idea_data = action.get('data', {})
                print(f"  {i}. {idea_data.get('title', 'Untitled')}")
                print(f"     Category: {idea_data.get('category', 'Unknown')}")
                print(f"     Confidence: {idea_data.get('confidence_score', 'N/A')}")
            
            if pipeline_actions:
                pipeline_data = pipeline_actions[0].get('data', {})
                print(f"\nPipeline Results:")
                print(f"  Ideas generated: {pipeline_data.get('ideas_generated', 0)}")
                print(f"  Processing time: {pipeline_data.get('processing_time_ms', 0)}ms")
                print(f"  Engines used: {pipeline_data.get('engines_used', [])}")
                print(f"  Success: {pipeline_data.get('success', False)}")
                
        else:
            print(f"❌ Pipeline failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Pipeline error: {e}")
    
    # Test 2: Generate ideas
    print("\n2. Testing 'generate ideas' command...")
    try:
        response = requests.post(
            'http://127.0.0.1:8002/api/chat/demo/message',
            json={'message': 'generate ideas about fintech'},
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Generate ideas working!")
            print(f"Response: {data.get('response', 'No response')[:150]}...")
            print(f"Intent: {data.get('intent', 'Unknown')}")
            
            actions = data.get('actions', [])
            save_actions = [a for a in actions if a.get('type') == 'save_idea']
            generate_actions = [a for a in actions if a.get('type') == 'generate_ideas']
            
            print(f"Save idea actions: {len(save_actions)}")
            print(f"Generate actions: {len(generate_actions)}")
            
            # Show generated ideas
            for i, action in enumerate(save_actions[:3], 1):
                idea_data = action.get('data', {})
                print(f"  {i}. {idea_data.get('title', 'Untitled')}")
                
        else:
            print(f"❌ Generate ideas failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Generate ideas error: {e}")
    
    # Test 3: Check saved ideas
    print("\n3. Testing saved ideas retrieval...")
    try:
        response = requests.get(
            'http://127.0.0.1:8002/api/chat/demo/ideas',
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Ideas retrieval working!")
            print(f"Total ideas saved: {data.get('total', 0)}")
            
            ideas = data.get('ideas', [])
            for i, idea in enumerate(ideas[:5], 1):
                print(f"  {i}. {idea.get('title', 'Untitled')} ({idea.get('category', 'uncategorized')})")
                
        else:
            print(f"❌ Ideas retrieval failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Ideas retrieval error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Pipeline Test Complete!")

if __name__ == "__main__":
    test_pipeline() 