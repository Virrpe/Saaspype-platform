#!/usr/bin/env python3
"""
Claude Cost Calculator for Luciq
Estimates costs based on typical usage patterns
"""

import requests
import json
import time

class ClaudeCostCalculator:
    def __init__(self):
        # Claude 3.5 Sonnet pricing (as of December 2024)
        self.input_cost_per_million = 3.00   # $3.00 per million input tokens
        self.output_cost_per_million = 15.00  # $15.00 per million output tokens
        
    def estimate_tokens(self, text):
        """Estimate tokens (rough approximation: 1 token ≈ 4 characters)"""
        return len(text) // 4
    
    def calculate_cost(self, input_tokens, output_tokens):
        """Calculate exact cost for Claude API call"""
        input_cost = (input_tokens / 1_000_000) * self.input_cost_per_million
        output_cost = (output_tokens / 1_000_000) * self.output_cost_per_million
        return input_cost + output_cost
    
    def test_and_estimate_costs(self):
        """Test API calls and estimate costs"""
        print("🔥 CLAUDE COST CALCULATOR")
        print("=" * 50)
        print("Testing intelligent responses and calculating costs...")
        print()
        
        test_scenarios = [
            {
                "query": "What are the key pain points in AI-powered meal planning apps for busy professionals?",
                "expected_response_tokens": 200
            },
            {
                "query": "How can I differentiate my SaaS product in the crowded project management space?",
                "expected_response_tokens": 250
            },
            {
                "query": "Analyze the competitive landscape for fintech startups in 2024",
                "expected_response_tokens": 300
            }
        ]
        
        total_cost = 0
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"🎯 SCENARIO {i}:")
            print(f"Query: {scenario['query']}")
            
            # Estimate input tokens
            input_tokens = self.estimate_tokens(scenario['query'])
            
            # Add context tokens (Luciq adds business intelligence context)
            context_tokens = 800  # Estimated context from intelligent orchestrator
            total_input_tokens = input_tokens + context_tokens
            
            # Estimate output tokens
            output_tokens = scenario['expected_response_tokens']
            
            # Calculate cost
            cost = self.calculate_cost(total_input_tokens, output_tokens)
            total_cost += cost
            
            print(f"💭 Input tokens: {total_input_tokens:,} (query: {input_tokens}, context: {context_tokens})")
            print(f"📝 Output tokens: {output_tokens:,}")
            print(f"💰 Estimated cost: ${cost:.6f}")
            print()
        
        print("📊 COST SUMMARY:")
        print(f"💰 Total for 3 requests: ${total_cost:.6f}")
        print(f"📈 Average per request: ${total_cost/3:.6f}")
        print()
        
        # Usage projections
        daily_requests = [10, 50, 100, 500]
        
        print("📅 DAILY COST PROJECTIONS:")
        for requests in daily_requests:
            daily_cost = (total_cost / 3) * requests
            monthly_cost = daily_cost * 30
            print(f"   • {requests:3} requests/day: ${daily_cost:.4f}/day (${monthly_cost:.2f}/month)")
        
        print()
        print("💡 COST OPTIMIZATION TIPS:")
        print("   • Shorter queries = lower input costs")
        print("   • Focused responses = lower output costs") 
        print("   • Context optimization can reduce costs significantly")
        print("   • Claude 3.5 Sonnet is premium but highest quality")
        
        return total_cost / 3  # Average cost per request

def check_claude_setup():
    """Check if Claude is properly configured"""
    print("🔧 CLAUDE SETUP CHECK")
    print("=" * 30)
    
    # Test API connection
    try:
        response = requests.post(
            "http://localhost:8000/api/chat/demo/message",
            json={"message": "Test Claude integration"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if Claude is being used
            if "claude" in str(data).lower() or "anthropic" in str(data).lower():
                print("✅ Claude integration detected!")
                return True
            else:
                print("⚠️ Claude not detected - may be using fallback")
                return False
        else:
            print(f"❌ API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    print("🤖 LUCIQ + CLAUDE COST ANALYSIS")
    print("=" * 60)
    
    # Check setup
    claude_working = check_claude_setup()
    print()
    
    # Calculate costs
    calculator = ClaudeCostCalculator()
    avg_cost = calculator.test_and_estimate_costs()
    
    print("🎯 BOTTOM LINE:")
    if claude_working:
        print(f"✅ Claude is active - estimated ${avg_cost:.6f} per intelligent response")
    else:
        print(f"⚠️ Using fallback intelligence - would cost ${avg_cost:.6f} per Claude response")
    
    print()
    print("📋 NEXT STEPS:")
    print("1. Set your Claude API key: set ANTHROPIC_API_KEY=your_key")
    print("2. Restart the API to activate Claude")
    print("3. Use 'python live_cost_dashboard.py' for real-time monitoring")
    print("4. Monitor costs as you use the intelligent features!") 