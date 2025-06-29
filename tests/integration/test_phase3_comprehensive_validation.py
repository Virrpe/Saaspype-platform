#!/usr/bin/env python3
"""
Phase 3 Comprehensive Validation Suite
Tests all Phase 1-3 capabilities: Dialectical Intelligence + Streaming Pipeline + Semantic Intelligence

VALIDATION SCOPE:
- Master API startup and health
- All authentication endpoints
- Discovery service (999-line crown jewel)
- Mega scraper (15+ platforms)
- Intelligence engine (dialectical + semantic)
- Streaming pipeline (temporal patterns)
- Semantic intelligence (Phase 3)
- Chat service
- System endpoints

Expected Result: 100% operational validation of triple-layer intelligence system
"""

import asyncio
import aiohttp
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Any

class Phase3ComprehensiveValidator:
    """Comprehensive validation of Phase 3 enhanced Master API"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.test_results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_details': []
        }
        self.auth_token = None
        
    async def run_comprehensive_validation(self):
        """Run complete validation suite"""
        print("🚀 PHASE 3 COMPREHENSIVE VALIDATION SUITE")
        print("=" * 60)
        print(f"Target: {self.base_url}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print()
        
        start_time = time.time()
        
        # Core System Tests
        await self.test_system_health()
        await self.test_system_capabilities()
        
        # Authentication Tests
        await self.test_authentication_flow()
        
        # Discovery Service Tests (Crown Jewel)
        await self.test_discovery_service()
        
        # Mega Scraper Tests
        await self.test_mega_scraper()
        
        # Phase 1: Dialectical Intelligence Tests
        await self.test_dialectical_intelligence()
        
        # Phase 2: Streaming Pipeline Tests
        await self.test_streaming_pipeline()
        
        # Phase 3: Semantic Intelligence Tests (NEW)
        await self.test_semantic_intelligence()
        
        # Intelligence Engine Tests
        await self.test_intelligence_engine()
        
        # Chat Service Tests
        await self.test_chat_service()
        
        # System Integration Tests
        await self.test_system_integration()
        
        # Performance and Load Tests
        await self.test_performance_metrics()
        
        duration = time.time() - start_time
        await self.generate_validation_report(duration)
    
    async def test_system_health(self):
        """Test core system health and status"""
        print("🏥 Testing System Health...")
        
        # Root endpoint
        await self.test_endpoint("GET", "/", "Root endpoint")
        
        # Health check
        await self.test_endpoint("GET", "/api/health", "Health check")
        
        # System stats
        await self.test_endpoint("GET", "/api/system/stats", "System statistics")
        
    async def test_system_capabilities(self):
        """Test system capabilities reporting"""
        print("🎯 Testing System Capabilities...")
        
        # Intelligence capabilities
        await self.test_endpoint("GET", "/api/intelligence/capabilities", "Intelligence capabilities")
        
        # Semantic capabilities (Phase 3)
        await self.test_endpoint("GET", "/api/semantic/capabilities", "Semantic capabilities")
        
    async def test_authentication_flow(self):
        """Test complete authentication flow"""
        print("🔐 Testing Authentication Flow...")
        
        # Generate unique test user
        timestamp = int(time.time())
        test_user = {
            "username": f"testuser{timestamp}",
            "email": f"test{timestamp}@example.com",
            "password": "testpassword123"
        }
        
        # Test registration
        register_result = await self.test_endpoint(
            "POST", "/api/auth/register", "User registration", data=test_user
        )
        
        if register_result.get('success'):
            # Test login
            login_data = {
                "username": test_user["username"],
                "password": test_user["password"]
            }
            
            login_result = await self.test_endpoint(
                "POST", "/api/auth/login", "User login", data=login_data
            )
            
            if login_result.get('access_token'):
                self.auth_token = login_result['access_token']
                
                # Test authenticated endpoint
                headers = {"Authorization": f"Bearer {self.auth_token}"}
                await self.test_endpoint(
                    "GET", "/api/auth/me", "Get current user", headers=headers
                )
    
    async def test_discovery_service(self):
        """Test discovery service (999-line crown jewel)"""
        print("💎 Testing Discovery Service (Crown Jewel)...")
        
        # Test subreddit discovery
        discovery_request = {
            "subreddit": "startups",
            "limit": 3,
            "hours_back": 24
        }
        
        await self.test_endpoint(
            "POST", "/api/discovery/analyze", "Pain point discovery", data=discovery_request
        )
        
        # Test supported subreddits
        await self.test_endpoint("GET", "/api/discovery/subreddits", "Supported subreddits")
        
        # Test discovery sessions
        await self.test_endpoint("GET", "/api/discovery/sessions", "Discovery sessions")
    
    async def test_mega_scraper(self):
        """Test mega scraper (15+ platforms)"""
        print("🌐 Testing Mega Scraper (15+ Platforms)...")
        
        # Test mega scan
        await self.test_endpoint(
            "POST", "/api/scraper/mega-scan?hours_back=1", "Mega source scan"
        )
        
        # Test scraper sources
        await self.test_endpoint("GET", "/api/scraper/sources", "Scraper sources")
    
    async def test_dialectical_intelligence(self):
        """Test Phase 1: Dialectical Intelligence"""
        print("🧠 Testing Phase 1: Dialectical Intelligence...")
        
        # Test dialectical analysis
        analysis_request = {
            "content": "Looking for a better startup idea validation tool. Current solutions are too expensive.",
            "platforms": ["reddit"]
        }
        
        await self.test_endpoint(
            "POST", "/api/intelligence/dialectical-analysis", "Dialectical analysis", data=analysis_request
        )
        
        # Test authority rankings
        await self.test_endpoint("GET", "/api/intelligence/authority-rankings", "Authority rankings")
        
        # Test real-time synthesis
        await self.test_endpoint(
            "POST", "/api/intelligence/real-time-synthesis?content=test content&platform=reddit", 
            "Real-time synthesis"
        )
    
    async def test_streaming_pipeline(self):
        """Test Phase 2: Advanced Streaming Pipeline"""
        print("📡 Testing Phase 2: Advanced Streaming Pipeline...")
        
        # Test streaming stats
        await self.test_endpoint("GET", "/api/streaming/stats", "Streaming statistics")
        
        # Test advanced streaming start
        streaming_request = {
            "platforms": ["reddit"],
            "keywords": ["startup", "business"],
            "duration_minutes": 1
        }
        
        start_result = await self.test_endpoint(
            "POST", "/api/streaming/advanced/start", "Advanced streaming start", data=streaming_request
        )
        
        if start_result.get('task_id'):
            task_id = start_result['task_id']
            
            # Wait a moment for some data
            await asyncio.sleep(2)
            
            # Test temporal analysis
            await self.test_endpoint(
                "GET", "/api/streaming/temporal-analysis/reddit", "Temporal analysis"
            )
            
            # Test active trends
            await self.test_endpoint("GET", "/api/streaming/active-trends", "Active trends")
            
            # Stop the task
            await self.test_endpoint(
                "POST", f"/api/streaming/stop/{task_id}", "Stop streaming task"
            )
    
    async def test_semantic_intelligence(self):
        """Test Phase 3: Semantic Intelligence (NEW)"""
        print("🎯 Testing Phase 3: Semantic Intelligence...")
        
        # Test semantic analysis
        semantic_request = {
            "content": "Revolutionary AI platform for automating customer service. Huge market opportunity for SMBs.",
            "analysis_type": "comprehensive",
            "semantic_threshold": 0.6,
            "include_entities": True,
            "include_intent": True
        }
        
        await self.test_endpoint(
            "POST", "/api/semantic/analyze", "Semantic content analysis", data=semantic_request
        )
        
        # Test intent classification
        await self.test_endpoint(
            "POST", "/api/semantic/intent-classification?content=Need urgent solution for team collaboration",
            "Intent classification"
        )
        
        # Test semantic capabilities
        await self.test_endpoint("GET", "/api/semantic/capabilities", "Semantic capabilities")
        
        # Test semantic-temporal fusion
        fusion_request = {
            "platforms": ["reddit"],
            "keywords": ["startup", "business"],
            "semantic_threshold": 0.6,
            "temporal_window": "medium"
        }
        
        await self.test_endpoint(
            "POST", "/api/semantic/temporal-fusion", "Semantic-temporal fusion", data=fusion_request
        )
        
        # Test business insights
        await self.test_endpoint("GET", "/api/semantic/business-insights", "Semantic business insights")
    
    async def test_intelligence_engine(self):
        """Test intelligence engine"""
        print("🤖 Testing Intelligence Engine...")
        
        # Test content analysis
        analysis_request = {
            "content": "SaaS startup looking for product-market fit. Need better customer feedback analysis.",
            "platforms": ["reddit"],
            "analysis_type": "comprehensive"
        }
        
        await self.test_endpoint(
            "POST", "/api/intelligence/analyze", "Content analysis", data=analysis_request
        )
    
    async def test_chat_service(self):
        """Test chat service"""
        print("💬 Testing Chat Service...")
        
        if self.auth_token:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            chat_request = {
                "message": "What are the latest business opportunities in fintech?"
            }
            
            await self.test_endpoint(
                "POST", "/api/chat/message", "Chat message", data=chat_request, headers=headers
            )
    
    async def test_system_integration(self):
        """Test system integration capabilities"""
        print("🔄 Testing System Integration...")
        
        # Test overnight discovery status
        await self.test_endpoint("GET", "/api/discovery/overnight/status", "Overnight discovery status")
    
    async def test_performance_metrics(self):
        """Test performance and response times"""
        print("⚡ Testing Performance Metrics...")
        
        # Test rapid health checks
        start_time = time.time()
        for i in range(5):
            await self.test_endpoint("GET", "/api/health", f"Performance test {i+1}", silent=True)
        duration = time.time() - start_time
        
        avg_response_time = duration / 5
        self.test_results['test_details'].append({
            'test': 'Performance - Average Response Time',
            'result': 'PASS' if avg_response_time < 1.0 else 'FAIL',
            'details': f'Average response time: {avg_response_time:.3f}s (target: <1.0s)',
            'performance_metric': avg_response_time
        })
        
        if avg_response_time < 1.0:
            self.test_results['passed_tests'] += 1
        else:
            self.test_results['failed_tests'] += 1
        self.test_results['total_tests'] += 1
    
    async def test_endpoint(self, method: str, endpoint: str, description: str, 
                          data: Dict = None, headers: Dict = None, silent: bool = False) -> Dict:
        """Test individual endpoint"""
        if not silent:
            print(f"  Testing: {description}")
        
        self.test_results['total_tests'] += 1
        
        try:
            url = f"{self.base_url}{endpoint}"
            
            async with aiohttp.ClientSession() as session:
                if method == "GET":
                    async with session.get(url, headers=headers) as response:
                        result = await self._process_response(response, description)
                elif method == "POST":
                    async with session.post(url, json=data, headers=headers) as response:
                        result = await self._process_response(response, description)
                else:
                    raise Exception(f"Unsupported method: {method}")
            
            return result
            
        except Exception as e:
            if not silent:
                print(f"    ❌ FAIL: {str(e)}")
            
            self.test_results['failed_tests'] += 1
            self.test_results['test_details'].append({
                'test': description,
                'result': 'FAIL',
                'error': str(e),
                'endpoint': endpoint
            })
            return {}
    
    async def _process_response(self, response, description: str) -> Dict:
        """Process HTTP response"""
        status = response.status
        
        try:
            result = await response.json()
        except:
            result = {"text": await response.text()}
        
        if 200 <= status < 300:
            print(f"    ✅ PASS: HTTP {status}")
            self.test_results['passed_tests'] += 1
            self.test_results['test_details'].append({
                'test': description,
                'result': 'PASS',
                'status_code': status,
                'response_preview': str(result)[:200] + "..." if len(str(result)) > 200 else str(result)
            })
        else:
            print(f"    ❌ FAIL: HTTP {status}")
            self.test_results['failed_tests'] += 1
            self.test_results['test_details'].append({
                'test': description,
                'result': 'FAIL',
                'status_code': status,
                'error': result
            })
        
        return result
    
    async def generate_validation_report(self, duration: float):
        """Generate comprehensive validation report"""
        print("\n" + "=" * 60)
        print("📊 PHASE 3 COMPREHENSIVE VALIDATION REPORT")
        print("=" * 60)
        
        total = self.test_results['total_tests']
        passed = self.test_results['passed_tests']
        failed = self.test_results['failed_tests']
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"🎯 OVERALL RESULTS:")
        print(f"   Total Tests: {total}")
        print(f"   Passed: {passed}")
        print(f"   Failed: {failed}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Duration: {duration:.1f} seconds")
        print()
        
        # System Status Assessment
        if success_rate >= 90:
            status = "🟢 EXCELLENT - Production Ready"
        elif success_rate >= 80:
            status = "🟡 GOOD - Minor Issues"
        elif success_rate >= 70:
            status = "🟠 FAIR - Needs Attention"
        else:
            status = "🔴 POOR - Requires Fixes"
        
        print(f"🏆 SYSTEM STATUS: {status}")
        print()
        
        # Failed tests summary
        if failed > 0:
            print("❌ FAILED TESTS:")
            for test_detail in self.test_results['test_details']:
                if test_detail['result'] == 'FAIL':
                    print(f"   • {test_detail['test']}: {test_detail.get('error', 'Unknown error')}")
            print()
        
        # Save detailed report
        report_data = {
            'validation_timestamp': datetime.now().isoformat(),
            'system_version': 'Phase 3 Semantic Intelligence Enhanced',
            'summary': {
                'total_tests': total,
                'passed_tests': passed,
                'failed_tests': failed,
                'success_rate': success_rate,
                'duration_seconds': duration
            },
            'detailed_results': self.test_results['test_details']
        }
        
        with open('phase3_validation_report.json', 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"📄 Detailed report saved: phase3_validation_report.json")

async def main():
    """Main validation execution"""
    try:
        print("🎯 Starting Phase 3 Comprehensive Validation...")
        print("⚠️  Ensure Master API is running on http://localhost:8000")
        print()
        
        # Wait for user confirmation
        input("Press Enter when Master API is running...")
        
        validator = Phase3ComprehensiveValidator()
        await validator.run_comprehensive_validation()
        
    except KeyboardInterrupt:
        print("\n⚠️ Validation interrupted by user")
    except Exception as e:
        print(f"\n❌ Validation failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 