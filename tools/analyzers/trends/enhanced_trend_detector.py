#!/usr/bin/env python3
"""
Enhanced Trend Detector - Integration with Signal Quality Enhancement System
Provides premium trend detection with quality filtering and business intelligence
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from signal_quality_enhancer import AdvancedSignalQualityEnhancer, EnhancedSignal

logger = logging.getLogger(__name__)

class EnhancedTrendDetector:
    """
    Enhanced trend detection system that integrates quality enhancement
    with trend analysis for premium business intelligence
    """
    
    def __init__(self):
        self.quality_enhancer = AdvancedSignalQualityEnhancer()
        self.trend_cache = {}
        self.last_analysis = None
        
        # Premium quality thresholds for trend detection
        self.premium_thresholds = {
            'minimum_overall_quality': 0.75,
            'minimum_business_relevance': 0.7,
            'minimum_trend_strength': 0.6,
            'minimum_signals_for_trend': 3
        }
        
        logger.info("Enhanced Trend Detector initialized with premium quality filtering")
    
    async def detect_premium_trends(self, 
                                   hours_back: int = 24,
                                   quality_threshold: float = 0.75,
                                   max_trends: int = 10) -> Dict[str, Any]:
        """
        Detect premium trends using quality-enhanced signals
        
        Args:
            hours_back: Hours of historical data to analyze
            quality_threshold: Minimum quality score for trend inclusion
            max_trends: Maximum number of trends to return
            
        Returns:
            Dict containing premium trends with quality metrics
        """
        try:
            # Simulate signal collection (in real implementation, this would fetch from data sources)
            raw_signals = await self._collect_recent_signals(hours_back)
            
            # Apply quality enhancement
            enhanced_signals = await self.quality_enhancer.enhance_signals(raw_signals)
            
            # Filter for premium quality
            premium_signals = [
                signal for signal in enhanced_signals 
                if signal.quality_score >= quality_threshold
            ]
            
            # Detect trends from premium signals
            trends = await self._analyze_trends(premium_signals)
            
            # Rank and filter trends
            premium_trends = self._rank_trends(trends, max_trends)
            
            analysis_result = {
                'premium_trends': premium_trends,
                'quality_metrics': {
                    'total_signals_analyzed': len(raw_signals),
                    'premium_signals_retained': len(premium_signals),
                    'quality_improvement_rate': f"{len(premium_signals)/len(raw_signals)*100:.1f}%",
                    'trends_detected': len(premium_trends),
                    'analysis_timestamp': datetime.now().isoformat()
                },
                'trend_insights': self._generate_trend_insights(premium_trends),
                'business_intelligence': self._extract_business_intelligence(premium_signals)
            }
            
            self.last_analysis = analysis_result
            return analysis_result
            
        except Exception as e:
            logger.error(f"Premium trend detection failed: {e}")
            return {
                'error': f"Trend detection failed: {str(e)}",
                'fallback_data': self._get_fallback_trends()
            }
    
    async def _collect_recent_signals(self, hours_back: int) -> List[Any]:
        """
        Simulate collecting recent signals from various sources
        In production, this would interface with real data streams
        """
        # Mock signal data for demonstration
        import random
        
        signals = []
        current_time = datetime.now()
        
        # Generate diverse signal types
        signal_templates = [
            {
                'content': 'Looking for better {solution} to replace {current_tool}. Need {feature} and costs less than ${budget}.',
                'keywords': ['solution', 'replace', 'need', 'costs'],
                'signal_type': 'pain_point'
            },
            {
                'content': 'Building {product} for {market}. Early traction with {metric} users.',
                'keywords': ['building', 'traction', 'users'],
                'signal_type': 'solution_building'
            },
            {
                'content': 'Market opportunity in {industry} - growing demand for {technology}.',
                'keywords': ['opportunity', 'growing', 'demand'],
                'signal_type': 'market_trend'
            }
        ]
        
        for i in range(hours_back * 10):  # ~10 signals per hour
            template = random.choice(signal_templates)
            
            # Fill template with realistic data
            content = template['content'].format(
                solution=random.choice(['CRM', 'analytics tool', 'automation platform']),
                current_tool=random.choice(['Excel', 'manual process', 'legacy system']),
                feature=random.choice(['real-time sync', 'better UI', 'API access']),
                budget=random.choice(['100', '500', '1000']),
                product=random.choice(['SaaS platform', 'mobile app', 'API service']),
                market=random.choice(['small businesses', 'enterprises', 'startups']),
                metric=random.choice(['100', '500', '1K']),
                industry=random.choice(['fintech', 'healthtech', 'edtech']),
                technology=random.choice(['AI automation', 'real-time analytics', 'workflow tools'])
            )
            
            class MockSignal:
                def __init__(self, content, signal_type, timestamp):
                    self.content = content
                    self.source = random.choice(['reddit', 'twitter', 'github', 'hackernews'])
                    self.engagement_score = random.uniform(20, 95)
                    self.timestamp = timestamp
                    self.signal_type = signal_type
                    self.credibility_weight = random.uniform(0.6, 0.9)
            
            signal_time = current_time - timedelta(hours=random.uniform(0, hours_back))
            signals.append(MockSignal(content, template['signal_type'], signal_time))
        
        return signals
    
    async def _analyze_trends(self, enhanced_signals: List[EnhancedSignal]) -> List[Dict[str, Any]]:
        """
        Analyze enhanced signals to identify trending patterns
        """
        trends = []
        
        # Group signals by semantic themes
        trend_groups = self._group_signals_by_theme(enhanced_signals)
        
        for theme, signals in trend_groups.items():
            if len(signals) >= self.premium_thresholds['minimum_signals_for_trend']:
                trend_strength = self._calculate_trend_strength(signals)
                
                if trend_strength >= self.premium_thresholds['minimum_trend_strength']:
                    trend = {
                        'theme': theme,
                        'signal_count': len(signals),
                        'trend_strength': trend_strength,
                        'business_potential': sum(s.business_potential for s in signals) / len(signals),
                        'quality_score': sum(s.quality_score for s in signals) / len(signals),
                        'market_timing': self._analyze_market_timing(signals),
                        'key_insights': self._extract_key_insights(signals),
                        'representative_signals': [s.original_signal.content[:100] + '...' for s in signals[:3]]
                    }
                    trends.append(trend)
        
        return trends
    
    def _group_signals_by_theme(self, signals: List[EnhancedSignal]) -> Dict[str, List[EnhancedSignal]]:
        """
        Group signals by semantic themes using keywords and content analysis
        """
        themes = {}
        
        for signal in signals:
            # Use semantic keywords to determine theme
            primary_theme = self._determine_primary_theme(signal)
            
            if primary_theme not in themes:
                themes[primary_theme] = []
            themes[primary_theme].append(signal)
        
        return themes
    
    def _determine_primary_theme(self, signal: EnhancedSignal) -> str:
        """
        Determine the primary theme of a signal based on semantic analysis
        """
        content = signal.original_signal.content.lower()
        keywords = signal.semantic_keywords
        
        # Theme classification based on keywords and content
        if any(word in content for word in ['automation', 'automate', 'workflow']):
            return 'Workflow Automation'
        elif any(word in content for word in ['analytics', 'dashboard', 'reporting']):
            return 'Data Analytics'
        elif any(word in content for word in ['crm', 'customer', 'sales']):
            return 'Customer Management'
        elif any(word in content for word in ['api', 'integration', 'platform']):
            return 'Platform Integration'
        elif any(word in content for word in ['mobile', 'app', 'ios', 'android']):
            return 'Mobile Solutions'
        else:
            # Use most prominent semantic keyword as theme
            return keywords[0] if keywords else 'General Business'
    
    def _calculate_trend_strength(self, signals: List[EnhancedSignal]) -> float:
        """
        Calculate trend strength based on signal quality and engagement
        """
        if not signals:
            return 0.0
        
        # Weighted average of quality score, business potential, and engagement
        total_weight = 0
        weighted_sum = 0
        
        for signal in signals:
            engagement_factor = min(signal.original_signal.engagement_score / 100, 1.0)
            weight = engagement_factor * signal.credibility_weight
            
            signal_strength = (
                signal.quality_score * 0.4 +
                signal.business_potential * 0.4 +
                signal.confidence_level * 0.2
            )
            
            weighted_sum += signal_strength * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def _analyze_market_timing(self, signals: List[EnhancedSignal]) -> Dict[str, Any]:
        """
        Analyze market timing based on signal patterns
        """
        timing_indicators = [s.market_timing for s in signals]
        
        timing_distribution = {}
        for timing in timing_indicators:
            timing_distribution[timing] = timing_distribution.get(timing, 0) + 1
        
        dominant_timing = max(timing_distribution.keys(), key=lambda x: timing_distribution[x])
        
        return {
            'dominant_phase': dominant_timing,
            'distribution': timing_distribution,
            'confidence': timing_distribution[dominant_timing] / len(signals)
        }
    
    def _extract_key_insights(self, signals: List[EnhancedSignal]) -> List[str]:
        """
        Extract key insights from signal patterns
        """
        insights = []
        
        # Pain point analysis
        all_pain_points = []
        for signal in signals:
            all_pain_points.extend(signal.pain_point_indicators)
        
        if all_pain_points:
            most_common_pain = max(set(all_pain_points), key=all_pain_points.count)
            insights.append(f"Primary pain point: {most_common_pain}")
        
        # Solution analysis
        all_solutions = []
        for signal in signals:
            all_solutions.extend(signal.solution_indicators)
        
        if all_solutions:
            most_common_solution = max(set(all_solutions), key=all_solutions.count)
            insights.append(f"Trending solution: {most_common_solution}")
        
        # Business opportunity
        avg_business_potential = sum(s.business_potential for s in signals) / len(signals)
        if avg_business_potential > 0.7:
            insights.append("High commercial potential detected")
        elif avg_business_potential > 0.5:
            insights.append("Moderate commercial potential")
        
        return insights
    
    def _rank_trends(self, trends: List[Dict[str, Any]], max_trends: int) -> List[Dict[str, Any]]:
        """
        Rank and filter trends by business value
        """
        # Sort by combined score of trend strength and business potential
        ranked_trends = sorted(
            trends,
            key=lambda x: x['trend_strength'] * 0.6 + x['business_potential'] * 0.4,
            reverse=True
        )
        
        return ranked_trends[:max_trends]
    
    def _generate_trend_insights(self, trends: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate high-level insights from detected trends
        """
        if not trends:
            return {'message': 'No significant trends detected in current timeframe'}
        
        insights = {
            'top_opportunity': trends[0]['theme'] if trends else None,
            'emerging_markets': [t['theme'] for t in trends if t.get('market_timing', {}).get('dominant_phase') == 'early'],
            'high_potential_areas': [t['theme'] for t in trends if t['business_potential'] > 0.8],
            'trend_summary': f"{len(trends)} premium trends detected with quality-enhanced analysis"
        }
        
        return insights
    
    def _extract_business_intelligence(self, signals: List[EnhancedSignal]) -> Dict[str, Any]:
        """
        Extract business intelligence from quality-enhanced signals
        """
        if not signals:
            return {}
        
        # Calculate aggregate metrics
        avg_quality = sum(s.quality_score for s in signals) / len(signals)
        avg_business_potential = sum(s.business_potential for s in signals) / len(signals)
        avg_confidence = sum(s.confidence_level for s in signals) / len(signals)
        
        # Extract industry insights
        all_keywords = []
        for signal in signals:
            all_keywords.extend(signal.semantic_keywords)
        
        keyword_frequency = {}
        for keyword in all_keywords:
            keyword_frequency[keyword] = keyword_frequency.get(keyword, 0) + 1
        
        top_keywords = sorted(keyword_frequency.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'signal_quality_metrics': {
                'average_quality': avg_quality,
                'average_business_potential': avg_business_potential,
                'average_confidence': avg_confidence
            },
            'market_intelligence': {
                'top_keywords': dict(top_keywords),
                'signal_volume': len(signals),
                'high_quality_percentage': len([s for s in signals if s.quality_score > 0.8]) / len(signals) * 100
            }
        }
    
    def _get_fallback_trends(self) -> Dict[str, Any]:
        """
        Provide fallback trend data when analysis fails
        """
        return {
            'fallback': True,
            'message': 'Using cached trend data',
            'basic_trends': [
                {'theme': 'Workflow Automation', 'strength': 0.7},
                {'theme': 'Data Analytics', 'strength': 0.6},
                {'theme': 'API Integration', 'strength': 0.5}
            ]
        }
    
    def get_detection_status(self) -> Dict[str, Any]:
        """
        Get current status of the trend detection system
        """
        return {
            'system_status': 'operational',
            'quality_enhancer_available': True,
            'last_analysis': self.last_analysis['quality_metrics'] if self.last_analysis else None,
            'premium_thresholds': self.premium_thresholds,
            'cache_size': len(self.trend_cache)
        }

# Convenience function for direct usage
async def detect_trends_with_quality_enhancement(hours_back: int = 24, 
                                               quality_threshold: float = 0.75) -> Dict[str, Any]:
    """
    Convenience function to detect trends with quality enhancement
    """
    detector = EnhancedTrendDetector()
    return await detector.detect_premium_trends(hours_back, quality_threshold)

if __name__ == "__main__":
    # Test the enhanced trend detector
    async def test_detector():
        detector = EnhancedTrendDetector()
        results = await detector.detect_premium_trends(hours_back=12, quality_threshold=0.5)
        print("Enhanced Trend Detection Results:")
        print(f"Premium trends detected: {len(results.get('premium_trends', []))}")
        print(f"Quality metrics: {results.get('quality_metrics', {})}")
        
    asyncio.run(test_detector()) 