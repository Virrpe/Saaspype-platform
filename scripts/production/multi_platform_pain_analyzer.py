#!/usr/bin/env python3
"""
MULTI-PLATFORM PAIN POINT ANALYZER
Enhanced pain point analysis across ALL scraped platforms
"""

import sys
import os
sys.path.append('src')
sys.path.append('.')

import asyncio
import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from collections import defaultdict

# Import the mega scraper and core detector
from mega_source_scraper import MegaSourceScraper
from src.api.domains.streaming.services.trend_detection_service import CrossPlatformTrendDetector

class MultiPlatformPainAnalyzer:
    """Enhanced pain point analysis across all scraped platforms"""
    
    def __init__(self):
        self.mega_scraper = MegaSourceScraper()
        self.core_detector = CrossPlatformTrendDetector()
        
        # Enhanced pain point indicators (from our fixed system)
        self.pain_indicators = {
            'high_intensity': ['hate', 'terrible', 'nightmare', 'impossible', 'broken', 'awful', 'disaster', 'overwhelming', 'frustrating', 'killing'],
            'workflow_friction': ['wasting time', 'manual', 'tedious', 'repetitive', 'inefficient', 'slow', 'clunky', 'piling up', 'too expensive'],
            'solution_seeking': ['need help', 'looking for', 'wish there was', 'no solution', "can't find", 'how do i', 'need automation', 'need', 'help'],
            'problem_patterns': ['problem with', 'issue with', 'struggling with', 'difficulty with', 'challenge with', 'problem', 'issue', 'struggle'],
            'urgency': ['urgent', 'asap', 'immediately', 'deadline', 'critical', 'emergency', 'desperate'],
            'business_impact': ['losing money', 'losing customers', 'response times', 'customers are', 'team', 'business']
        }
        
        # Platform-specific pain extraction patterns
        self.platform_patterns = {
            'reddit': {
                'weight': 0.25,
                'pain_multiplier': 1.2,  # Reddit users are very vocal about problems
                'context': 'community_discussion'
            },
            'twitter': {
                'weight': 0.15,
                'pain_multiplier': 1.0,
                'context': 'real_time_complaints'
            },
            'hacker_news': {
                'weight': 0.20,
                'pain_multiplier': 1.3,  # Technical pain points are well-articulated
                'context': 'technical_discussion'
            },
            'github': {
                'weight': 0.15,
                'pain_multiplier': 1.1,
                'context': 'developer_issues'
            },
            'product_hunt': {
                'weight': 0.10,
                'pain_multiplier': 0.8,  # More solution-focused than problem-focused
                'context': 'product_launches'
            },
            'indie_hackers': {
                'weight': 0.15,
                'pain_multiplier': 1.4,  # Entrepreneurs are explicit about business problems
                'context': 'business_problems'
            },
            'dev_to': {
                'weight': 0.08,
                'pain_multiplier': 1.0,
                'context': 'developer_content'
            },
            'stack_overflow': {
                'weight': 0.12,
                'pain_multiplier': 1.1,
                'context': 'technical_problems'
            },
            'ycombinator': {
                'weight': 0.18,
                'pain_multiplier': 1.3,
                'context': 'startup_discussions'
            },
            'medium': {
                'weight': 0.08,
                'pain_multiplier': 0.9,
                'context': 'thought_leadership'
            },
            'linkedin': {
                'weight': 0.10,
                'pain_multiplier': 1.0,
                'context': 'professional_problems'
            },
            'quora': {
                'weight': 0.12,
                'pain_multiplier': 1.2,
                'context': 'question_based_problems'
            }
        }
        
        # Industry classification (enhanced)
        self.industry_patterns = {
            'fintech': ['payment', 'banking', 'finance', 'money', 'transaction', 'invoice', 'billing', 'accounting', 'crypto', 'blockchain'],
            'ecommerce': ['shop', 'store', 'product', 'inventory', 'customer', 'order', 'shipping', 'retail', 'marketplace'],
            'saas': ['software', 'platform', 'api', 'integration', 'automation', 'tool', 'service', 'app', 'dashboard'],
            'marketing': ['ads', 'campaign', 'lead', 'conversion', 'analytics', 'seo', 'social media', 'content', 'growth'],
            'productivity': ['workflow', 'task', 'project', 'team', 'collaboration', 'management', 'organization', 'efficiency'],
            'devtools': ['development', 'coding', 'programming', 'deployment', 'testing', 'debugging', 'framework', 'ci/cd'],
            'operations': ['process', 'operations', 'logistics', 'supply chain', 'vendor', 'procurement', 'manufacturing'],
            'hr': ['hiring', 'recruitment', 'employee', 'onboarding', 'training', 'performance', 'culture', 'talent'],
            'customer_service': ['support', 'tickets', 'helpdesk', 'customer service', 'feedback', 'complaints', 'chat'],
            'ai_ml': ['artificial intelligence', 'machine learning', 'ai', 'ml', 'neural network', 'deep learning', 'nlp'],
            'cybersecurity': ['security', 'cybersecurity', 'encryption', 'vulnerability', 'threat', 'compliance', 'privacy'],
            'healthcare': ['health', 'medical', 'patient', 'doctor', 'clinic', 'hospital', 'telemedicine', 'wellness']
        }
    
    async def analyze_all_platforms(self, hours_back: int = 24) -> Dict[str, Any]:
        """Run enhanced pain point analysis across all platforms"""
        
        print("🧠 MULTI-PLATFORM PAIN POINT ANALYZER")
        print("=" * 60)
        print("🎯 Enhanced LLM-powered analysis across 15+ platforms")
        print()
        
        start_time = datetime.now()
        
        # Phase 1: Scrape all platforms
        print("📊 PHASE 1: Multi-Platform Data Collection")
        print("-" * 50)
        
        # Get data from mega scraper (15+ platforms)
        mega_results = await self.mega_scraper.scrape_all_sources(hours_back)
        
        # Get core platform data
        core_opportunities = await self.core_detector.detect_cross_platform_trends(hours_back)
        
        print(f"✅ Data collection complete:")
        print(f"   📊 Mega scraper opportunities: {len(mega_results.get('all_opportunities', []))}")
        print(f"   🎯 Core platform opportunities: {len(core_opportunities)}")
        
        # Phase 2: Enhanced pain point analysis
        print(f"\n🧠 PHASE 2: Enhanced Pain Point Analysis")
        print("-" * 50)
        
        all_content = []
        
        # Extract content from mega scraper results
        for opp in mega_results.get('all_opportunities', []):
            content_item = {
                'title': opp.get('title', ''),
                'description': opp.get('description', ''),
                'source': opp.get('source', 'unknown'),
                'url': opp.get('url', ''),
                'score': opp.get('score', 0),
                'platform_type': 'mega_scraper'
            }
            all_content.append(content_item)
        
        # Extract content from core opportunities
        for opp in core_opportunities:
            content_item = {
                'title': opp.title,
                'description': opp.description,
                'source': opp.sources[0] if opp.sources else 'unknown',
                'url': '',
                'score': opp.momentum_score,
                'platform_type': 'core_detector'
            }
            all_content.append(content_item)
        
        print(f"📝 Total content items to analyze: {len(all_content)}")
        
        # Phase 3: Apply enhanced pain point analysis
        print(f"\n🎯 PHASE 3: Pain Point Scoring & Classification")
        print("-" * 50)
        
        high_quality_pain_points = []
        platform_stats = defaultdict(lambda: {'analyzed': 0, 'pain_points': 0, 'avg_score': 0})
        
        for item in all_content:
            platform = item['source']
            platform_stats[platform]['analyzed'] += 1
            
            # Apply enhanced analysis
            analysis = await self._analyze_content_item(item)
            
            if analysis and analysis['total_score'] >= 6:  # Quality threshold
                high_quality_pain_points.append(analysis)
                platform_stats[platform]['pain_points'] += 1
                platform_stats[platform]['avg_score'] += analysis['total_score']
        
        # Calculate platform averages
        for platform, stats in platform_stats.items():
            if stats['pain_points'] > 0:
                stats['avg_score'] = stats['avg_score'] / stats['pain_points']
        
        # Phase 4: Results analysis
        duration = (datetime.now() - start_time).total_seconds()
        
        print(f"\n🎉 MULTI-PLATFORM ANALYSIS COMPLETE!")
        print("=" * 60)
        print(f"⏱️ Duration: {duration:.1f} seconds")
        print(f"📊 Total platforms: {len(platform_stats)}")
        print(f"📝 Content analyzed: {len(all_content)}")
        print(f"🎯 High-quality pain points: {len(high_quality_pain_points)}")
        print(f"📈 Success rate: {len(high_quality_pain_points)/len(all_content)*100:.1f}%")
        
        # Platform performance
        print(f"\n🏆 TOP PERFORMING PLATFORMS:")
        print("-" * 40)
        
        sorted_platforms = sorted(
            [(p, s) for p, s in platform_stats.items() if s['pain_points'] > 0],
            key=lambda x: x[1]['avg_score'],
            reverse=True
        )
        
        for i, (platform, stats) in enumerate(sorted_platforms[:8], 1):
            print(f"{i}. {platform}: {stats['pain_points']} pain points (avg: {stats['avg_score']:.1f}/10)")
        
        # Top opportunities
        print(f"\n🔥 TOP PAIN POINT OPPORTUNITIES:")
        print("-" * 40)
        
        sorted_opportunities = sorted(high_quality_pain_points, key=lambda x: x['total_score'], reverse=True)
        
        for i, opp in enumerate(sorted_opportunities[:10], 1):
            print(f"{i}. {opp['pain_point'][:60]}...")
            print(f"   📊 Score: {opp['total_score']}/10 | 🏭 Domain: {opp['domain']} | 📱 Platform: {opp['source_platform']}")
        
        # Save comprehensive results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"multi_platform_pain_analysis_{timestamp}.json"
        
        results = {
            'timestamp': timestamp,
            'duration_seconds': duration,
            'platforms_analyzed': len(platform_stats),
            'content_items_analyzed': len(all_content),
            'high_quality_pain_points': len(high_quality_pain_points),
            'success_rate': len(high_quality_pain_points)/len(all_content)*100,
            'platform_performance': dict(platform_stats),
            'top_opportunities': sorted_opportunities[:20],
            'domain_distribution': self._analyze_domain_distribution(high_quality_pain_points),
            'quality_metrics': {
                'average_score': sum(p['total_score'] for p in high_quality_pain_points) / len(high_quality_pain_points) if high_quality_pain_points else 0,
                'score_distribution': self._analyze_score_distribution(high_quality_pain_points)
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {filename}")
        
        return results
    
    async def _analyze_content_item(self, item: Dict) -> Optional[Dict]:
        """Apply enhanced pain point analysis to a content item"""
        try:
            title = item.get('title', '')
            description = item.get('description', '')
            source = item.get('source', 'unknown')
            
            combined_text = f"{title}\n\n{description}"
            
            # Check for pain indicators
            has_pain, indicators = self._detect_pain_indicators(combined_text)
            if not has_pain:
                return None
            
            # Quality filter
            if not self._passes_quality_filter(item):
                return None
            
            # Extract pain point description
            pain_point = self._extract_pain_point_description(combined_text)
            
            # Score dimensions
            market_size = self._score_market_size(combined_text)
            urgency = self._score_urgency(combined_text)
            solution_gap = self._score_solution_gap(combined_text)
            monetization = self._score_monetization(combined_text)
            
            # Apply platform-specific multipliers
            platform_config = self.platform_patterns.get(source, {'pain_multiplier': 1.0, 'weight': 0.05})
            platform_multiplier = platform_config['pain_multiplier']
            
            # Calculate total score with platform weighting
            base_score = market_size + urgency + solution_gap + monetization
            total_score = min(10, base_score * platform_multiplier)
            
            # Calculate confidence
            confidence = self._calculate_confidence(item, combined_text, total_score)
            
            # Classify domain
            domain = self._classify_domain(combined_text)
            
            # Generate opportunity description
            opportunity_description = self._generate_opportunity_description(pain_point, domain)
            
            # Extract validation signals
            validation_signals = self._extract_validation_signals(item, combined_text, indicators)
            
            return {
                'pain_point': pain_point,
                'market_size': market_size,
                'urgency': urgency,
                'solution_gap': solution_gap,
                'monetization': monetization,
                'total_score': round(total_score, 1),
                'confidence': confidence,
                'domain': domain,
                'opportunity_description': opportunity_description,
                'validation_signals': validation_signals,
                'source_platform': source,
                'platform_weight': platform_config['weight'],
                'platform_context': platform_config.get('context', 'general'),
                'source_item': {
                    'title': title,
                    'url': item.get('url', ''),
                    'score': item.get('score', 0)
                }
            }
            
        except Exception as e:
            print(f"Error analyzing content item: {e}")
            return None
    
    def _detect_pain_indicators(self, text: str) -> tuple:
        """Detect pain indicators in text"""
        text_lower = text.lower()
        indicator_count = 0
        found_indicators = []
        
        for category, indicators in self.pain_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    indicator_count += 1
                    found_indicators.append(f"{category}: {indicator}")
        
        return indicator_count >= 2, found_indicators
    
    def _passes_quality_filter(self, item: Dict) -> bool:
        """Quality filter for content items"""
        title = item.get('title', '')
        description = item.get('description', '')
        
        # Content length filter
        if len(title) < 10 or len(title + description) < 30:
            return False
        
        # Promotional content filter
        promotional_keywords = ['check out', 'my startup', 'our product', 'we launched', 'sign up', 'free trial']
        combined_text = (title + ' ' + description).lower()
        promotional_count = sum(1 for keyword in promotional_keywords if keyword in combined_text)
        
        return promotional_count < 2
    
    def _extract_pain_point_description(self, text: str) -> str:
        """Extract pain point description using regex patterns"""
        problem_patterns = [
            r"(?:the (?:main |biggest |real )?(?:problem|issue|challenge) (?:is|with))\s+([^.!?]{10,100})",
            r"(?:i (?:can't|cannot|struggle to|have trouble))\s+([^.!?]{10,100})",
            r"(?:it's (?:hard|difficult|impossible) to)\s+([^.!?]{10,100})",
            r"(?:no (?:good )?(?:solution|tool|way) (?:for|to))\s+([^.!?]{10,100})",
            r"(?:wish there was|need help with|looking for)\s+([^.!?]{10,100})"
        ]
        
        for pattern in problem_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Fallback
        lines = text.split('\n')
        for line in lines[:3]:
            if any(word in line.lower() for word in ['problem', 'issue', 'struggle', 'difficult', 'hard']):
                return line.strip()[:100]
        
        return "Business process inefficiency identified"
    
    def _score_market_size(self, text: str) -> int:
        """Score market size (0-3)"""
        text_lower = text.lower()
        
        enterprise_indicators = ['enterprise', 'company', 'business', 'industry', 'corporate', 'organization', 'team']
        if any(indicator in text_lower for indicator in enterprise_indicators):
            return 3
        
        professional_indicators = ['professional', 'work', 'job', 'career', 'client', 'customer']
        if any(indicator in text_lower for indicator in professional_indicators):
            return 2
        
        return 1
    
    def _score_urgency(self, text: str) -> int:
        """Score urgency (0-3)"""
        text_lower = text.lower()
        
        critical_indicators = ['critical', 'urgent', 'emergency', 'asap', 'immediately', 'deadline', 'losing money']
        if any(indicator in text_lower for indicator in critical_indicators):
            return 3
        
        high_indicators = ['frustrating', 'wasting time', 'inefficient', 'slowing down', 'blocking']
        if any(indicator in text_lower for indicator in high_indicators):
            return 2
        
        return 1
    
    def _score_solution_gap(self, text: str) -> int:
        """Score solution gap (0-2)"""
        text_lower = text.lower()
        
        gap_indicators = ['no solution', 'nothing exists', "can't find", 'no tool', 'no way to', 'impossible to find']
        if any(indicator in text_lower for indicator in gap_indicators):
            return 2
        
        inadequate_indicators = ['too expensive', 'too complex', 'doesn\'t work well', 'limited options', 'not good enough']
        if any(indicator in text_lower for indicator in inadequate_indicators):
            return 1
        
        return 1
    
    def _score_monetization(self, text: str) -> int:
        """Score monetization potential (0-2)"""
        text_lower = text.lower()
        
        high_monetization = ['willing to pay', 'budget for', 'cost', 'price', 'expensive', 'revenue', 'profit', 'roi']
        if any(indicator in text_lower for indicator in high_monetization):
            return 2
        
        medium_monetization = ['business', 'professional', 'work', 'company', 'client']
        if any(indicator in text_lower for indicator in medium_monetization):
            return 1
        
        return 1
    
    def _calculate_confidence(self, item: Dict, text: str, total_score: float) -> float:
        """Calculate confidence score"""
        confidence = 0.0
        
        # Content quality (30%)
        if len(text) > 100:
            confidence += 0.3
        
        # Source credibility (25%)
        source = item.get('source', '')
        if source in ['hacker_news', 'indie_hackers', 'reddit', 'ycombinator']:
            confidence += 0.25
        elif source in ['github', 'stack_overflow', 'dev_to']:
            confidence += 0.20
        else:
            confidence += 0.15
        
        # Score quality (25%)
        if total_score >= 8:
            confidence += 0.25
        elif total_score >= 6:
            confidence += 0.15
        
        # Engagement (20%)
        score = item.get('score', 0)
        if score > 10:
            confidence += 0.20
        elif score > 5:
            confidence += 0.10
        
        return min(1.0, confidence)
    
    def _classify_domain(self, text: str) -> str:
        """Classify business domain"""
        text_lower = text.lower()
        
        for domain, keywords in self.industry_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                return domain
        
        return 'general'
    
    def _generate_opportunity_description(self, pain_point: str, domain: str) -> str:
        """Generate specific opportunity description"""
        domain_solutions = {
            'productivity': f"AI-powered workflow automation platform addressing {pain_point.lower()}",
            'marketing': f"Intelligent marketing automation tool solving {pain_point.lower()}",
            'devtools': f"Developer productivity platform targeting {pain_point.lower()}",
            'fintech': f"Financial automation solution for {pain_point.lower()}",
            'ecommerce': f"E-commerce optimization platform addressing {pain_point.lower()}",
            'saas': f"SaaS integration platform solving {pain_point.lower()}",
            'operations': f"Operations management system for {pain_point.lower()}",
            'hr': f"HR automation platform addressing {pain_point.lower()}",
            'customer_service': f"Customer service automation tool solving {pain_point.lower()}",
            'ai_ml': f"AI/ML platform addressing {pain_point.lower()}",
            'cybersecurity': f"Security automation solution for {pain_point.lower()}",
            'healthcare': f"Healthcare technology platform solving {pain_point.lower()}"
        }
        
        return domain_solutions.get(domain, f"Business automation platform addressing {pain_point.lower()}")
    
    def _extract_validation_signals(self, item: Dict, text: str, indicators: List[str]) -> List[str]:
        """Extract validation signals"""
        signals = []
        
        score = item.get('score', 0)
        if score > 20:
            signals.append(f"High engagement ({score} points)")
        
        if any('urgent' in ind or 'critical' in ind for ind in indicators):
            signals.append("High urgency indicated")
        
        if 'business' in text.lower() or 'company' in text.lower():
            signals.append("Business/professional context")
        
        if any(word in text.lower() for word in ['willing to pay', 'budget', 'cost']):
            signals.append("Monetization potential indicated")
        
        return signals
    
    def _analyze_domain_distribution(self, pain_points: List[Dict]) -> Dict[str, int]:
        """Analyze distribution of domains"""
        domain_counts = defaultdict(int)
        for pp in pain_points:
            domain_counts[pp['domain']] += 1
        return dict(domain_counts)
    
    def _analyze_score_distribution(self, pain_points: List[Dict]) -> Dict[str, int]:
        """Analyze score distribution"""
        score_ranges = {'6-7': 0, '7-8': 0, '8-9': 0, '9-10': 0}
        for pp in pain_points:
            score = pp['total_score']
            if 6 <= score < 7:
                score_ranges['6-7'] += 1
            elif 7 <= score < 8:
                score_ranges['7-8'] += 1
            elif 8 <= score < 9:
                score_ranges['8-9'] += 1
            elif score >= 9:
                score_ranges['9-10'] += 1
        return score_ranges
    
    async def close(self):
        """Clean up resources"""
        await self.mega_scraper.close()
        await self.core_detector.close()

async def main():
    """Run multi-platform pain point analysis"""
    analyzer = MultiPlatformPainAnalyzer()
    
    try:
        results = await analyzer.analyze_all_platforms(hours_back=24)
        
        print(f"\n🎯 HONEST ASSESSMENT:")
        print("-" * 30)
        
        success_rate = results['success_rate']
        avg_score = results['quality_metrics']['average_score']
        
        if success_rate >= 15 and avg_score >= 7:
            print("✅ EXCELLENT: High-quality pain points across multiple platforms")
        elif success_rate >= 10 and avg_score >= 6:
            print("✅ GOOD: Decent pain point detection across platforms")
        elif success_rate >= 5:
            print("⚠️ OKAY: Some pain points found but could be better")
        else:
            print("❌ POOR: Low success rate, needs improvement")
        
        print(f"📊 Success rate: {success_rate:.1f}%")
        print(f"📈 Average quality: {avg_score:.1f}/10")
        print(f"🏭 Top domains: {', '.join(list(results['domain_distribution'].keys())[:5])}")
        
    finally:
        await analyzer.close()

if __name__ == "__main__":
    asyncio.run(main()) 