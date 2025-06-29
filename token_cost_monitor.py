#!/usr/bin/env python3
"""
Real-Time Token Cost Monitor for Luciq
Tracks Claude API usage and costs live
"""

import json
import time
from datetime import datetime
from typing import Dict, List
import threading
import os

class TokenCostMonitor:
    def __init__(self):
        self.costs_file = "token_costs.json"
        self.session_costs = {}
        self.total_costs = {
            "total_tokens": 0,
            "total_cost_usd": 0.0,
            "requests_count": 0,
            "average_cost_per_request": 0.0
        }
        
        # Claude 3.5 Sonnet pricing (as of 2024)
        self.claude_pricing = {
            "input_tokens_per_million": 3.00,   # $3.00 per million input tokens
            "output_tokens_per_million": 15.00,  # $15.00 per million output tokens
        }
        
        self.load_existing_costs()
        
    def load_existing_costs(self):
        """Load existing cost data"""
        try:
            if os.path.exists(self.costs_file):
                with open(self.costs_file, 'r') as f:
                    data = json.load(f)
                    self.total_costs = data.get('total_costs', self.total_costs)
                    self.session_costs = data.get('session_costs', {})
        except Exception as e:
            print(f"⚠️ Could not load existing costs: {e}")
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> Dict:
        """Calculate cost for a Claude API call"""
        
        # Calculate costs
        input_cost = (input_tokens / 1_000_000) * self.claude_pricing["input_tokens_per_million"]
        output_cost = (output_tokens / 1_000_000) * self.claude_pricing["output_tokens_per_million"]
        total_cost = input_cost + output_cost
        
        return {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "input_cost_usd": round(input_cost, 6),
            "output_cost_usd": round(output_cost, 6),
            "total_cost_usd": round(total_cost, 6),
            "cost_breakdown": {
                "input": f"${input_cost:.6f} ({input_tokens:,} tokens)",
                "output": f"${output_cost:.6f} ({output_tokens:,} tokens)"
            }
        }
    
    def track_request_cost(self, request_id: str, input_tokens: int, output_tokens: int, 
                          query: str = "", response_preview: str = "") -> Dict:
        """Track cost for a specific request"""
        
        cost_data = self.calculate_cost(input_tokens, output_tokens)
        
        # Add metadata
        cost_data.update({
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "query_preview": query[:100] + "..." if len(query) > 100 else query,
            "response_preview": response_preview[:100] + "..." if len(response_preview) > 100 else response_preview
        })
        
        # Update session costs
        self.session_costs[request_id] = cost_data
        
        # Update totals
        self.total_costs["total_tokens"] += cost_data["total_tokens"]
        self.total_costs["total_cost_usd"] += cost_data["total_cost_usd"]
        self.total_costs["requests_count"] += 1
        self.total_costs["average_cost_per_request"] = (
            self.total_costs["total_cost_usd"] / self.total_costs["requests_count"]
        )
        
        # Save to file
        self.save_costs()
        
        return cost_data
    
    def save_costs(self):
        """Save costs to file"""
        try:
            with open(self.costs_file, 'w') as f:
                json.dump({
                    "total_costs": self.total_costs,
                    "session_costs": self.session_costs,
                    "last_updated": datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save costs: {e}")
    
    def get_live_stats(self) -> Dict:
        """Get current cost statistics"""
        recent_requests = list(self.session_costs.values())[-10:]  # Last 10 requests
        
        return {
            "total_stats": self.total_costs,
            "recent_requests": recent_requests,
            "cost_per_1k_tokens": {
                "input": round((self.claude_pricing["input_tokens_per_million"] / 1000), 4),
                "output": round((self.claude_pricing["output_tokens_per_million"] / 1000), 4)
            },
            "session_summary": {
                "requests_this_session": len([r for r in recent_requests if 
                    (datetime.now() - datetime.fromisoformat(r["timestamp"])).seconds < 3600]),
                "cost_this_hour": sum(r["total_cost_usd"] for r in recent_requests if 
                    (datetime.now() - datetime.fromisoformat(r["timestamp"])).seconds < 3600)
            }
        }
    
    def print_live_dashboard(self):
        """Print a live cost dashboard"""
        stats = self.get_live_stats()
        
        print("\n🔥 LUCIQ TOKEN COST DASHBOARD")
        print("=" * 60)
        print(f"💰 Total Spent: ${stats['total_stats']['total_cost_usd']:.6f}")
        print(f"🔢 Total Tokens: {stats['total_stats']['total_tokens']:,}")
        print(f"📊 Total Requests: {stats['total_stats']['requests_count']}")
        print(f"📈 Avg Cost/Request: ${stats['total_stats']['average_cost_per_request']:.6f}")
        print()
        print(f"⏰ This Hour:")
        print(f"   • Requests: {stats['session_summary']['requests_this_session']}")
        print(f"   • Cost: ${stats['session_summary']['cost_this_hour']:.6f}")
        print()
        print("💡 Pricing (Claude 3.5 Sonnet):")
        print(f"   • Input: ${stats['cost_per_1k_tokens']['input']:.4f} per 1K tokens")
        print(f"   • Output: ${stats['cost_per_1k_tokens']['output']:.4f} per 1K tokens")
        
        if stats['recent_requests']:
            print("\n📋 Recent Requests:")
            for req in stats['recent_requests'][-5:]:  # Last 5
                time_ago = (datetime.now() - datetime.fromisoformat(req["timestamp"])).seconds
                print(f"   • ${req['total_cost_usd']:.6f} ({req['total_tokens']} tokens) - {time_ago}s ago")

# Global cost monitor instance
cost_monitor = TokenCostMonitor()

def track_claude_request(request_id: str, input_tokens: int, output_tokens: int, 
                        query: str = "", response: str = "") -> Dict:
    """Track a Claude request cost"""
    return cost_monitor.track_request_cost(request_id, input_tokens, output_tokens, query, response)

def get_cost_stats() -> Dict:
    """Get current cost statistics"""
    return cost_monitor.get_live_stats()

def print_cost_dashboard():
    """Print the live cost dashboard"""
    cost_monitor.print_live_dashboard()

if __name__ == "__main__":
    # Demo the cost monitor
    print("🔥 TOKEN COST MONITOR DEMO")
    
    # Simulate some requests
    track_claude_request("demo_1", 1000, 500, "Test query", "Test response")
    track_claude_request("demo_2", 1500, 800, "Another query", "Another response")
    
    print_cost_dashboard() 