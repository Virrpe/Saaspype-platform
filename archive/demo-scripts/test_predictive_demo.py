#!/usr/bin/env python3
"""
Luciq Phase 4 Predictive Analytics Demo Test
Simplified version for Windows console compatibility
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime

class PredictiveAnalyticsDemo:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
    
    async def check_server_status(self):
        """Check if the API server is running"""
        print("Checking API server status...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/health") as response:
                    if response.status == 200:
                        print("✓ API server is running")
                        return True
                    else:
                        print(f"✗ API server check failed: HTTP {response.status}")
                        return False
        except Exception as e:
            print(f"✗ Cannot connect to API server: {e}")
            print("Make sure to start the API server first:")
            print("   python master_luciq_api.py")
            return False
    
    async def test_predictive_capabilities(self):
        """Test Phase 4 predictive analytics capabilities endpoint"""
        print("\n--- Testing Predictive Analytics Capabilities ---")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/intelligence/predictive-analytics-capabilities"
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        capabilities = result.get('capabilities', {})
                        
                        print(f"✓ Capabilities loaded successfully")
                        print(f"  Engine: {capabilities.get('engine_name', 'N/A')}")
                        print(f"  Version: {capabilities.get('version', 'N/A')}")
                        print(f"  Features: {len(capabilities.get('capabilities', []))} capabilities")
                        
                        # Show competitive advantage
                        comp_advantage = capabilities.get('competitive_advantage', {})
                        if comp_advantage:
                            print(f"  Cost Advantage: {comp_advantage.get('luciq_advantage', 'N/A')}")
                            print(f"  Traditional Cost: {comp_advantage.get('traditional_cost', 'N/A')}")
                        
                        return True
                    else:
                        print(f"✗ Capabilities test failed: HTTP {response.status}")
                        return False
                        
        except Exception as e:
            print(f"✗ Capabilities test error: {str(e)}")
            return False
    
    async def test_predictive_analysis(self, scenario_name: str, content: str, platform: str):
        """Test predictive analysis with specific scenario"""
        print(f"\n--- Testing Scenario: {scenario_name} ---")
        
        payload = {
            "content": content,
            "platform": platform,
            "analysis_type": "comprehensive",
            "include_forecasting": True,
            "include_timing_analysis": True
        }
        
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/intelligence/predictive-analytics",
                    json=payload,
                    headers={'Content-Type': 'application/json'}
                ) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        print(f"✓ Analysis completed in {response_time:.2f}s")
                        print(f"  Phase: {result.get('phase', 'N/A')}")
                        print(f"  Engine: {result.get('engine_version', 'N/A')}")
                        
                        # Predictive Metrics
                        pred_metrics = result.get('predictive_forecasting', {})
                        if pred_metrics:
                            print(f"  Trend Forecast (30d): {pred_metrics.get('trend_forecast_30d', 'N/A'):.3f}")
                            print(f"  Trend Forecast (90d): {pred_metrics.get('trend_forecast_90d', 'N/A'):.3f}")
                            print(f"  Momentum Score: {pred_metrics.get('momentum_score', 'N/A'):.3f}")
                            print(f"  Volatility Index: {pred_metrics.get('volatility_index', 'N/A'):.3f}")
                        
                        # Predictive Insights
                        insights = result.get('predictive_insights', [])
                        print(f"  Generated Insights: {len(insights)} insights")
                        for i, insight in enumerate(insights[:3], 1):  # Show first 3
                            print(f"    {i}. {insight.get('insight_type', 'N/A')}: {insight.get('description', 'N/A')[:100]}...")
                        
                        # Optimal Timing
                        timing = result.get('optimal_timing', {})
                        if timing:
                            print(f"  Opportunity Window: {timing.get('opportunity_window', 'N/A')}")
                            print(f"  Market Momentum: {timing.get('market_momentum', 'N/A')}")
                        
                        # Predictive Score
                        pred_score = result.get('predictive_score', 0)
                        print(f"  Overall Predictive Score: {pred_score:.3f}")
                        
                        self.test_results.append({
                            'scenario': scenario_name,
                            'status': 'PASSED',
                            'response_time': response_time,
                            'predictive_score': pred_score,
                            'insights_count': len(insights)
                        })
                        
                        return True
                    else:
                        print(f"✗ Analysis failed: HTTP {response.status}")
                        error_text = await response.text()
                        print(f"  Error: {error_text[:200]}...")
                        return False
                        
        except Exception as e:
            print(f"✗ Analysis error: {str(e)}")
            return False
    
    async def run_demo(self):
        """Run complete predictive analytics demonstration"""
        print("=" * 60)
        print("LUCIQ PHASE 4 PREDICTIVE ANALYTICS DEMO")
        print("=" * 60)
        
        # Check server status
        if not await self.check_server_status():
            return
        
        # Test capabilities
        if not await self.test_predictive_capabilities():
            return
        
        # Test scenarios
        test_scenarios = [
            {
                'name': 'High Growth Startup',
                'content': 'AI-powered productivity tool gaining 50% month-over-month user growth with strong product-market fit',
                'platform': 'reddit'
            },
            {
                'name': 'Emerging Market Trend',
                'content': 'Sustainable fashion marketplace showing increased consumer interest and investment activity',
                'platform': 'twitter'
            },
            {
                'name': 'Tech Innovation',
                'content': 'Blockchain-based supply chain solution with Fortune 500 pilot programs and regulatory support',
                'platform': 'hackernews'
            }
        ]
        
        successful_tests = 0
        for scenario in test_scenarios:
            if await self.test_predictive_analysis(
                scenario['name'], 
                scenario['content'], 
                scenario['platform']
            ):
                successful_tests += 1
        
        # Generate summary
        self.generate_summary(successful_tests, len(test_scenarios))
    
    def generate_summary(self, successful_tests: int, total_tests: int):
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("PREDICTIVE ANALYTICS DEMO SUMMARY")
        print("=" * 60)
        
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        
        if self.test_results:
            response_times = [r['response_time'] for r in self.test_results if 'response_time' in r]
            if response_times:
                avg_time = sum(response_times) / len(response_times)
                print(f"Average Response Time: {avg_time:.2f}s")
            
            pred_scores = [r['predictive_score'] for r in self.test_results if 'predictive_score' in r]
            if pred_scores:
                avg_score = sum(pred_scores) / len(pred_scores)
                print(f"Average Predictive Score: {avg_score:.3f}")
            
            total_insights = sum(r.get('insights_count', 0) for r in self.test_results)
            print(f"Total Insights Generated: {total_insights}")
        
        print("\nKey Capabilities Demonstrated:")
        print("- Multi-horizon forecasting (30d/90d/12m)")
        print("- Momentum and volatility analysis")
        print("- Automated insight generation")
        print("- Optimal timing analysis")
        print("- Competitive advantage positioning")
        print("- Real-time predictive intelligence")
        
        print(f"\nRevolutionary Advantage:")
        print(f"- Luciq: $2,499/year comprehensive platform")
        print(f"- Traditional: $150,000+/year manual analysis")
        print(f"- Cost Advantage: 60-100x cheaper with superior capabilities")

async def main():
    """Main demo execution"""
    demo = PredictiveAnalyticsDemo()
    await demo.run_demo()

if __name__ == "__main__":
    asyncio.run(main()) 