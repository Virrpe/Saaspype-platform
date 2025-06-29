#!/usr/bin/env python3
"""
Advanced Intelligence Test for Luciq
Shows the dramatic improvement from "pre-generated" to "genuinely intelligent"
"""

import requests
import json
import time

class AdvancedIntelligenceTest:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.test_scenarios = [
            {
                "name": "🧠 Market Intelligence Test",
                "query": "I'm considering launching an AI-powered meal planning app for busy professionals. What are the key market opportunities and competitive landscape I should know about?",
                "expected_intelligence": ["market analysis", "competitive landscape", "opportunities", "professionals", "strategic insights"]
            },
            {
                "name": "🎯 Business Strategy Test", 
                "query": "How can I differentiate my SaaS product in the crowded project management space? What unique angles should I consider?",
                "expected_intelligence": ["differentiation", "unique positioning", "strategic advantage", "market gaps", "competitive analysis"]
            },
            {
                "name": "💡 Context Memory Test",
                "query": "Based on our previous discussion about the meal planning app, what would be the best go-to-market strategy for targeting busy professionals?",
                "expected_intelligence": ["context awareness", "go-to-market", "strategy", "targeting", "previous discussion"]
            },
            {
                "name": "🔍 Technical Intelligence Test",
                "query": "Should I build my real-time analytics dashboard with React + FastAPI or Vue + Django? What are the pros and cons for a startup?",
                "expected_intelligence": ["technical analysis", "pros and cons", "startup considerations", "architecture", "recommendations"]
            }
        ]

    def analyze_intelligence_level(self, response_text):
        """Analyze how intelligent the response feels"""
        
        # Intelligence indicators
        intelligence_signals = [
            "analysis shows", "data indicates", "research reveals", "trends suggest",
            "market analysis", "competitive landscape", "strategic advantage", 
            "according to", "insights from", "based on data", "studies show",
            "real-time intelligence", "platform analysis", "market signals",
            "predictive analytics", "business intelligence", "actionable insights",
            "competitive positioning", "market validation", "strategic recommendations"
        ]
        
        # Depth indicators
        depth_signals = [
            "specifically", "for example", "such as", "including", "particularly",
            "furthermore", "additionally", "however", "therefore", "consequently",
            "in contrast", "on the other hand", "meanwhile", "simultaneously"
        ]
        
        # Calculate intelligence score
        intelligence_score = sum(1 for signal in intelligence_signals if signal.lower() in response_text.lower())
        depth_score = sum(1 for signal in depth_signals if signal.lower() in response_text.lower())
        
        # Overall assessment
        total_score = intelligence_score + depth_score
        
        if total_score >= 8:
            intelligence_level = "🚀 GENIUS LEVEL"
        elif total_score >= 5:
            intelligence_level = "🧠 HIGHLY INTELLIGENT"
        elif total_score >= 3:
            intelligence_level = "💡 MODERATELY INTELLIGENT"
        elif total_score >= 1:
            intelligence_level = "🤖 BASIC INTELLIGENCE"
        else:
            intelligence_level = "😴 FEELS PRE-GENERATED"
        
        return {
            "intelligence_score": intelligence_score,
            "depth_score": depth_score,
            "total_score": total_score,
            "intelligence_level": intelligence_level,
            "response_length": len(response_text),
            "feels_intelligent": total_score >= 3
        }

    def test_scenario(self, scenario):
        """Test a specific intelligence scenario"""
        print(f"\n{scenario['name']}")
        print("=" * 60)
        print(f"QUERY: {scenario['query']}")
        print()
        
        try:
            # Send request to demo endpoint
            response = requests.post(
                f"{self.base_url}/api/chat/demo/message",
                json={"message": scenario['query']},
                timeout=45  # Longer timeout for complex queries
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('response', '') or data.get('ai_response', '')
                
                # Analyze intelligence
                analysis = self.analyze_intelligence_level(ai_response)
                
                print(f"🤖 AI RESPONSE ({analysis['intelligence_level']}):")
                print("-" * 40)
                print(ai_response)
                print("-" * 40)
                print()
                print(f"📊 INTELLIGENCE ANALYSIS:")
                print(f"   • Intelligence Score: {analysis['intelligence_score']}/20")
                print(f"   • Depth Score: {analysis['depth_score']}/15") 
                print(f"   • Total Score: {analysis['total_score']}/35")
                print(f"   • Response Length: {analysis['response_length']} characters")
                print(f"   • Feels Intelligent: {'✅ YES' if analysis['feels_intelligent'] else '❌ NO'}")
                print(f"   • Confidence: {data.get('confidence_score', 0):.2f}")
                print(f"   • Demo Mode: {data.get('demo_mode', False)}")
                
                return analysis
                
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def run_comprehensive_test(self):
        """Run comprehensive intelligence test"""
        print("🧠 LUCIQ ADVANCED INTELLIGENCE TEST")
        print("=" * 70)
        print("Testing the transformation from 'pre-generated' to 'genuinely intelligent'")
        print()
        
        # Check API health
        try:
            health = requests.get(f"{self.base_url}/api/health", timeout=5)
            if health.status_code == 200:
                print("✅ Luciq API is healthy and ready")
            else:
                print("❌ API health check failed")
                return
        except:
            print("❌ Cannot connect to Luciq API")
            return
        
        # Run all test scenarios
        results = []
        for scenario in self.test_scenarios:
            result = self.test_scenario(scenario)
            if result:
                results.append(result)
            
            # Small delay between tests
            time.sleep(2)
        
        # Generate final assessment
        if results:
            print("\n" + "=" * 70)
            print("🎯 FINAL INTELLIGENCE ASSESSMENT")
            print("=" * 70)
            
            avg_intelligence = sum(r['intelligence_score'] for r in results) / len(results)
            avg_depth = sum(r['depth_score'] for r in results) / len(results)
            avg_total = sum(r['total_score'] for r in results) / len(results)
            avg_length = sum(r['response_length'] for r in results) / len(results)
            
            intelligent_responses = sum(1 for r in results if r['feels_intelligent'])
            intelligence_rate = (intelligent_responses / len(results)) * 100
            
            print(f"📊 Overall Performance:")
            print(f"   • Average Intelligence Score: {avg_intelligence:.1f}/20")
            print(f"   • Average Depth Score: {avg_depth:.1f}/15")
            print(f"   • Average Total Score: {avg_total:.1f}/35")
            print(f"   • Average Response Length: {avg_length:.0f} characters")
            print(f"   • Intelligence Success Rate: {intelligence_rate:.1f}%")
            print()
            
            # Final verdict
            if avg_total >= 8:
                verdict = "🚀 TRANSFORMATION COMPLETE! Luciq now feels genuinely intelligent!"
                recommendation = "Users will be amazed by the intelligence upgrade."
            elif avg_total >= 5:
                verdict = "🧠 MAJOR IMPROVEMENT! Significant intelligence enhancement achieved."
                recommendation = "Consider adding Claude API key for even better results."
            elif avg_total >= 3:
                verdict = "💡 GOOD PROGRESS! Intelligence improvements are noticeable."
                recommendation = "Continue connecting more AI services for better results."
            else:
                verdict = "🔧 NEEDS WORK! Still feels somewhat pre-generated."
                recommendation = "Enable LLM integration and connect more AI services."
            
            print(f"🎊 FINAL VERDICT: {verdict}")
            print(f"💡 RECOMMENDATION: {recommendation}")
            
            # Show what to do next
            print()
            print("🚀 NEXT STEPS TO MAXIMIZE INTELLIGENCE:")
            print("   1. Add your Claude API key: set ANTHROPIC_API_KEY=your_key")
            print("   2. Connect existing AI services to the orchestrator")
            print("   3. Enable real-time intelligence gathering")
            print("   4. Test with more complex business scenarios")

if __name__ == "__main__":
    test = AdvancedIntelligenceTest()
    test.run_comprehensive_test() 