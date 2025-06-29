#!/usr/bin/env python3
"""
Test Claude Integration with Real Cost Tracking - FIXED DETECTION LOGIC
"""

import requests
import json
import time

def test_claude_with_costs():
    print("🤖 TESTING CLAUDE + COST TRACKING (FIXED DETECTION)")
    print("=" * 60)
    
    test_queries = [
        "Analyze the AI meal planning market opportunity for busy professionals",
        "What are the top 3 differentiation strategies for SaaS products?",
        "Give me a detailed competitive analysis of the fintech space"
    ]
    
    total_cost = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🎯 TEST {i}: {query[:50]}...")
        
        try:
            start_time = time.time()
            
            response = requests.post(
                "http://localhost:8000/api/chat/demo/message",
                json={"message": query},
                timeout=45
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('response', '') or data.get('ai_response', '')
                
                print(f"✅ Response received in {response_time:.2f}s")
                print(f"📝 Length: {len(ai_response)} characters")
                
                # FIXED DETECTION LOGIC - Check for actual Claude usage indicators
                token_usage = data.get('token_usage')
                claude_detected = False
                detection_reason = "No token usage data"
                
                if token_usage:
                    cost = token_usage.get('cost_usd', 0)
                    tokens = token_usage.get('total_tokens', 0)
                    input_tokens = token_usage.get('input_tokens', 0)
                    output_tokens = token_usage.get('output_tokens', 0)
                    total_cost += cost
                    
                    # PRIMARY DETECTION: If there are costs and tokens, Claude was used
                    if cost > 0 and tokens > 0:
                        claude_detected = True
                        detection_reason = f"Token usage: {tokens} tokens, ${cost:.6f} cost"
                    else:
                        # SECONDARY DETECTION: Check response characteristics
                        if len(ai_response) > 1500:  # Claude responses are typically longer
                            claude_detected = True
                            detection_reason = f"Long sophisticated response ({len(ai_response)} chars) but $0 cost - possible hardcoded key"
                        else:
                            detection_reason = f"Short response ({len(ai_response)} chars), $0 cost - likely fallback"
                    
                    print(f"💰 COST: ${cost:.6f}")
                    print(f"🔢 TOKENS: {tokens:,} (in: {input_tokens}, out: {output_tokens})")
                else:
                    # NO TOKEN DATA - Check response characteristics
                    if len(ai_response) > 1500 and response_time > 5:
                        claude_detected = True
                        detection_reason = f"Long response ({len(ai_response)} chars) + slow ({response_time:.1f}s) - likely Claude without tracking"
                    else:
                        detection_reason = f"Short/fast response - likely fallback intelligence"
                
                print(f"🤖 CLAUDE: {'✅ ACTIVE' if claude_detected else '❌ FALLBACK'}")
                print(f"🔍 Detection: {detection_reason}")
                
                # Show response preview
                preview = ai_response[:200] + "..." if len(ai_response) > 200 else ai_response
                print(f"💭 Preview: {preview}")
                
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 60)
        time.sleep(1)
    
    print(f"\n📊 TOTAL SESSION COST: ${total_cost:.6f}")
    
    if total_cost > 0:
        print(f"🎯 Average cost per query: ${total_cost/len(test_queries):.6f}")
        print(f"📈 Estimated cost per 1K chars: ${total_cost/3:.6f}")
        print("\n🔥 CLAUDE IS WORKING! Real costs being tracked!")
    else:
        print("\n⚠️ No costs detected - checking possible scenarios:")
        print("   1. Using hardcoded API key (costs not tracked in environment)")
        print("   2. Using fallback intelligence")
        print("   3. API key not properly configured")
        print("💡 Check API logs for 'HTTP Request: POST https://api.anthropic.com' messages")

def check_environment():
    """Check if Claude is properly configured"""
    print("🔧 ENVIRONMENT CHECK")
    print("=" * 30)
    
    import os
    claude_key = os.getenv('ANTHROPIC_API_KEY')
    
    if claude_key:
        masked_key = claude_key[:10] + "*" * (len(claude_key) - 20) + claude_key[-10:] if len(claude_key) > 20 else "***MASKED***"
        print(f"✅ ANTHROPIC_API_KEY: {masked_key}")
        return True
    else:
        print("❌ ANTHROPIC_API_KEY: Not set in environment")
        print("💡 Note: API may be using hardcoded key in master_luciq_api.py")
        return False

def check_api_logs():
    """Instructions for checking API logs"""
    print("\n🔍 HOW TO VERIFY CLAUDE USAGE:")
    print("=" * 40)
    print("1. Look for these log messages in your API console:")
    print("   'HTTP Request: POST https://api.anthropic.com/v1/messages \"HTTP/1.1 200 OK\"'")
    print("2. If you see these logs = Claude is working")
    print("3. If no logs = Using fallback intelligence")
    print("4. Response characteristics:")
    print("   • Claude: 2000-3500+ characters, sophisticated analysis")
    print("   • Fallback: 200-800 characters, templated responses")

if __name__ == "__main__":
    print("🚀 CLAUDE INTEGRATION TEST - FIXED DETECTION")
    print("=" * 70)
    
    # Check environment
    env_ok = check_environment()
    print()
    
    # Test API
    test_claude_with_costs()
    
    # Show verification instructions
    check_api_logs()
    
    print("\n🎯 NEXT STEPS:")
    print("1. Check your API console for Anthropic HTTP requests")
    print("2. If seeing 'HTTP/1.1 200 OK' from api.anthropic.com = Claude working")
    print("3. Use 'python live_cost_dashboard.py' for real-time monitoring")
    print("4. Each Claude response should be 2000+ characters with sophisticated analysis") 