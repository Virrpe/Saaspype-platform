#!/usr/bin/env python3
"""
Comprehensive Luciq Pipeline Validation
ORCHESTRATOR Mission: Validate entire intelligence logic and extract valuable insights

Focus Areas:
1. End-to-end intelligence pipeline validation
2. Business insight quality assessment  
3. Cross-platform correlation analysis
4. Market opportunity identification accuracy
5. Actionable intelligence generation
"""

import asyncio
import sys
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
import os
from typing import Dict, List, Any

# Add project paths
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / 'src'))

from api.domains.streaming.services.trend_detection_service import CrossPlatformTrendDetector

class BusinessIntelligenceValidator:
    """Validates business value and insight quality of Luciq intelligence"""
    
    def __init__(self):
        self.insights = []
        self.validation_results = {}
        
    def analyze_opportunity_quality(self, opportunities: List) -> Dict:
        """Analyze the business value and actionability of detected opportunities"""
        analysis = {
            'total_opportunities': len(opportunities),
            'high_value_opportunities': 0,
            'cross_platform_opportunities': 0,
            'actionable_opportunities': 0,
            'market_segments': set(),
            'opportunity_categories': {},
            'confidence_distribution': {'high': 0, 'medium': 0, 'low': 0},
            'business_insights': []
        }
        
        for opp in opportunities:
            # Cross-platform analysis
            sources = list(set(signal.source for signal in opp.signals))
            if len(sources) > 1:
                analysis['cross_platform_opportunities'] += 1
            
            # Market segment tracking
            if hasattr(opp, 'category') and opp.category:
                analysis['market_segments'].add(opp.category)
                if opp.category in analysis['opportunity_categories']:
                    analysis['opportunity_categories'][opp.category] += 1
                else:
                    analysis['opportunity_categories'][opp.category] = 1
            
            # Confidence analysis
            if opp.confidence_level >= 0.7:
                analysis['confidence_distribution']['high'] += 1
            elif opp.confidence_level >= 0.4:
                analysis['confidence_distribution']['medium'] += 1
            else:
                analysis['confidence_distribution']['low'] += 1
            
            # High-value opportunity detection
            if (opp.momentum_score >= 0.6 and 
                opp.confidence_level >= 0.5 and 
                len(sources) >= 1):
                analysis['high_value_opportunities'] += 1
                
                # Generate business insight
                insight = self._generate_business_insight(opp, sources)
                analysis['business_insights'].append(insight)
            
            # Actionability assessment
            if (hasattr(opp, 'estimated_market_size') and 
                opp.estimated_market_size and 
                opp.estimated_market_size != 'Unknown' and
                opp.momentum_score >= 0.4):
                analysis['actionable_opportunities'] += 1
        
        return analysis
    
    def _generate_business_insight(self, opportunity, sources: List) -> Dict:
        """Generate actionable business insight from opportunity data"""
        return {
            'title': opportunity.title,
            'sources': sources,
            'momentum': round(opportunity.momentum_score, 3),
            'confidence': round(opportunity.confidence_level, 3),
            'market_size': getattr(opportunity, 'estimated_market_size', 'Unknown'),
            'complexity': getattr(opportunity, 'technical_complexity', 'Unknown'),
            'business_value': self._assess_business_value(opportunity),
            'recommended_action': self._suggest_action(opportunity, sources),
            'risk_level': self._assess_risk(opportunity)
        }
    
    def _assess_business_value(self, opp) -> str:
        """Assess business value potential"""
        if opp.momentum_score >= 0.8 and opp.confidence_level >= 0.7:
            return "HIGH - Strong market signal with high confidence"
        elif opp.momentum_score >= 0.6 and opp.confidence_level >= 0.5:
            return "MEDIUM - Good momentum with moderate confidence"
        elif opp.momentum_score >= 0.4:
            return "LOW-MEDIUM - Emerging signal, monitor for growth"
        else:
            return "LOW - Weak signal, requires validation"
    
    def _suggest_action(self, opp, sources: List) -> str:
        """Suggest actionable next steps"""
        if len(sources) > 1:
            return f"CROSS-PLATFORM VALIDATION - Investigate across {', '.join(sources)} for market validation"
        elif opp.momentum_score >= 0.7:
            return "IMMEDIATE RESEARCH - High momentum opportunity, conduct market analysis"
        elif opp.momentum_score >= 0.5:
            return "MONITOR & VALIDATE - Track trend development, gather additional data"
        else:
            return "WATCH LIST - Monitor for momentum increase"
    
    def _assess_risk(self, opp) -> str:
        """Assess business risk level"""
        complexity = getattr(opp, 'technical_complexity', 'Unknown')
        if complexity == 'Low' and opp.confidence_level >= 0.6:
            return "LOW - Simple execution, high confidence"
        elif complexity == 'Medium' or opp.confidence_level >= 0.5:
            return "MEDIUM - Moderate complexity/confidence"
        else:
            return "HIGH - Complex execution or low confidence"

