#!/usr/bin/env python3
"""
Phase 4 Streaming Pipeline Test Suite
Real-time signal simulation and streaming analytics verification
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime
import random
from typing import List, Dict

class StreamingPipelineTestSuite:
    """Comprehensive test suite for Phase 4 streaming pipeline"""
    
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self.session = None
        self.test_results = {}
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def health_check(self) -> bool:
        """Verify API server is healthy"""
        try:
            async with self.session.get(f"{self.api_base_url}/health") as response:
                data = await response.json()
                return data.get("status") == "healthy"
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False

    async def start_streaming_pipeline(self) -> Dict:
        """Start the streaming pipeline"""
        try:
            headers = {"Authorization": "Bearer test_token"}
            async with self.session.post(
                f"{self.api_base_url}/api/streaming/start",
                headers=headers
            ) as response:
                data = await response.json()
                print(f"🚀 Pipeline Start Response: {data.get('status', 'unknown')}")
                return data
        except Exception as e:
            print(f"❌ Failed to start pipeline: {e}")
            return {"status": "error", "error": str(e)}

    async def get_streaming_status(self) -> Dict:
        """Get current streaming pipeline status"""
        try:
            headers = {"Authorization": "Bearer test_token"}
            async with self.session.get(
                f"{self.api_base_url}/api/streaming/status",
                headers=headers
            ) as response:
                data = await response.json()
                print(f"📊 Pipeline Status: {data.get('is_streaming', False)}")
                return data
        except Exception as e:
            print(f"❌ Failed to get status: {e}")
            return {"is_streaming": False, "error": str(e)}

    async def simulate_signal_stream(self, signal_count: int = 50, signals_per_second: float = 5.0) -> Dict:
        """Simulate real-time signal stream"""
        try:
            headers = {"Authorization": "Bearer test_token"}
            params = {
                "signal_count": signal_count,
                "signals_per_second": signals_per_second
            }
            
            async with self.session.post(
                f"{self.api_base_url}/api/streaming/simulate",
                headers=headers,
                params=params
            ) as response:
                data = await response.json()
                print(f"🎯 Signal Simulation: {data.get('status', 'unknown')}")
                print(f"   Duration: {data.get('duration_seconds', 0):.1f}s")
                return data
        except Exception as e:
            print(f"❌ Failed to simulate signals: {e}")
            return {"status": "error", "error": str(e)}

    async def get_real_time_events(self, limit: int = 20) -> Dict:
        """Get recent real-time events"""
        try:
            headers = {"Authorization": "Bearer test_token"}
            params = {"limit": limit}
            
            async with self.session.get(
                f"{self.api_base_url}/api/streaming/events",
                headers=headers,
                params=params
            ) as response:
                data = await response.json()
                events_count = len(data.get('events', []))
                print(f"🎪 Real-time Events: {events_count} events retrieved")
                return data
        except Exception as e:
            print(f"❌ Failed to get events: {e}")
            return {"events": [], "error": str(e)}

    async def get_streaming_analytics(self, window: str = "all") -> Dict:
        """Get streaming analytics"""
        try:
            headers = {"Authorization": "Bearer test_token"}
            params = {"window": window}
            
            async with self.session.get(
                f"{self.api_base_url}/api/streaming/analytics",
                headers=headers,
                params=params
            ) as response:
                data = await response.json()
                print(f"📈 Analytics Status: {data.get('status', 'unknown')}")
                return data
        except Exception as e:
            print(f"❌ Failed to get analytics: {e}")
            return {"status": "error", "error": str(e)}

    async def stop_streaming_pipeline(self) -> Dict:
        """Stop the streaming pipeline"""
        try:
            headers = {"Authorization": "Bearer test_token"}
            async with self.session.post(
                f"{self.api_base_url}/api/streaming/stop",
                headers=headers
            ) as response:
                data = await response.json()
                print(f"🛑 Pipeline Stop: {data.get('status', 'unknown')}")
                return data
        except Exception as e:
            print(f"❌ Failed to stop pipeline: {e}")
            return {"status": "error", "error": str(e)}

    def display_test_results(self):
        """Display comprehensive test results"""
        print("\n" + "="*80)
        print("🎯 PHASE 4 STREAMING PIPELINE TEST RESULTS")
        print("="*80)
        
        for test_name, result in self.test_results.items():
            status_icon = "✅" if result.get("success", False) else "❌"
            print(f"{status_icon} {test_name}: {result.get('status', 'Unknown')}")
            
            if result.get("details"):
                for detail in result["details"]:
                    print(f"    • {detail}")
        
        print("\n" + "="*80)

    async def run_comprehensive_test(self):
        """Run comprehensive streaming pipeline test suite"""
        print("🚀 Starting Phase 4 Streaming Pipeline Test Suite")
        print("="*60)
        
        # Test 1: Health Check
        print("\n1️⃣ Testing API Health...")
        health_ok = await self.health_check()
        self.test_results["API Health Check"] = {
            "success": health_ok,
            "status": "Healthy" if health_ok else "Failed",
            "details": ["API server responding correctly"] if health_ok else ["API server not accessible"]
        }
        
        if not health_ok:
            print("❌ API not healthy, aborting tests")
            return
        
        # Test 2: Start Streaming Pipeline
        print("\n2️⃣ Starting Streaming Pipeline...")
        start_result = await self.start_streaming_pipeline()
        pipeline_started = start_result.get("status") in ["starting", "already_running"]
        self.test_results["Pipeline Startup"] = {
            "success": pipeline_started,
            "status": start_result.get("status", "Failed"),
            "details": [
                f"Response: {start_result.get('message', 'No message')}",
                f"Capabilities: {len(start_result.get('capabilities', []))} features"
            ]
        }
        
        # Wait for pipeline to initialize
        if pipeline_started:
            print("⏳ Waiting for pipeline initialization...")
            await asyncio.sleep(3)
        
        # Test 3: Pipeline Status Check
        print("\n3️⃣ Checking Pipeline Status...")
        status_result = await self.get_streaming_status()
        is_streaming = status_result.get("is_streaming", False)
        self.test_results["Pipeline Status"] = {
            "success": is_streaming,
            "status": "Streaming" if is_streaming else "Not Streaming",
            "details": [
                f"Uptime: {status_result.get('uptime_seconds', 0):.1f}s",
                f"Windows: {len(status_result.get('windows', {}))}"
            ]
        }
        
        if not is_streaming:
            print("❌ Pipeline not streaming, continuing with available tests...")
        
        # Test 4: Signal Stream Simulation
        print("\n4️⃣ Simulating Real-time Signal Stream...")
        simulation_result = await self.simulate_signal_stream(signal_count=30, signals_per_second=8.0)
        simulation_started = simulation_result.get("status") == "simulation_started"
        self.test_results["Signal Simulation"] = {
            "success": simulation_started,
            "status": simulation_result.get("status", "Failed"),
            "details": [
                f"Duration: {simulation_result.get('duration_seconds', 0):.1f}s",
                f"Message: {simulation_result.get('message', 'No message')}"
            ]
        }
        
        # Wait for some signals to be processed
        if simulation_started:
            print("⏳ Processing signals...")
            await asyncio.sleep(8)
        
        # Test 5: Real-time Events Retrieval
        print("\n5️⃣ Retrieving Real-time Events...")
        events_result = await self.get_real_time_events(limit=25)
        events_retrieved = len(events_result.get("events", [])) > 0
        self.test_results["Real-time Events"] = {
            "success": events_retrieved,
            "status": f"{len(events_result.get('events', []))} events" if events_retrieved else "No events",
            "details": [
                f"Total events: {events_result.get('total_events', 0)}",
                f"Event types: {len(events_result.get('event_types_available', []))}"
            ]
        }
        
        # Test 6: Streaming Analytics
        print("\n6️⃣ Analyzing Streaming Performance...")
        analytics_result = await self.get_streaming_analytics()
        analytics_available = analytics_result.get("status") != "not_streaming"
        
        analytics_details = []
        if analytics_available:
            real_time_stats = analytics_result.get("real_time_statistics", {})
            performance_metrics = analytics_result.get("performance_metrics", {})
            
            analytics_details = [
                f"Events processed: {real_time_stats.get('events_processed', 0)}",
                f"Processing rate: {performance_metrics.get('events_per_second', 0):.1f}/sec",
                f"Latency: {performance_metrics.get('average_latency_ms', 0):.1f}ms",
                f"Trends detected: {performance_metrics.get('trends_detected', 0)}",
                f"Anomalies found: {performance_metrics.get('anomalies_found', 0)}"
            ]
        
        self.test_results["Streaming Analytics"] = {
            "success": analytics_available,
            "status": "Available" if analytics_available else "Not Available",
            "details": analytics_details or ["Analytics not available"]
        }
        
        # Test 7: Revolutionary Capabilities Verification
        print("\n7️⃣ Verifying Revolutionary Capabilities...")
        capabilities_verified = False
        capabilities_details = []
        
        if is_streaming and status_result.get("phase_4_achievements"):
            achievements = status_result.get("phase_4_achievements", [])
            revolutionary_caps = status_result.get("revolutionary_capabilities", {})
            
            capabilities_verified = len(achievements) >= 5
            capabilities_details = [
                f"Achievements: {len(achievements)} features",
                f"Pattern detectors: {revolutionary_caps.get('pattern_detectors', 0)}",
                f"Anomaly detectors: {revolutionary_caps.get('anomaly_detectors', 0)}",
                f"Sliding windows: {revolutionary_caps.get('sliding_windows', 0)}",
                f"Target latency: {revolutionary_caps.get('processing_latency', 'Unknown')}"
            ]
        
        self.test_results["Revolutionary Capabilities"] = {
            "success": capabilities_verified,
            "status": "Verified" if capabilities_verified else "Unverified",
            "details": capabilities_details or ["Capabilities not accessible"]
        }
        
        # Test 8: System Integration Test
        print("\n8️⃣ Testing System Integration...")
        integration_score = 0
        integration_details = []
        
        # Score based on successful tests
        for test_name, result in self.test_results.items():
            if result.get("success", False):
                integration_score += 1
        
        integration_percentage = (integration_score / len(self.test_results)) * 100
        integration_success = integration_percentage >= 70
        
        integration_details = [
            f"Integration score: {integration_score}/{len(self.test_results)} tests passed",
            f"Success rate: {integration_percentage:.1f}%",
            f"Critical systems: {'Operational' if integration_percentage >= 70 else 'Issues detected'}"
        ]
        
        self.test_results["System Integration"] = {
            "success": integration_success,
            "status": f"{integration_percentage:.1f}% Success",
            "details": integration_details
        }
        
        # Test 9: Performance Benchmark
        print("\n9️⃣ Performance Benchmarking...")
        start_time = time.time()
        
        # Quick performance test
        for i in range(3):
            await self.get_streaming_status()
        
        benchmark_duration = time.time() - start_time
        performance_acceptable = benchmark_duration < 2.0
        
        self.test_results["Performance Benchmark"] = {
            "success": performance_acceptable,
            "status": f"{benchmark_duration:.3f}s for 3 calls",
            "details": [
                f"Average response time: {benchmark_duration/3:.3f}s",
                f"Performance: {'Excellent' if benchmark_duration < 1.0 else 'Good' if benchmark_duration < 2.0 else 'Needs optimization'}"
            ]
        }
        
        # Final cleanup
        print("\n🧹 Cleaning up...")
        await self.stop_streaming_pipeline()
        
        # Display results
        self.display_test_results()
        
        # Summary
        successful_tests = sum(1 for result in self.test_results.values() if result.get("success", False))
        total_tests = len(self.test_results)
        
        print(f"\n🎯 TEST SUITE SUMMARY:")
        print(f"   Tests Passed: {successful_tests}/{total_tests}")
        print(f"   Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        print(f"   Phase 4 Status: {'✅ OPERATIONAL' if successful_tests >= 6 else '⚠️ NEEDS ATTENTION'}")
        print("\n" + "="*80)

async def main():
    """Main test execution"""
    print("🚀 PHASE 4 STREAMING PIPELINE COMPREHENSIVE TEST")
    print("Revolutionary Real-time Architecture Verification")
    print("="*80)
    
    async with StreamingPipelineTestSuite() as test_suite:
        await test_suite.run_comprehensive_test()
    
    print("\n🎉 Test suite completed!")

if __name__ == "__main__":
    asyncio.run(main()) 