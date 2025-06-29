#!/usr/bin/env python3
"""
Live Cost Dashboard for Luciq
Real-time monitoring of Claude API costs
"""

import json
import time
import os
import requests
from datetime import datetime, timedelta
import threading
import sys

class LiveCostDashboard:
    def __init__(self):
        self.costs_file = "token_costs.json"
        self.running = True
        self.update_interval = 2  # seconds
        
    def load_costs(self):
        """Load current cost data"""
        try:
            if os.path.exists(self.costs_file):
                with open(self.costs_file, 'r') as f:
                    return json.load(f)
            return {"total_costs": {"total_cost_usd": 0, "total_tokens": 0, "requests_count": 0}, "session_costs": {}}
        except:
            return {"total_costs": {"total_cost_usd": 0, "total_tokens": 0, "requests_count": 0}, "session_costs": {}}
    
    def calculate_rate_per_hour(self, session_costs):
        """Calculate current spending rate per hour"""
        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)
        
        recent_costs = []
        for request_data in session_costs.values():
            try:
                request_time = datetime.fromisoformat(request_data["timestamp"])
                if request_time > one_hour_ago:
                    recent_costs.append(request_data["total_cost_usd"])
            except:
                continue
        
        return sum(recent_costs), len(recent_costs)
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_dashboard(self):
        """Display the live cost dashboard"""
        while self.running:
            try:
                # Load current data
                data = self.load_costs()
                total_costs = data.get("total_costs", {})
                session_costs = data.get("session_costs", {})
                
                # Calculate hourly rate
                hourly_cost, hourly_requests = self.calculate_rate_per_hour(session_costs)
                
                # Get recent requests
                recent_requests = list(session_costs.values())[-10:] if session_costs else []
                
                # Clear screen and display
                self.clear_screen()
                
                print("🔥 LUCIQ LIVE COST DASHBOARD")
                print("=" * 60)
                print(f"💰 Total Spent: ${total_costs.get('total_cost_usd', 0):.6f}")
                print(f"🔢 Total Tokens: {total_costs.get('total_tokens', 0):,}")
                print(f"📊 Total Requests: {total_costs.get('requests_count', 0)}")
                
                if total_costs.get('requests_count', 0) > 0:
                    avg_cost = total_costs.get('total_cost_usd', 0) / total_costs.get('requests_count', 1)
                    print(f"📈 Avg Cost/Request: ${avg_cost:.6f}")
                
                print()
                print(f"⏰ Last Hour:")
                print(f"   • Cost: ${hourly_cost:.6f}")
                print(f"   • Requests: {hourly_requests}")
                
                if hourly_requests > 0:
                    hourly_rate = hourly_cost
                    daily_projection = hourly_rate * 24
                    monthly_projection = daily_projection * 30
                    
                    print(f"   • Hourly Rate: ${hourly_rate:.6f}/hour")
                    print(f"   • Daily Projection: ${daily_projection:.4f}/day")
                    print(f"   • Monthly Projection: ${monthly_projection:.2f}/month")
                
                print()
                print("💡 Claude 3.5 Sonnet Pricing:")
                print("   • Input: $0.003 per 1K tokens")
                print("   • Output: $0.015 per 1K tokens")
                
                if recent_requests:
                    print("\n📋 Recent Requests:")
                    for req in recent_requests[-5:]:  # Last 5
                        try:
                            timestamp = datetime.fromisoformat(req["timestamp"])
                            time_ago = int((datetime.now() - timestamp).total_seconds())
                            
                            if time_ago < 60:
                                time_str = f"{time_ago}s ago"
                            elif time_ago < 3600:
                                time_str = f"{time_ago//60}m ago"
                            else:
                                time_str = f"{time_ago//3600}h ago"
                            
                            print(f"   • ${req['total_cost_usd']:.6f} ({req['total_tokens']} tokens) - {time_str}")
                            
                            # Show query preview
                            query_preview = req.get('query_preview', '')[:40]
                            if query_preview:
                                print(f"     📝 \"{query_preview}...\"")
                        except:
                            continue
                
                print(f"\n🔄 Last updated: {datetime.now().strftime('%H:%M:%S')}")
                print("Press Ctrl+C to exit")
                
                time.sleep(self.update_interval)
                
            except KeyboardInterrupt:
                self.running = False
                print("\n👋 Cost monitoring stopped.")
                break
            except Exception as e:
                print(f"⚠️ Dashboard error: {e}")
                time.sleep(self.update_interval)

def test_api_with_cost_tracking():
    """Test the API and show costs"""
    print("🧪 TESTING API WITH COST TRACKING")
    print("=" * 50)
    
    test_queries = [
        "What are the key pain points in AI-powered meal planning apps?",
        "How can I differentiate my SaaS product in project management?",
        "What's the best market opportunity in fintech for 2024?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🎯 Test {i}: {query[:40]}...")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/chat/demo/message",
                json={"message": query},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Show token usage if available
                token_usage = data.get('token_usage', {})
                if token_usage:
                    print(f"💰 Cost: ${token_usage.get('cost_usd', 0):.6f}")
                    print(f"🔢 Tokens: {token_usage.get('total_tokens', 0)}")
                
                print(f"✅ Request successful")
                
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(2)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_api_with_cost_tracking()
    else:
        dashboard = LiveCostDashboard()
        
        print("🚀 Starting Live Cost Dashboard...")
        print("This will monitor Claude API costs in real-time.")
        print("Make some API requests to see costs appear!")
        print()
        
        dashboard.display_dashboard() 