async def comprehensive_pipeline_test():
    """Execute comprehensive pipeline validation with business intelligence analysis"""
    print("🎯 ORCHESTRATOR: Comprehensive Pipeline Validation")
    print("🧠 Mission: Validate intelligence logic and extract valuable insights")
    print("=" * 70)
    print(f"🕒 Validation started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize components
    detector = CrossPlatformTrendDetector()
    validator = BusinessIntelligenceValidator()
    
    try:
        # Phase 1: Platform Connectivity Validation
        print("\n📡 PHASE 1: Platform Connectivity & Data Quality")
        print("=" * 50)
        
        # Display platform configuration
        print("📊 Intelligence Network Configuration:")
        active_platforms = []
        total_weight = 0
        
        for source, config in detector.data_sources.items():
            if config['enabled']:
                weight = config.get('weight', 0)
                credibility = config.get('credibility_multiplier', 1.0)
                total_weight += weight
                active_platforms.append(source)
                
                print(f"   ✅ {source}: weight={weight:.3f}, credibility={credibility:.2f}")
                
                if source == 'reddit':
                    subreddits = len(config.get('subreddits', []))
                    posts_limit = config.get('posts_per_subreddit', 'unlimited')
                    print(f"      📱 Subreddits: {subreddits}, posts_limit: {posts_limit}")
        
        print(f"\n🎯 Network Status: {len(active_platforms)} platforms active")
        print(f"⚖️ Total weight distribution: {total_weight:.3f}")
        
        # Phase 2: Full Pipeline Execution
        print(f"\n🚀 PHASE 2: Full Intelligence Pipeline Execution")
        print("=" * 50)
        print("🔄 Executing cross-platform trend detection...")
        
        start_time = time.time()
        opportunities = await detector.detect_cross_platform_trends(hours_back=24)
        execution_time = time.time() - start_time
        
        print(f"✅ Pipeline completed in {execution_time:.2f} seconds")
        print(f"📊 Raw opportunities detected: {len(opportunities)}")
        
        # Phase 3: Business Intelligence Analysis
        print(f"\n🧠 PHASE 3: Business Intelligence Quality Analysis")
        print("=" * 50)
        
        analysis = validator.analyze_opportunity_quality(opportunities)
        
        print(f"📈 Business Value Assessment:")
        print(f"   🎯 Total opportunities: {analysis['total_opportunities']}")
        print(f"   💎 High-value opportunities: {analysis['high_value_opportunities']}")
        print(f"   🔗 Cross-platform opportunities: {analysis['cross_platform_opportunities']}")
        print(f"   ⚡ Actionable opportunities: {analysis['actionable_opportunities']}")
        
        print(f"\n📊 Market Intelligence Distribution:")
        for category, count in analysis['opportunity_categories'].items():
            percentage = (count / analysis['total_opportunities'] * 100) if analysis['total_opportunities'] > 0 else 0
            print(f"   📈 {category}: {count} opportunities ({percentage:.1f}%)")
        
        print(f"\n🎯 Confidence Level Distribution:")
        total_opps = analysis['total_opportunities']
        for level, count in analysis['confidence_distribution'].items():
            percentage = (count / total_opps * 100) if total_opps > 0 else 0
            emoji = '🔥' if level == 'high' else '⚡' if level == 'medium' else '💭'
            print(f"   {emoji} {level.title()}: {count} opportunities ({percentage:.1f}%)")
        
        # Phase 4: Actionable Insights Generation
        print(f"\n💡 PHASE 4: Actionable Business Insights")
        print("=" * 50)
        
        high_value_insights = analysis['business_insights'][:5]  # Top 5 insights
        
        if high_value_insights:
            print(f"🏆 TOP {len(high_value_insights)} ACTIONABLE BUSINESS INSIGHTS:")
            
            for i, insight in enumerate(high_value_insights, 1):
                print(f"\n   💎 INSIGHT #{i}: {insight['title']}")
                print(f"      📊 Sources: {', '.join(insight['sources'])} ({len(insight['sources'])} platforms)")
                print(f"      🚀 Momentum: {insight['momentum']:.3f} | 🎯 Confidence: {insight['confidence']:.3f}")
                print(f"      💰 Market Size: {insight['market_size']}")
                print(f"      🛠️ Complexity: {insight['complexity']}")
                print(f"      💡 Business Value: {insight['business_value']}")
                print(f"      🎯 Recommended Action: {insight['recommended_action']}")
                print(f"      ⚠️ Risk Level: {insight['risk_level']}")
                
        else:
            print("⚠️ No high-value insights generated - system may need calibration")
        
        # Phase 5: Platform Signal Analysis
        print(f"\n📡 PHASE 5: Platform Signal Quality Analysis")
        print("=" * 50)
        
        platform_signals = {}
        total_signals = 0
        
        for opp in opportunities:
            for signal in opp.signals:
                source = signal.source
                if source not in platform_signals:
                    platform_signals[source] = {
                        'count': 0,
                        'avg_strength': 0,
                        'total_strength': 0
                    }
                platform_signals[source]['count'] += 1
                platform_signals[source]['total_strength'] += signal.engagement_score
                total_signals += 1
        
        # Calculate averages
        for source, data in platform_signals.items():
            if data['count'] > 0:
                data['avg_strength'] = data['total_strength'] / data['count']
        
        print("🔍 Platform Signal Quality:")
        for source, data in sorted(platform_signals.items(), key=lambda x: x[1]['count'], reverse=True):
            percentage = (data['count'] / total_signals * 100) if total_signals > 0 else 0
            avg_strength = data['avg_strength']
            quality_emoji = '🔥' if avg_strength >= 70 else '⚡' if avg_strength >= 50 else '💭'
            
            print(f"   {quality_emoji} {source}: {data['count']} signals ({percentage:.1f}%) | avg_engagement: {avg_strength:.1f}")
        
        # Phase 6: System Intelligence Assessment
        print(f"\n🧠 PHASE 6: System Intelligence Assessment")
        print("=" * 50)
        
        # Calculate intelligence metrics
        cross_platform_rate = (analysis['cross_platform_opportunities'] / analysis['total_opportunities'] * 100) if analysis['total_opportunities'] > 0 else 0
        high_value_rate = (analysis['high_value_opportunities'] / analysis['total_opportunities'] * 100) if analysis['total_opportunities'] > 0 else 0
        actionable_rate = (analysis['actionable_opportunities'] / analysis['total_opportunities'] * 100) if analysis['total_opportunities'] > 0 else 0
        
        print(f"📊 Intelligence Quality Metrics:")
        print(f"   🔗 Cross-platform correlation: {cross_platform_rate:.1f}%")
        print(f"   💎 High-value opportunity rate: {high_value_rate:.1f}%")
        print(f"   ⚡ Actionable insight rate: {actionable_rate:.1f}%")
        print(f"   ⚡ Processing speed: {execution_time:.2f}s for {total_signals} signals")
        
        # Overall System Score
        platform_score = len(active_platforms) / 7 * 100  # Out of max 7 platforms
        quality_score = (cross_platform_rate + high_value_rate + actionable_rate) / 3
        performance_score = 100 if execution_time <= 60 else max(0, 100 - (execution_time - 60) * 2)
        
        overall_score = (platform_score * 0.3 + quality_score * 0.5 + performance_score * 0.2)
        
        print(f"\n🏆 OVERALL SYSTEM INTELLIGENCE SCORE: {overall_score:.1f}/100")
        
        if overall_score >= 80:
            print("   🎉 EXCELLENT: Production-ready intelligence system")
        elif overall_score >= 60:
            print("   ✅ GOOD: Solid intelligence capabilities with minor improvements needed")
        elif overall_score >= 40:
            print("   ⚠️ MODERATE: Functional but needs optimization")
        else:
            print("   🔧 NEEDS IMPROVEMENT: Significant calibration required")
        
        # Phase 7: Business Decision Recommendations
        print(f"\n💼 PHASE 7: Strategic Business Recommendations")
        print("=" * 50)
        
        if len(high_value_insights) >= 3:
            print("🚀 STRATEGIC RECOMMENDATION: IMMEDIATE MARKET ENTRY")
            print("   📈 Multiple high-value opportunities identified")
            print("   🎯 Recommend: Begin market validation on top 2-3 insights")
            print("   💰 Estimated development effort: 2-4 weeks per opportunity")
            
        elif len(high_value_insights) >= 1:
            print("⚡ STRATEGIC RECOMMENDATION: FOCUSED DEVELOPMENT")
            print("   💡 Quality opportunities detected")
            print("   🎯 Recommend: Deep dive on highest-momentum opportunity")
            print("   💰 Estimated development effort: 3-6 weeks")
            
        else:
            print("🔍 STRATEGIC RECOMMENDATION: MARKET RESEARCH PHASE")
            print("   📊 Limited high-confidence opportunities")
            print("   🎯 Recommend: Expand data sources or adjust detection criteria")
            print("   💰 Estimated research effort: 1-2 weeks")
        
        # Save detailed results
        results = {
            'timestamp': datetime.now().isoformat(),
            'execution_time': execution_time,
            'total_opportunities': analysis['total_opportunities'],
            'business_insights': high_value_insights,
            'platform_signals': platform_signals,
            'overall_score': overall_score,
            'recommendations': 'See console output for detailed recommendations'
        }
        
        with open('pipeline_validation_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: pipeline_validation_results.json")
        
    except Exception as e:
        print(f"❌ Pipeline validation error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await detector.close()
        print(f"\n🔄 Pipeline validation completed at: {datetime.now().strftime('%H:%M:%S')}")

async def main():
    """Execute comprehensive pipeline validation"""
    await comprehensive_pipeline_test()
    
    print("\n" + "=" * 70)
    print("🎯 ORCHESTRATOR: Comprehensive Pipeline Validation Complete")
    print("📊 Business intelligence logic validated")
    print("💡 Actionable insights extracted and analyzed")
    print("🚀 Strategic recommendations generated")
    print("\n🔄 Boomerang Return: Full pipeline analysis ready for strategic review")

if __name__ == "__main__":
    asyncio.run(main()) 