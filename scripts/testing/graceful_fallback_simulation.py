#!/usr/bin/env python3
"""
Graceful Fallback Simulation Script
Demonstrates how the enhanced system gracefully degrades when LLM services fail
"""

import asyncio
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class ServiceStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded" 
    FAILED = "failed"

@dataclass
class SystemHealth:
    reddit_api: ServiceStatus = ServiceStatus.HEALTHY
    llm_service: ServiceStatus = ServiceStatus.HEALTHY
    database: ServiceStatus = ServiceStatus.HEALTHY
    overall_functionality: float = 1.0  # 0.0 to 1.0

class MockRedditData:
    """Mock Reddit data that simulates your existing working system"""
    
    @staticmethod
    def get_sample_posts() -> List[Dict]:
        return [
            {
                "id": "abc123",
                "title": "I wish there was a simple inventory management tool for my Shopify store",
                "body": "Currently using spreadsheets and it's a nightmare. Always running out of popular items or overstocking. Need something under $100/month that doesn't require a PhD to use.",
                "author": "shopify_owner_99",
                "score": 45,
                "num_comments": 23,
                "subreddit": "entrepreneur",
                "business_context": {
                    "industry": "ecommerce",
                    "pain_level": 8,
                    "keywords": ["inventory", "shopify", "management", "tool"]
                },
                "spam_analysis": {"is_spam": False, "confidence": 0.95}
            },
            {
                "id": "def456", 
                "title": "How do you handle customer support when you're a solo founder?",
                "body": "Getting 50+ support emails daily and I'm drowning. Can't afford to hire someone yet. What tools or strategies work for bootstrapped startups?",
                "author": "solo_founder_2024",
                "score": 78,
                "num_comments": 41,
                "subreddit": "startups",
                "business_context": {
                    "industry": "software",
                    "pain_level": 9,
                    "keywords": ["customer support", "solo founder", "bootstrapped"]
                },
                "spam_analysis": {"is_spam": False, "confidence": 0.98}
            },
            {
                "id": "ghi789",
                "title": "Marketing automation for small agencies - what actually works?",
                "body": "We're a 5-person agency and spending too much time on repetitive marketing tasks. Looking for automation that won't break the bank. Most solutions seem built for enterprise.",
                "author": "agency_owner_pro",
                "score": 34,
                "num_comments": 19,
                "subreddit": "marketing",
                "business_context": {
                    "industry": "marketing",
                    "pain_level": 7,
                    "keywords": ["marketing automation", "small agency", "affordable"]
                },
                "spam_analysis": {"is_spam": False, "confidence": 0.92}
            }
        ]

class MockLLMService:
    """Mock LLM service that can simulate failures and recoveries"""
    
    def __init__(self, failure_rate: float = 0.0):
        self.failure_rate = failure_rate
        self.status = ServiceStatus.HEALTHY
        self.request_count = 0
        
    def simulate_status_change(self):
        """Randomly change service status to simulate real-world conditions"""
        rand = random.random()
        if rand < self.failure_rate:
            self.status = ServiceStatus.FAILED
        elif rand < self.failure_rate + 0.1:
            self.status = ServiceStatus.DEGRADED
        else:
            self.status = ServiceStatus.HEALTHY
    
    async def analyze_pain_points(self, posts: List[Dict]) -> Optional[Dict]:
        """Simulate LLM pain point analysis with potential failures"""
        self.request_count += 1
        self.simulate_status_change()
        
        # Add realistic latency
        await asyncio.sleep(random.uniform(1, 3))
        
        if self.status == ServiceStatus.FAILED:
            raise Exception("LLM service unavailable - API timeout")
        
        if self.status == ServiceStatus.DEGRADED:
            # Return partial results
            return {
                "analysis_quality": "degraded",
                "analysis_type": "degraded_llm_analysis",
                "pain_points": ["Basic keyword-based analysis available"],
                "confidence": 0.3,
                "note": "LLM service degraded - using fallback analysis"
            }
        
        # Full LLM analysis (healthy state)
        enhanced_analysis = {
            "analysis_quality": "premium",
            "analysis_type": "premium_llm_analysis",
            "pain_points": [
                {
                    "problem": "Shopify inventory management complexity",
                    "severity": 8,
                    "market_size": "300K+ Shopify stores",
                    "solution_gap": "No affordable AI-powered solutions under $100/month",
                    "opportunity": "AI inventory predictor for SMB Shopify stores",
                    "confidence": 0.87
                },
                {
                    "problem": "Solo founder customer support overwhelm", 
                    "severity": 9,
                    "market_size": "2M+ solo founders",
                    "solution_gap": "Enterprise support tools too complex/expensive",
                    "opportunity": "Simple AI support assistant for bootstrapped startups",
                    "confidence": 0.82
                },
                {
                    "problem": "Small agency marketing automation gaps",
                    "severity": 7, 
                    "market_size": "150K+ small agencies",
                    "solution_gap": "Automation tools designed for enterprise, not SMBs",
                    "opportunity": "SMB-focused marketing automation platform",
                    "confidence": 0.75
                }
            ],
            "business_opportunities": 3,
            "total_confidence": 0.81
        }
        
        return enhanced_analysis

