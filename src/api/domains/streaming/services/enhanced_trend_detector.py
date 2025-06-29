#!/usr/bin/env python3
"""
Enhanced Trend Detection Service with Advanced Signal Quality
Integrates the new signal quality enhancement system
"""

import asyncio
import logging
from typing import List, Dict
from datetime import datetime
from dataclasses import dataclass

# Import existing trend detection
from src.api.domains.streaming.services.trend_detection_service import (
    CrossPlatformTrendDetector, TrendOpportunity, TrendSignal
)

# Import new quality enhancement system
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../tools/analyzers'))
from signal_quality_enhancer import AdvancedSignalQualityEnhancer, EnhancedSignal

logger = logging.getLogger(__name__)

@dataclass
class PremiumTrendOpportunity:
    """Premium trend opportunity with enhanced quality metrics"""
    # Original opportunity data
    original_opportunity: TrendOpportunity
    
    # Enhanced quality metrics
    average_quality_score: float
    average_business_potential: float
    average_confidence_level: float
    pain_point_intensity: float
    solution_maturity: str
    market_timing_confidence: float
    
    # Business intelligence
    revenue_potential_signals: List[str]
    competitive_advantage_indicators: List[str]
    urgency_factors: List[str]
    technology_opportunities: List[str]
    
    # Quality assessment
    signal_quality_distribution: Dict[str, int]
    enhancement_report: Dict

