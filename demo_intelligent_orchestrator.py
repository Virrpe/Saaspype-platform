#!/usr/bin/env python3
"""
Demo: Luciq Intelligent Orchestrator
Shows the difference between old static responses vs new intelligent responses
"""

import asyncio
import json
import requests
import time
from datetime import datetime

class LuciqIntelligenceDemo:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.demo_scenarios = [
            {
                "name": "Market Research Query",
                "message": "I'm thinking about starting a AI-powered meal planning app for busy professionals. What are the key pain points in this market?",
                "expected_intelligence": "Real-time market analysis, competitor research, pain point detection"
            },
            {
                "name": "Business Strategy Question", 
                "message": "How can I differentiate my SaaS product in a crowded market like project management tools?",
                "expected_intelligence": "Strategic analysis, competitive positioning, unique value propositions"
            },
            {
                "name": "Technical Implementation",
                "message": "Should I build my MVP with Django or FastAPI for a real-time analytics dashboard?",
                "expected_intelligence": "Technical recommendations, architecture analysis, pros/cons"
            },
            {
                "name": "Follow-up Context Test",
                "message": "Based on our previous discussion about the meal planning app, what's the best go-to-market strategy?",
                "expected_intelligence": "Context awareness, strategic recommendations, market entry"
            }
        ]

    def compare_responses(self, old_response: str, new_response: str) -> dict:
        """Compare old vs new response quality"""
        
        intelligence_indicators = [
            "real-time analysis", "current market", "specific data", "actionable insights",
            "competitive analysis", "strategic recommendation", "personalized advice",
            "context awareness", "follow-up questions", "detailed methodology"
        ]
        
        old_score = sum(1 for indicator in intelligence_indicators if indicator.lower() in old_response.lower())
        new_score = sum(1 for indicator in intelligence_indicators if indicator.lower() in new_response.lower())
        
        return {
            "old_intelligence_score": old_score,
            "new_intelligence_score": new_score,
            "improvement_percentage": ((new_score - old_score) / max(old_score, 1)) * 100,
            "feels_intelligent": new_score >= 3,
            "old_length": len(old_response),
            "new_length": len(new_response),
            "response_depth": "Deep" if new_score >= 4 else "Surface" if new_score >= 2 else "Shallow"
        }

    async def test_chat_intelligence(self, message: str) -> dict:
        """Test the enhanced chat intelligence"""
        try:
            response = requests.post(
                f"{self.base_url}/api/chat/message",
                json={"message": message, "user_id": 1},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "response": data.get("ai_response", ""),
                    "confidence": data.get("confidence_score", 0),
                    "analysis_type": data.get("conversation_context", {}).get("intent", "unknown"),
                    "real_time_data": data.get("ai_insights", {}).get("real_time_intelligence", False),
                    "response_time": response.elapsed.total_seconds()
                }
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_static_response(self, message: str) -> str:
        """Simulate old static response system"""
        if "pain point" in message.lower():
            return "I've analyzed your query about pain points. Based on general market patterns, here are some common challenges users face. This analysis uses standard business intelligence frameworks."
        elif "differentiate" in message.lower() or "strategy" in message.lower():
            return "For market differentiation, consider these standard approaches: unique features, pricing strategy, and customer service. This recommendation follows common business best practices."
        elif "django" in message.lower() or "fastapi" in message.lower():
            return "Both Django and FastAPI are good choices. Django offers more features out of the box, while FastAPI is faster for APIs. Choose based on your team's experience."
        else:
            return "Thank you for your question. I'll analyze this using our business intelligence framework and provide you with insights based on standard market research methodologies."

    async def run_intelligence_demo(self):
        """Run the complete intelligence demonstration"""
        print("🚀 LUCIQ INTELLIGENCE ORCHESTRATOR DEMO")
        print("=" * 60)
        print(f"Testing enhanced intelligence vs static responses...")
        print(f"Base URL: {self.base_url}")
        print()
        
        # Check if API is running
        try:
            health_check = requests.get(f"{self.base_url}/api/health", timeout=5)
            if health_check.status_code != 200:
                print("❌ API not running. Start with: python master_luciq_api.py")
                return
            print("✅ Luciq API is running")
        except:
            print("❌ Cannot connect to Luciq API. Please start the server first.")
            return
        
        print()
        
        overall_results = {
            "scenarios_tested": 0,
            "intelligence_improvements": [],
            "average_improvement": 0,
            "feels_intelligent_count": 0
        }
        
        for i, scenario in enumerate(self.demo_scenarios, 1):
            print(f"📋 SCENARIO {i}: {scenario['name']}")
            print(f"Query: {scenario['message']}")
            print()
            
            # Generate old static response
            old_response = self.generate_static_response(scenario['message'])
            print("🤖 OLD RESPONSE (Static):")
            print(f"   {old_response}")
            print()
            
            # Get new intelligent response
            print("🧠 NEW RESPONSE (Intelligent Orchestrator):")
            result = await self.test_chat_intelligence(scenario['message'])
            
            if result['success']:
                new_response = result['response']
                print(f"   {new_response}")
                print()
                
                # Compare responses
                comparison = self.compare_responses(old_response, new_response)
                
                print("📊 INTELLIGENCE ANALYSIS:")
                print(f"   Old Intelligence Score: {comparison['old_intelligence_score']}/10")
                print(f"   New Intelligence Score: {comparison['new_intelligence_score']}/10")
                print(f"   Improvement: {comparison['improvement_percentage']:.1f}%")
                print(f"   Response Depth: {comparison['response_depth']}")
                print(f"   Feels Intelligent: {'✅ YES' if comparison['feels_intelligent'] else '❌ NO'}")
                print(f"   Response Time: {result['response_time']:.2f}s")
                print(f"   Confidence Score: {result['confidence']:.2f}")
                print()
                
                # Track overall results
                overall_results["scenarios_tested"] += 1
                overall_results["intelligence_improvements"].append(comparison['improvement_percentage'])
                if comparison['feels_intelligent']:
                    overall_results["feels_intelligent_count"] += 1
                    
            else:
                print(f"   ❌ Error: {result['error']}")
                print()
            
            print("-" * 60)
            print()
            
            # Small delay between tests
            await asyncio.sleep(1)
        
        # Final summary
        if overall_results["scenarios_tested"] > 0:
            overall_results["average_improvement"] = sum(overall_results["intelligence_improvements"]) / len(overall_results["intelligence_improvements"])
            
            print("🎯 FINAL INTELLIGENCE ASSESSMENT")
            print("=" * 60)
            print(f"✅ Scenarios Tested: {overall_results['scenarios_tested']}")
            print(f"🧠 Average Intelligence Improvement: {overall_results['average_improvement']:.1f}%")
            print(f"⭐ Scenarios That Feel Intelligent: {overall_results['feels_intelligent_count']}/{overall_results['scenarios_tested']}")
            print(f"🎊 Intelligence Success Rate: {(overall_results['feels_intelligent_count']/overall_results['scenarios_tested'])*100:.1f}%")
            
            if overall_results['average_improvement'] > 100:
                print("🚀 RESULT: MAJOR INTELLIGENCE BREAKTHROUGH!")
                print("   Luciq now feels genuinely intelligent instead of scripted")
            elif overall_results['average_improvement'] > 50:
                print("✅ RESULT: SIGNIFICANT INTELLIGENCE IMPROVEMENT")
                print("   Users will notice the enhanced intelligence")
            else:
                print("⚠️  RESULT: MODERATE IMPROVEMENT")
                print("   Additional enhancements needed")

if __name__ == "__main__":
    demo = LuciqIntelligenceDemo()
    asyncio.run(demo.run_intelligence_demo()) 