#!/usr/bin/env python3
"""
Test Chat API Implementation
Quick test to verify the chat API endpoints work correctly
"""

import asyncio
import aiohttp
import json
from datetime import datetime

BASE_URL = "http://localhost:8002"

async def test_chat_api():
    """Test the chat API endpoints"""
    
    print("🧪 Testing Luciq Chat API Implementation")
    print("=" * 60)
    
    async with aiohttp.ClientSession() as session:
        
        # Test 1: Basic chat message
        print("\n1. Testing basic chat message...")
        try:
            async with session.post(
                f"{BASE_URL}/api/chat/message",
                json={
                    "message": "hello",
                    "session_id": "test_session_123"
                },
                headers={"Authorization": "Bearer demo_token"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ Chat response: {result['response'][:100]}...")
                    print(f"   Intent: {result['intent']}")
                    print(f"   Actions: {len(result['actions'])} actions")
                else:
                    print(f"❌ Chat API failed: {response.status}")
                    error_text = await response.text()
                    print(f"   Error: {error_text}")
        except Exception as e:
            print(f"❌ Chat API error: {e}")
        
        # Test 2: Save idea
        print("\n2. Testing save idea...")
        try:
            async with session.post(
                f"{BASE_URL}/api/chat/ideas/save",
                json={
                    "title": "AI-powered test idea",
                    "description": "This is a test idea for the chat API",
                    "category": "testing"
                },
                headers={"Authorization": "Bearer demo_token"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ Idea saved: {result['message']}")
                    print(f"   Idea ID: {result['idea_id']}")
                else:
                    print(f"❌ Save idea failed: {response.status}")
                    error_text = await response.text()
                    print(f"   Error: {error_text}")
        except Exception as e:
            print(f"❌ Save idea error: {e}")
        
        # Test 3: Generate ideas
        print("\n3. Testing idea generation...")
        try:
            async with session.post(
                f"{BASE_URL}/api/chat/generate-ideas",
                json={
                    "topic": "productivity apps",
                    "count": 3
                },
                headers={"Authorization": "Bearer demo_token"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ Generated {len(result['ideas'])} ideas")
                    print(f"   Processing time: {result['processing_time_ms']}ms")
                    print(f"   Engines used: {result['engines_used']}")
                    for i, idea in enumerate(result['ideas'][:2], 1):
                        print(f"   {i}. {idea.get('title', 'Untitled')}")
                else:
                    print(f"❌ Generate ideas failed: {response.status}")
                    error_text = await response.text()
                    print(f"   Error: {error_text}")
        except Exception as e:
            print(f"❌ Generate ideas error: {e}")
        
        # Test 4: Get user ideas
        print("\n4. Testing get user ideas...")
        try:
            async with session.get(
                f"{BASE_URL}/api/chat/ideas",
                headers={"Authorization": "Bearer demo_token"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ Retrieved {result['total']} ideas")
                    for idea in result['ideas'][:3]:
                        print(f"   - {idea['title']} ({idea['category']})")
                else:
                    print(f"❌ Get ideas failed: {response.status}")
                    error_text = await response.text()
                    print(f"   Error: {error_text}")
        except Exception as e:
            print(f"❌ Get ideas error: {e}")
        
        # Test 5: Generate insights
        print("\n5. Testing insights generation...")
        try:
            async with session.post(
                f"{BASE_URL}/api/chat/insights/generate",
                json={
                    "analysis_type": "comprehensive"
                },
                headers={"Authorization": "Bearer demo_token"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ Generated insights: {result['analysis_type']}")
                    if 'insights' in result and 'executive_summary' in result['insights']:
                        summary = result['insights']['executive_summary']
                        print(f"   Status: {summary.get('status', 'Unknown')}")
                        print(f"   Total ideas: {summary['overview']['total_ideas']}")
                else:
                    print(f"❌ Generate insights failed: {response.status}")
                    error_text = await response.text()
                    print(f"   Error: {error_text}")
        except Exception as e:
            print(f"❌ Generate insights error: {e}")
        
        # Test 6: Complex chat interaction
        print("\n6. Testing complex chat interaction...")
        try:
            async with session.post(
                f"{BASE_URL}/api/chat/message",
                json={
                    "message": "save my idea about AI-powered market research tool",
                    "session_id": "test_session_123"
                },
                headers={"Authorization": "Bearer demo_token"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ Complex interaction successful")
                    print(f"   Intent: {result['intent']}")
                    print(f"   Response: {result['response'][:100]}...")
                    print(f"   Actions triggered: {len(result['actions'])}")
                    for action in result['actions']:
                        print(f"     - {action['type']}: {action.get('data', {}).get('title', 'N/A')}")
                else:
                    print(f"❌ Complex interaction failed: {response.status}")
        except Exception as e:
            print(f"❌ Complex interaction error: {e}")

    print("\n" + "=" * 60)
    print("🎯 Chat API Test Complete!")
    print("\nNext steps:")
    print("1. Start the API server: python start_api.py")
    print("2. Start the frontend: python start_frontend.py")
    print("3. Visit: http://localhost:3000/ai-terminal")
    print("4. Try chatting with ARIA!")

if __name__ == "__main__":
    asyncio.run(test_chat_api()) 