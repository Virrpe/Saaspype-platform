#!/usr/bin/env python3
"""
Test Claude API key directly to verify it works
"""

import anthropic

def test_claude_key():
    print("🧪 TESTING CLAUDE API KEY DIRECTLY")
    print("=" * 50)
    
    # The new valid key
    claude_key = "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"
    
    try:
        print(f"🔑 Testing key: {claude_key[:20]}...{claude_key[-10:]}")
        
        # Create client
        client = anthropic.Anthropic(api_key=claude_key)
        
        # Test simple message with current model
        print("📤 Sending test message to Claude...")
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",  # Current model
            max_tokens=100,
            temperature=0.7,
            messages=[
                {"role": "user", "content": "Say hello and confirm you're Claude"}
            ]
        )
        
        print("✅ SUCCESS! Claude responded:")
        print(f"📝 Response: {response.content[0].text}")
        print(f"💰 Input tokens: {response.usage.input_tokens}")
        print(f"💰 Output tokens: {response.usage.output_tokens}")
        
        # Calculate cost (Claude 3.5 Sonnet pricing)
        input_cost = response.usage.input_tokens * 0.000003  # $3 per million
        output_cost = response.usage.output_tokens * 0.000015  # $15 per million
        total_cost = input_cost + output_cost
        
        print(f"💵 Total cost: ${total_cost:.6f}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

if __name__ == "__main__":
    test_claude_key() 