class EnhancedTrendDetector:
    """Enhanced trend detector with advanced signal quality filtering"""
    
    def __init__(self):
        self.base_detector = CrossPlatformTrendDetector()
        self.quality_enhancer = AdvancedSignalQualityEnhancer()
        
        # Quality improvement settings
        self.quality_improvement_config = {
            'enable_advanced_filtering': True,
            'minimum_enhanced_quality': 0.75,
            'require_pain_point_clarity': True,
            'prioritize_business_potential': True,
            'boost_urgent_opportunities': True
        }
    
    async def detect_premium_trends(self, hours_back: int = 24) -> List[PremiumTrendOpportunity]:
        """
        Main enhanced trend detection pipeline
        Returns only premium, high-quality trend opportunities
        """
        
        logger.info(f"🚀 Starting premium trend detection with advanced quality filtering...")
        
        # Step 1: Collect raw signals using existing system
        logger.info("📡 Collecting raw signals from all platforms...")
        raw_opportunities = await self.base_detector.detect_cross_platform_trends(hours_back)
        
        if not raw_opportunities:
            logger.warning("No raw opportunities found")
            return []
        
        logger.info(f"   📊 Collected {len(raw_opportunities)} raw opportunities")
        
        # Step 2: Extract all signals for quality enhancement
        all_raw_signals = []
        for opportunity in raw_opportunities:
            all_raw_signals.extend(opportunity.signals)
        
        logger.info(f"   🔍 Analyzing {len(all_raw_signals)} individual signals for quality...")
        
        # Step 3: Apply advanced signal quality enhancement
        enhanced_signals, enhancement_report = await self._enhance_signal_quality(all_raw_signals)
        
        logger.info(f"   ✅ Quality enhancement complete:")
        logger.info(f"      🏆 High-quality signals retained: {len(enhanced_signals)}")
        logger.info(f"      📈 Quality improvement rate: {len(enhanced_signals)/len(all_raw_signals)*100:.1f}%")
        
        # Step 4: Rebuild opportunities with enhanced signals
        premium_opportunities = await self._rebuild_premium_opportunities(
            raw_opportunities, enhanced_signals, enhancement_report
        )
        
        # Step 5: Apply final quality filtering and ranking
        filtered_opportunities = self._apply_premium_filtering(premium_opportunities)
        
        logger.info(f"🎯 Premium trend detection complete:")
        logger.info(f"   📊 Premium opportunities identified: {len(filtered_opportunities)}")
        
        if filtered_opportunities:
            avg_quality = sum(op.average_quality_score for op in filtered_opportunities) / len(filtered_opportunities)
            avg_business_potential = sum(op.average_business_potential for op in filtered_opportunities) / len(filtered_opportunities)
            logger.info(f"   🏆 Average quality score: {avg_quality:.3f}")
            logger.info(f"   💰 Average business potential: {avg_business_potential:.3f}")
        
        return filtered_opportunities
    
    async def _enhance_signal_quality(self, raw_signals: List[TrendSignal]) -> tuple:
        """Apply advanced signal quality enhancement"""
        
        try:
            # Use the advanced quality enhancer
            enhanced_signals = await self.quality_enhancer.enhance_signals(raw_signals)
            enhancement_report = self.quality_enhancer.get_enhancement_report(enhanced_signals)
            
            logger.info(f"   🎯 Quality enhancement results:")
            if 'enhancement_summary' in enhancement_report:
                summary = enhancement_report['enhancement_summary']
                logger.info(f"      📊 Average quality score: {summary.get('avg_quality_score', 0):.3f}")
                logger.info(f"      💼 Average business potential: {summary.get('avg_business_potential', 0):.3f}")
                logger.info(f"      🎯 Average confidence level: {summary.get('avg_confidence_level', 0):.3f}")
            
            return enhanced_signals, enhancement_report
            
        except Exception as e:
            logger.error(f"Quality enhancement failed: {e}")
            # Fallback to original signals with basic filtering
            return [], {'error': str(e)}
    
    async def _rebuild_premium_opportunities(self, raw_opportunities: List[TrendOpportunity], 
                                           enhanced_signals: List[EnhancedSignal],
                                           enhancement_report: Dict) -> List[PremiumTrendOpportunity]:
        """Rebuild opportunities using enhanced signals"""
        
        premium_opportunities = []
        
        # Create mapping of original signals to enhanced signals
        enhanced_signal_map = {
            id(enhanced.original_signal): enhanced 
            for enhanced in enhanced_signals
        }
        
        for raw_opportunity in raw_opportunities:
            # Find enhanced signals for this opportunity
            opportunity_enhanced_signals = []
            
            for raw_signal in raw_opportunity.signals:
                signal_id = id(raw_signal)
                if signal_id in enhanced_signal_map:
                    opportunity_enhanced_signals.append(enhanced_signal_map[signal_id])
            
            # Only proceed if we have enhanced signals
            if not opportunity_enhanced_signals:
                continue
            
            # Calculate enhanced metrics
            enhanced_metrics = self._calculate_enhanced_metrics(opportunity_enhanced_signals)
            
            # Create premium opportunity
            premium_opportunity = PremiumTrendOpportunity(
                original_opportunity=raw_opportunity,
                average_quality_score=enhanced_metrics['avg_quality'],
                average_business_potential=enhanced_metrics['avg_business_potential'],
                average_confidence_level=enhanced_metrics['avg_confidence'],
                pain_point_intensity=enhanced_metrics['pain_intensity'],
                solution_maturity=enhanced_metrics['solution_maturity'],
                market_timing_confidence=enhanced_metrics['timing_confidence'],
                revenue_potential_signals=enhanced_metrics['revenue_signals'],
                competitive_advantage_indicators=enhanced_metrics['competitive_signals'],
                urgency_factors=enhanced_metrics['urgency_signals'],
                technology_opportunities=enhanced_metrics['tech_opportunities'],
                signal_quality_distribution=enhanced_metrics['quality_distribution'],
                enhancement_report=enhancement_report
            )
            
            premium_opportunities.append(premium_opportunity)
        
        return premium_opportunities
    
    def _calculate_enhanced_metrics(self, enhanced_signals: List[EnhancedSignal]) -> Dict:
        """Calculate enhanced metrics from enhanced signals"""
        
        if not enhanced_signals:
            return self._get_default_metrics()
        
        # Quality statistics
        quality_scores = [s.quality_score for s in enhanced_signals]
        business_potentials = [s.business_potential for s in enhanced_signals]
        confidence_levels = [s.confidence_level for s in enhanced_signals]
        urgency_scores = [s.urgency_score for s in enhanced_signals]
        
        # Pain point analysis
        all_pain_points = []
        for signal in enhanced_signals:
            all_pain_points.extend(signal.pain_point_indicators)
        
        pain_intensity = len([p for p in all_pain_points if 'intense_' in p]) / max(1, len(all_pain_points))
        
        # Solution maturity assessment
        solution_stages = [s.market_timing for s in enhanced_signals]
        solution_maturity = max(set(solution_stages), key=solution_stages.count) if solution_stages else 'emerging'
        
        # Business intelligence extraction
        revenue_signals = []
        competitive_signals = []
        urgency_signals = []
        tech_opportunities = []
        
        for signal in enhanced_signals:
            revenue_signals.extend(signal.market_size_signals)
            competitive_signals.extend(signal.competition_signals)
            if signal.urgency_score > 0.5:
                urgency_signals.extend([f"urgent_signal_{signal.urgency_score:.2f}"])
            if signal.technology_relevance > 0.3:
                tech_opportunities.extend(signal.semantic_keywords)
        
        # Quality distribution
        quality_distribution = {
            'high_quality': len([s for s in enhanced_signals if s.quality_score >= 0.8]),
            'medium_quality': len([s for s in enhanced_signals if 0.6 <= s.quality_score < 0.8]),
            'low_quality': len([s for s in enhanced_signals if s.quality_score < 0.6])
        }
        
        return {
            'avg_quality': sum(quality_scores) / len(quality_scores),
            'avg_business_potential': sum(business_potentials) / len(business_potentials),
            'avg_confidence': sum(confidence_levels) / len(confidence_levels),
            'pain_intensity': pain_intensity,
            'solution_maturity': solution_maturity,
            'timing_confidence': sum(quality_scores) / len(quality_scores),  # Simplified
            'revenue_signals': list(set(revenue_signals))[:5],  # Top 5 unique
            'competitive_signals': list(set(competitive_signals))[:5],
            'urgency_signals': list(set(urgency_signals))[:3],
            'tech_opportunities': list(set(tech_opportunities))[:10],
            'quality_distribution': quality_distribution
        }
    
    def _get_default_metrics(self) -> Dict:
        """Get default metrics when no enhanced signals available"""
        return {
            'avg_quality': 0.0,
            'avg_business_potential': 0.0,
            'avg_confidence': 0.0,
            'pain_intensity': 0.0,
            'solution_maturity': 'unknown',
            'timing_confidence': 0.0,
            'revenue_signals': [],
            'competitive_signals': [],
            'urgency_signals': [],
            'tech_opportunities': [],
            'quality_distribution': {'high_quality': 0, 'medium_quality': 0, 'low_quality': 0}
        }
    
    def _apply_premium_filtering(self, premium_opportunities: List[PremiumTrendOpportunity]) -> List[PremiumTrendOpportunity]:
        """Apply final premium quality filtering"""
        
        filtered_opportunities = []
        
        for opportunity in premium_opportunities:
            # Quality gate 1: Minimum quality score
            if opportunity.average_quality_score < self.quality_improvement_config['minimum_enhanced_quality']:
                continue
            
            # Quality gate 2: Business potential threshold
            if self.quality_improvement_config['prioritize_business_potential']:
                if opportunity.average_business_potential < 0.6:
                    continue
            
            # Quality gate 3: Pain point clarity requirement
            if self.quality_improvement_config['require_pain_point_clarity']:
                if opportunity.pain_point_intensity < 0.3:
                    continue
            
            # Quality gate 4: Confidence threshold
            if opportunity.average_confidence_level < 0.5:
                continue
            
            filtered_opportunities.append(opportunity)
        
        # Sort by composite score (quality × business potential × confidence)
        filtered_opportunities.sort(
            key=lambda x: (
                x.average_quality_score * 
                x.average_business_potential * 
                x.average_confidence_level *
                (1.2 if len(x.urgency_factors) > 0 else 1.0)  # Boost urgent opportunities
            ),
            reverse=True
        )
        
        return filtered_opportunities
    
    def get_quality_improvement_report(self, premium_opportunities: List[PremiumTrendOpportunity]) -> Dict:
        """Generate comprehensive quality improvement report"""
        
        if not premium_opportunities:
            return {'error': 'No premium opportunities to analyze'}
        
        # Overall statistics
        total_opportunities = len(premium_opportunities)
        avg_quality = sum(op.average_quality_score for op in premium_opportunities) / total_opportunities
        avg_business_potential = sum(op.average_business_potential for op in premium_opportunities) / total_opportunities
        avg_confidence = sum(op.average_confidence_level for op in premium_opportunities) / total_opportunities
        
        # Solution maturity distribution
        solution_maturity_dist = {}
        for op in premium_opportunities:
            maturity = op.solution_maturity
            solution_maturity_dist[maturity] = solution_maturity_dist.get(maturity, 0) + 1
        
        # Business intelligence summary
        all_revenue_signals = []
        all_tech_opportunities = []
        urgent_opportunities = 0
        
        for op in premium_opportunities:
            all_revenue_signals.extend(op.revenue_potential_signals)
            all_tech_opportunities.extend(op.technology_opportunities)
            if len(op.urgency_factors) > 0:
                urgent_opportunities += 1
        
        return {
            'quality_improvement_summary': {
                'total_premium_opportunities': total_opportunities,
                'average_quality_score': avg_quality,
                'average_business_potential': avg_business_potential,
                'average_confidence_level': avg_confidence,
                'urgent_opportunities': urgent_opportunities,
                'urgent_opportunities_percentage': urgent_opportunities / total_opportunities * 100
            },
            'solution_maturity_distribution': solution_maturity_dist,
            'business_intelligence': {
                'revenue_signals_detected': len(set(all_revenue_signals)),
                'technology_opportunities': len(set(all_tech_opportunities)),
                'top_revenue_signals': list(set(all_revenue_signals))[:10],
                'top_tech_opportunities': list(set(all_tech_opportunities))[:10]
            },
            'quality_gates_applied': self.quality_improvement_config,
            'recommendations': self._generate_quality_recommendations(premium_opportunities)
        }
    
    def _generate_quality_recommendations(self, premium_opportunities: List[PremiumTrendOpportunity]) -> List[str]:
        """Generate quality improvement recommendations"""
        
        recommendations = []
        
        if not premium_opportunities:
            return ["No premium opportunities found - consider lowering quality thresholds"]
        
        avg_quality = sum(op.average_quality_score for op in premium_opportunities) / len(premium_opportunities)
        avg_business_potential = sum(op.average_business_potential for op in premium_opportunities) / len(premium_opportunities)
        
        if avg_quality < 0.8:
            recommendations.append("Consider raising data source quality standards - average quality below optimal")
        
        if avg_business_potential < 0.7:
            recommendations.append("Focus on higher business potential opportunities - current pipeline may be too technical")
        
        urgent_count = sum(1 for op in premium_opportunities if len(op.urgency_factors) > 0)
        if urgent_count / len(premium_opportunities) > 0.5:
            recommendations.append("High urgency signal detected - prioritize rapid development/validation")
        
        early_stage_count = sum(1 for op in premium_opportunities if op.solution_maturity == 'early')
        if early_stage_count / len(premium_opportunities) > 0.6:
            recommendations.append("Many early-stage opportunities - ideal for first-mover advantage")
        
        return recommendations

# Utility function for easy integration
async def detect_premium_trends(hours_back: int = 24) -> tuple:
    """
    Main function for premium trend detection
    Returns premium opportunities and quality report
    """
    detector = EnhancedTrendDetector()
    premium_opportunities = await detector.detect_premium_trends(hours_back)
    quality_report = detector.get_quality_improvement_report(premium_opportunities)
    
    return premium_opportunities, quality_report 