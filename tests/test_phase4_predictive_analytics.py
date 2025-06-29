#!/usr/bin/env python3
"""
Phase 4 Predictive Analytics Engine Test Suite
Tests the advanced predictive analytics capabilities
"""

import asyncio
import json
import time
from datetime import datetime
import aiohttp
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Phase4PredictiveAnalyticsTest:
    """Comprehensive test suite for Phase 4 Predictive Analytics"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
        
    async def run_all_tests(self):
        """Run comprehensive Phase 4 test suite"""
        logger.info("🔮 Starting Phase 4 Predictive Analytics Test Suite...")
        
        test_cases = [
            {
                'name': 'High Growth Startup Opportunity',
                'content': '''
                I'm seeing explosive growth in AI-powered customer service automation. 
                Our current solutions are outdated and expensive. Companies are desperately 
                looking for affordable, intelligent automation that can handle complex queries.
                Market is hot right now with tons of demand. Every SMB wants this technology 
                but current vendors price them out. Perfect timing for disruption.
                ''',
                'platform': 'reddit',
                'expected_score_range': (0.7, 1.0)
            },
            {
                'name': 'Emerging Market Trend',
                'content': '''
                Remote work tools are evolving rapidly. Traditional solutions like Zoom 
                and Slack are missing key features. Teams need better integration, 
                smarter automation, and seamless collaboration. Market is growing at 40% 
                yearly. Early players positioning for massive opportunity.
                ''',
                'platform': 'hackernews',
                'expected_score_range': (0.6, 0.9)
            },
            {
                'name': 'Seasonal Business Pattern',
                'content': '''
                E-commerce holiday season planning tools are broken. Retailers struggle 
                every year with inventory, staffing, and customer service during peaks.
                Cyclical problem that repeats annually. Someone needs to build better 
                predictive planning software for seasonal businesses.
                ''',
                'platform': 'twitter',
                'expected_score_range': (0.5, 0.8)
            },
            {
                'name': 'Volatile Market Opportunity',
                'content': '''
                Cryptocurrency trading bots are unpredictable and risky. Market volatility 
                makes automated trading dangerous. Uncertain regulatory environment.
                Technology changes rapidly. High risk, high reward scenario but timing 
                is critical and market is unstable.
                ''',
                'platform': 'unknown',
                'expected_score_range': (0.3, 0.7)
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            logger.info(f"\n📊 Test {i}/4: {test_case['name']}")
            result = await self.test_predictive_analytics(test_case)
            self.test_results.append(result)
            
            # Brief pause between tests
            await asyncio.sleep(1)
        
        await self.test_capabilities_endpoint()
        await self.test_error_handling()
        
        self.generate_comprehensive_report()
        
    async def test_predictive_analytics(self, test_case: dict):
        """Test predictive analytics endpoint"""
        try:
            payload = {
                'content': test_case['content'],
                'platform': test_case['platform'],
                'context': {'test_case': test_case['name']}
            }
            
            start_time = time.time()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/intelligence/predictive-analytics",
                    json=payload,
                    headers={'Content-Type': 'application/json'}
                ) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        # Validate response structure
                        validation_results = self.validate_phase4_response(result)
                        
                        # Check predictive score
                        predictive_score = result.get('predictive_score', 0)
                        score_min, score_max = test_case['expected_score_range']
                        score_in_range = score_min <= predictive_score <= score_max
                        
                        logger.info(f"✅ Predictive Score: {predictive_score:.3f} (Expected: {score_min}-{score_max})")
                        logger.info(f"⚡ Response Time: {response_time:.2f}s")
                        
                        # Log key insights
                        insights = result.get('predictive_insights', [])
                        logger.info(f"🧠 Generated {len(insights)} predictive insights")
                        
                        if insights:
                            top_insight = insights[0]
                            logger.info(f"   📈 Top Insight: {top_insight.get('type')} - {top_insight.get('description', '')[:100]}...")
                        
                        # Log forecasting
                        forecasting = result.get('predictive_forecasting', {})
                        logger.info(f"🔮 30-day forecast: {forecasting.get('trend_forecast_30d', 0):.2f}")
                        logger.info(f"📅 Opportunity window: {forecasting.get('opportunity_window', 'unknown')}")
                        
                        return {
                            'test_case': test_case['name'],
                            'status': 'PASSED',
                            'predictive_score': predictive_score,
                            'score_in_expected_range': score_in_range,
                            'response_time': response_time,
                            'insights_count': len(insights),
                            'validation_results': validation_results,
                            'details': {
                                'phase': result.get('phase'),
                                'engine_version': result.get('engine_version'),
                                'forecasting': forecasting,
                                'timing': result.get('optimal_timing', {}),
                                'recommendations_count': len(result.get('advanced_recommendations', []))
                            }
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ HTTP {response.status}: {error_text}")
                        return {
                            'test_case': test_case['name'],
                            'status': 'FAILED',
                            'error': f"HTTP {response.status}: {error_text}",
                            'response_time': response_time
                        }
                        
        except Exception as e:
            logger.error(f"❌ Test error: {str(e)}")
            return {
                'test_case': test_case['name'],
                'status': 'ERROR',
                'error': str(e)
            }
    
    def validate_phase4_response(self, result: dict) -> dict:
        """Validate Phase 4 response structure"""
        validation = {
            'has_predictive_score': 'predictive_score' in result,
            'has_forecasting': 'predictive_forecasting' in result,
            'has_insights': 'predictive_insights' in result,
            'has_timing_analysis': 'optimal_timing' in result,
            'has_recommendations': 'advanced_recommendations' in result,
            'has_competitive_advantage': 'competitive_advantage' in result,
            'has_capabilities': 'capabilities' in result,
            'has_foundation_analysis': 'foundation_analysis' in result,
            'correct_phase': result.get('phase') == 'Phase 4: Advanced Analytics & Predictive Intelligence',
            'correct_engine': result.get('engine_version') == 'predictive_analytics_engine_v1.0'
        }
        
        validation['overall_valid'] = all(validation.values())
        
        passed_checks = sum(1 for v in validation.values() if v)
        total_checks = len(validation) - 1  # Exclude overall_valid
        
        logger.info(f"📋 Response Validation: {passed_checks}/{total_checks} checks passed")
        
        return validation
    
    async def test_capabilities_endpoint(self):
        """Test Phase 4 capabilities endpoint"""
        logger.info("\n🔧 Testing Phase 4 Capabilities Endpoint...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/intelligence/predictive-analytics-capabilities"
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        capabilities = result.get('capabilities', {})
                        logger.info(f"✅ Capabilities loaded: {len(capabilities)} sections")
                        logger.info(f"📊 Engine: {capabilities.get('engine_name')}")
                        logger.info(f"🔮 Version: {capabilities.get('version')}")
                        logger.info(f"🎯 Features: {len(capabilities.get('capabilities', []))}")
                        
                        # Validate competitive advantage info
                        comp_advantage = capabilities.get('competitive_advantage', {})
                        if comp_advantage:
                            logger.info(f"💰 Cost advantage: {comp_advantage.get('luciq_advantage')}")
                        
                        self.test_results.append({
                            'test_case': 'Phase 4 Capabilities',
                            'status': 'PASSED',
                            'capabilities_count': len(capabilities),
                            'features_count': len(capabilities.get('capabilities', [])),
                            'has_competitive_info': bool(comp_advantage)
                        })
                    else:
                        logger.error(f"❌ Capabilities test failed: HTTP {response.status}")
                        self.test_results.append({
                            'test_case': 'Phase 4 Capabilities',
                            'status': 'FAILED',
                            'error': f"HTTP {response.status}"
                        })
                        
        except Exception as e:
            logger.error(f"❌ Capabilities test error: {str(e)}")
            self.test_results.append({
                'test_case': 'Phase 4 Capabilities',
                'status': 'ERROR',
                'error': str(e)
            })
    
    async def test_error_handling(self):
        """Test error handling scenarios"""
        logger.info("\n🚨 Testing Error Handling...")
        
        error_tests = [
            {
                'name': 'Empty Content',
                'payload': {'content': '', 'platform': 'test'},
                'expected_status': 422
            },
            {
                'name': 'Invalid Platform',
                'payload': {'content': 'test content', 'platform': None},
                'expected_status': 422
            }
        ]
        
        for error_test in error_tests:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.base_url}/api/intelligence/predictive-analytics",
                        json=error_test['payload'],
                        headers={'Content-Type': 'application/json'}
                    ) as response:
                        if response.status == error_test['expected_status']:
                            logger.info(f"✅ {error_test['name']}: Correct error handling")
                        else:
                            logger.warning(f"⚠️ {error_test['name']}: Expected {error_test['expected_status']}, got {response.status}")
                            
            except Exception as e:
                logger.error(f"❌ Error test failed: {str(e)}")
    
    def generate_comprehensive_report(self):
        """Generate comprehensive test report"""
        logger.info("\n" + "="*60)
        logger.info("📊 PHASE 4 PREDICTIVE ANALYTICS TEST REPORT")
        logger.info("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r.get('status') == 'PASSED'])
        failed_tests = len([r for r in self.test_results if r.get('status') == 'FAILED'])
        error_tests = len([r for r in self.test_results if r.get('status') == 'ERROR'])
        
        logger.info(f"📈 Total Tests: {total_tests}")
        logger.info(f"✅ Passed: {passed_tests}")
        logger.info(f"❌ Failed: {failed_tests}")
        logger.info(f"🚨 Errors: {error_tests}")
        logger.info(f"🎯 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        logger.info("\n📊 Test Details:")
        for result in self.test_results:
            status_emoji = "✅" if result['status'] == 'PASSED' else "❌" if result['status'] == 'FAILED' else "🚨"
            logger.info(f"{status_emoji} {result['test_case']}: {result['status']}")
            
            if result.get('predictive_score'):
                logger.info(f"   🔮 Predictive Score: {result['predictive_score']:.3f}")
            if result.get('response_time'):
                logger.info(f"   ⚡ Response Time: {result['response_time']:.2f}s")
            if result.get('insights_count'):
                logger.info(f"   🧠 Insights Generated: {result['insights_count']}")
        
        # Performance Summary
        response_times = [r.get('response_time', 0) for r in self.test_results if r.get('response_time')]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            logger.info(f"\n⚡ Performance Summary:")
            logger.info(f"   Average Response Time: {avg_response_time:.2f}s")
            logger.info(f"   Fastest Response: {min(response_times):.2f}s")
            logger.info(f"   Slowest Response: {max(response_times):.2f}s")
        
        logger.info("\n🎉 Phase 4 Predictive Analytics Testing Complete!")
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"phase4_test_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'total_tests': total_tests,
                    'passed': passed_tests,
                    'failed': failed_tests,
                    'errors': error_tests,
                    'success_rate': (passed_tests/total_tests)*100
                },
                'test_results': self.test_results,
                'performance': {
                    'avg_response_time': avg_response_time if response_times else 0,
                    'response_times': response_times
                }
            }, f, indent=2)
        
        logger.info(f"💾 Detailed results saved to: {results_file}")

async def main():
    """Main test execution"""
    print("🔮 Phase 4 Predictive Analytics Engine Test Suite")
    print("=" * 50)
    
    # Check if API server is running
    tester = Phase4PredictiveAnalyticsTest()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{tester.base_url}/api/health") as response:
                if response.status == 200:
                    print("✅ API server is running")
                else:
                    print(f"❌ API server check failed: HTTP {response.status}")
                    return
    except Exception as e:
        print(f"❌ Cannot connect to API server: {e}")
        print("💡 Make sure to start the API server first:")
        print("   python master_luciq_api.py")
        return
    
    # Run comprehensive test suite
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 