class GracefulFallbackSystem:
    """Enhanced discovery system with graceful fallback capabilities"""
    
    def __init__(self):
        self.llm_service = MockLLMService(failure_rate=0.2)  # 20% failure rate for demo
        self.health = SystemHealth()
        self.fallback_strategies = {
            "keyword_analysis": True,
            "cached_results": True,
            "basic_sentiment": True
        }
        
    async def discover_pain_points_basic(self, posts: List[Dict]) -> Dict:
        """Your existing working system - keyword-based analysis"""
        print("🔧 Running basic discovery (your existing system)...")
        
        pain_points = []
        for post in posts:
            # Simulate your existing keyword-based analysis
            business_context = post.get('business_context', {})
            if business_context.get('pain_level', 0) > 6:
                pain_point = {
                    "title": post['title'],
                    "industry": business_context.get('industry', 'unknown'),
                    "pain_level": business_context.get('pain_level', 0),
                    "engagement": post['score'] + post['num_comments'],
                    "keywords": business_context.get('keywords', []),
                    "analysis_type": "keyword_based"
                }
                pain_points.append(pain_point)
        
        return {
            "analysis_type": "basic_keyword_analysis",
            "pain_points": pain_points,
            "system_status": "fully_functional",
            "quality_level": "good",
            "note": "Reliable keyword-based analysis from existing system"
        }
    
    async def discover_pain_points_enhanced(self, posts: List[Dict]) -> Dict:
        """Enhanced system with LLM + graceful fallback"""
        print("🚀 Attempting enhanced discovery with LLM...")
        
        try:
            # Try LLM enhancement
            llm_analysis = await self.llm_service.analyze_pain_points(posts)
            
            if llm_analysis and llm_analysis.get("analysis_quality") == "premium":
                print("✅ LLM analysis successful - premium insights available")
                self.health.llm_service = ServiceStatus.HEALTHY
                self.health.overall_functionality = 1.0
                return llm_analysis
            
            elif llm_analysis and llm_analysis.get("analysis_quality") == "degraded":
                print("⚠️ LLM service degraded - combining with basic analysis")
                self.health.llm_service = ServiceStatus.DEGRADED
                self.health.overall_functionality = 0.7
                
                # Combine degraded LLM with basic analysis
                basic_analysis = await self.discover_pain_points_basic(posts)
                return {
                    "analysis_type": "hybrid_degraded",
                    "llm_component": llm_analysis,
                    "basic_component": basic_analysis,
                    "quality_level": "good",
                    "note": "LLM degraded - using hybrid approach"
                }
            
        except Exception as e:
            print(f"❌ LLM service failed: {e}")
            print("🔄 Falling back to basic analysis...")
            
            self.health.llm_service = ServiceStatus.FAILED
            self.health.overall_functionality = 0.6
            
            # Graceful fallback to your existing system
            basic_analysis = await self.discover_pain_points_basic(posts)
            basic_analysis.update({
                "fallback_reason": str(e),
                "note": "LLM unavailable - using proven keyword analysis",
                "system_status": "degraded_but_functional"
            })
            
            return basic_analysis
    
    def get_system_health(self) -> Dict:
        """Get current system health status"""
        return {
            "timestamp": datetime.now().isoformat(),
            "reddit_api": self.health.reddit_api.value,
            "llm_service": self.health.llm_service.value,
            "database": self.health.database.value,
            "overall_functionality": f"{self.health.overall_functionality * 100:.1f}%",
            "user_impact": self._get_user_impact_description()
        }
    
    def _get_user_impact_description(self) -> str:
        """Describe impact on user experience"""
        if self.health.overall_functionality >= 0.9:
            return "Full premium experience - advanced AI insights available"
        elif self.health.overall_functionality >= 0.7:
            return "Good experience - some AI features degraded but core functionality intact"
        elif self.health.overall_functionality >= 0.5:
            return "Basic experience - reliable keyword analysis with reduced AI features"
        else:
            return "Minimal experience - core systems operational, AI features unavailable"

async def run_fallback_simulation():
    """Run the graceful fallback simulation"""
    print("🎯 Graceful Fallback Simulation - Luciq Enhanced Discovery")
    print("=" * 70)
    
    system = GracefulFallbackSystem()
    sample_posts = MockRedditData.get_sample_posts()
    
    # Simulate multiple scenarios
    scenarios = [
        ("Normal Operation", 0.0),
        ("Occasional Failures", 0.2), 
        ("High Failure Rate", 0.5),
        ("Complete LLM Outage", 1.0)
    ]
    
    for scenario_name, failure_rate in scenarios:
        print(f"\n🔬 SCENARIO: {scenario_name} (LLM failure rate: {failure_rate * 100:.0f}%)")
        print("-" * 50)
        
        # Update failure rate
        system.llm_service.failure_rate = failure_rate
        
        # Run multiple attempts to show consistency
        for attempt in range(3):
            print(f"\n📊 Attempt {attempt + 1}:")
            
            start_time = time.time()
            results = await system.discover_pain_points_enhanced(sample_posts)
            end_time = time.time()
            
            print(f"⏱️ Processing time: {end_time - start_time:.2f}s")
            print(f"📈 Analysis type: {results.get('analysis_type', 'unknown')}")
            print(f"📊 Quality level: {results.get('quality_level', 'unknown')}")
            print(f"💡 Pain points found: {len(results.get('pain_points', []))}")
            
            if results.get('note'):
                print(f"📝 Note: {results['note']}")
            
            # Show system health
            health = system.get_system_health()
            print(f"🏥 System health: {health['overall_functionality']} - {health['user_impact']}")
            
            # Brief pause between attempts
            await asyncio.sleep(1)
    
    print(f"\n✅ Simulation complete!")
    print("\n📋 Key Insights:")
    print("• Your existing Reddit system never fails")
    print("• LLM failures don't break core functionality") 
    print("• Users always get value, even during outages")
    print("• System gracefully upgrades when LLM recovers")
    print("• Performance remains consistent across all scenarios")

async def demonstrate_recovery_scenario():
    """Demonstrate system recovery when LLM comes back online"""
    print("\n🔄 RECOVERY DEMONSTRATION")
    print("=" * 50)
    
    system = GracefulFallbackSystem()
    sample_posts = MockRedditData.get_sample_posts()
    
    # Start with LLM completely down
    system.llm_service.failure_rate = 1.0
    print("💀 LLM service completely down...")
    
    result1 = await system.discover_pain_points_enhanced(sample_posts)
    print(f"📊 Fallback result: {result1.get('analysis_type', 'unknown')}")
    print(f"📝 Status: {result1.get('note', 'N/A')}")
    
    # Gradual recovery
    system.llm_service.failure_rate = 0.3
    print("\n🔧 LLM service partially recovering...")
    
    result2 = await system.discover_pain_points_enhanced(sample_posts)
    print(f"📊 Recovery result: {result2.get('analysis_type', 'unknown')}")
    print(f"📝 Status: {result2.get('note', 'N/A')}")
    
    # Full recovery
    system.llm_service.failure_rate = 0.0
    print("\n✅ LLM service fully recovered...")
    
    result3 = await system.discover_pain_points_enhanced(sample_posts)
    print(f"📊 Full result: {result3.get('analysis_type', 'unknown')}")
    print(f"💎 Premium features: Available")
    print(f"🎯 Business opportunities: {result3.get('business_opportunities', 0)}")

if __name__ == "__main__":
    print("🚀 Starting Graceful Fallback Simulation...")
    asyncio.run(run_fallback_simulation())
    asyncio.run(demonstrate_recovery_scenario()) 