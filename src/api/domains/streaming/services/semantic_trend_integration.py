#!/usr/bin/env python3
"""
Semantic Trend Integration Service - Phase 2 Implementation
Integrates Advanced Semantic Understanding and Temporal Pattern Recognition
with existing Phase 1 foundation for 3x accuracy improvement
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import numpy as np

# Import Phase 1 foundation services
from src.api.domains.streaming.services.trend_detection_service import CrossPlatformTrendDetector, TrendSignal, TrendOpportunity
from src.api.domains.intelligence.services.cross_platform_intelligence import CrossPlatformIntelligenceEngine
from src.api.domains.credibility.services.source_credibility_engine import get_credibility_engine
from tools.validators.real_data_validator import GroundbreakingDataValidator

# Import Phase 2 advanced engines
from src.api.domains.intelligence.services.semantic_analysis_engine import get_semantic_engine, SemanticScore
from src.api.domains.streaming.services.temporal_pattern_engine import get_temporal_engine, TemporalPattern, TrendEmergenceSignal

logger = logging.getLogger(__name__)

@dataclass
class EnhancedTrendSignal:
    """Enhanced trend signal with semantic and temporal analysis"""
    # Original signal data
    original_signal: TrendSignal
    
    # Phase 2 enhancements
    semantic_score: SemanticScore
    temporal_patterns: List[TemporalPattern] = field(default_factory=list)
    emergence_signals: List[TrendEmergenceSignal] = field(default_factory=list)
    
    # Enhanced metrics
    enhanced_confidence: float = 0.0
    semantic_relevance: float = 0.0
    temporal_momentum: float = 0.0
    innovation_score: float = 0.0
    
    # Integration metadata
    processing_time: float = 0.0
    enhancement_version: str = "phase_2_v1.0"

@dataclass
class IntelligentTrendOpportunity:
    """Intelligent trend opportunity with semantic understanding and temporal analysis"""
    # Original opportunity data
    original_opportunity: TrendOpportunity
    
    # Phase 2 intelligence enhancements
    semantic_analysis: Dict = field(default_factory=dict)
    temporal_analysis: Dict = field(default_factory=dict)
    emergence_prediction: Dict = field(default_factory=dict)
    
    # Enhanced scoring
    intelligence_score: float = 0.0      # Overall intelligence-enhanced score
    semantic_relevance: float = 0.0      # Business context relevance
    temporal_momentum: float = 0.0       # Time-based momentum
    innovation_potential: float = 0.0    # Innovation and disruption potential
    market_timing_score: float = 0.0     # Optimal market timing assessment
    
    # Predictive insights
    emergence_probability: float = 0.0   # Probability of trend emergence
    growth_trajectory: str = "unknown"   # Expected growth pattern
    optimal_entry_timing: str = "unknown" # Best time to act on opportunity
    risk_factors: List[str] = field(default_factory=list)
    
    # Context understanding
    business_context: List[str] = field(default_factory=list)
    market_indicators: List[str] = field(default_factory=list)
    competitive_insights: Dict = field(default_factory=dict)

class SemanticTrendIntegrationEngine:
    """Revolutionary trend detection with semantic understanding and temporal intelligence"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("🧠⏰ Initializing Semantic Trend Integration Engine...")
        
        # Initialize Phase 1 foundation services
        self.trend_detector = CrossPlatformTrendDetector()
        self.intelligence_engine = CrossPlatformIntelligenceEngine()
        self.credibility_engine = get_credibility_engine()
        self.data_validator = GroundbreakingDataValidator()
        
        # Initialize Phase 2 advanced engines
        self.semantic_engine = get_semantic_engine()
        self.temporal_engine = get_temporal_engine()
        
        # Integration configuration
        self.config = {
            'semantic_weight': 0.35,      # Weight for semantic analysis
            'temporal_weight': 0.30,      # Weight for temporal analysis
            'foundation_weight': 0.35,    # Weight for Phase 1 foundation
            'min_intelligence_score': 0.6, # Minimum score for intelligent opportunities
            'enhancement_threshold': 0.7   # Threshold for additional enhancement
        }
        
        # Performance tracking
        self.integration_stats = {
            'signals_enhanced': 0,
            'opportunities_enriched': 0,
            'accuracy_improvement': 0.0,
            'avg_processing_time': 0.0,
            'semantic_accuracy': 0.0,
            'temporal_accuracy': 0.0
        }
        
        self.logger.info("✅ Semantic Trend Integration Engine initialized successfully")
    
    async def detect_intelligent_trends(self, hours_back: int = 24) -> List[IntelligentTrendOpportunity]:
        """
        Detect trends using enhanced semantic and temporal intelligence
        
        Args:
            hours_back: Hours to look back for trend detection
            
        Returns:
            List of intelligent trend opportunities with Phase 2 enhancements
        """
        start_time = datetime.now()
        
        try:
            self.logger.info(f"🔍 Starting intelligent trend detection (Phase 2) - {hours_back}h lookback...")
            
            # Step 1: Get foundation trends from Phase 1
            foundation_opportunities = await self.trend_detector.detect_cross_platform_trends(hours_back)
            self.logger.info(f"📊 Phase 1 Foundation: {len(foundation_opportunities)} opportunities detected")
            
            # Step 2: Enhance with semantic understanding
            enhanced_opportunities = []
            for opportunity in foundation_opportunities:
                try:
                    intelligent_opportunity = await self._enhance_with_intelligence(opportunity)
                    if intelligent_opportunity.intelligence_score >= self.config['min_intelligence_score']:
                        enhanced_opportunities.append(intelligent_opportunity)
                except Exception as e:
                    self.logger.warning(f"Failed to enhance opportunity: {e}")
                    continue
            
            self.logger.info(f"🧠 Phase 2 Enhancement: {len(enhanced_opportunities)} intelligent opportunities")
            
            # Step 3: Apply temporal pattern analysis
            temporal_enhanced = await self._apply_temporal_enhancement(enhanced_opportunities)
            
            # Step 4: Final ranking with integrated intelligence
            final_opportunities = await self._rank_intelligent_opportunities(temporal_enhanced)
            
            # Update performance statistics
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_integration_stats(len(final_opportunities), processing_time)
            
            self.logger.info(f"✅ Intelligent trend detection complete: {len(final_opportunities)} opportunities in {processing_time:.2f}s")
            return final_opportunities
            
        except Exception as e:
            self.logger.error(f"❌ Intelligent trend detection failed: {e}")
            return []
    
    async def _enhance_with_intelligence(self, opportunity: TrendOpportunity) -> IntelligentTrendOpportunity:
        """Enhance opportunity with semantic and temporal intelligence"""
        start_time = datetime.now()
        
        # Create intelligent opportunity container
        intelligent_opp = IntelligentTrendOpportunity(original_opportunity=opportunity)
        
        # Semantic Analysis Enhancement
        semantic_analysis = await self._perform_semantic_analysis(opportunity)
        intelligent_opp.semantic_analysis = semantic_analysis
        intelligent_opp.semantic_relevance = semantic_analysis.get('relevance_score', 0.0)
        intelligent_opp.innovation_potential = semantic_analysis.get('innovation_score', 0.0)
        intelligent_opp.business_context = semantic_analysis.get('context_indicators', [])
        
        # Extract market insights from semantic analysis
        market_insights = await self._extract_market_insights(semantic_analysis)
        intelligent_opp.market_indicators = market_insights.get('indicators', [])
        intelligent_opp.competitive_insights = market_insights.get('competitive_analysis', {})
        
        # Temporal Analysis Enhancement
        temporal_analysis = await self._perform_temporal_analysis(opportunity)
        intelligent_opp.temporal_analysis = temporal_analysis
        intelligent_opp.temporal_momentum = temporal_analysis.get('momentum_score', 0.0)
        intelligent_opp.growth_trajectory = temporal_analysis.get('growth_pattern', 'unknown')
        
        # Emergence Prediction
        emergence_prediction = await self._predict_emergence(opportunity, semantic_analysis, temporal_analysis)
        intelligent_opp.emergence_prediction = emergence_prediction
        intelligent_opp.emergence_probability = emergence_prediction.get('probability', 0.0)
        intelligent_opp.optimal_entry_timing = emergence_prediction.get('optimal_timing', 'unknown')
        intelligent_opp.risk_factors = emergence_prediction.get('risks', [])
        
        # Market Timing Assessment
        intelligent_opp.market_timing_score = await self._assess_market_timing(
            semantic_analysis, temporal_analysis, emergence_prediction
        )
        
        # Calculate integrated intelligence score
        intelligent_opp.intelligence_score = self._calculate_intelligence_score(intelligent_opp)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        self.integration_stats['opportunities_enriched'] += 1
        
        return intelligent_opp
    
    async def _perform_semantic_analysis(self, opportunity: TrendOpportunity) -> Dict:
        """Perform comprehensive semantic analysis on opportunity"""
        try:
            # Combine all text content from signals
            combined_content = " ".join([
                opportunity.title,
                opportunity.description,
                *[signal.content for signal in opportunity.signals[:10]]  # Top 10 signals
            ])
            
            # Perform semantic analysis
            semantic_score = await self.semantic_engine.analyze_semantic_understanding(combined_content)
            
            # Extract key insights
            analysis = {
                'relevance_score': semantic_score.context_relevance,
                'innovation_score': semantic_score.innovation_potential,
                'sentiment_analysis': semantic_score.sentiment_breakdown,
                'context_indicators': semantic_score.context_indicators,
                'key_concepts': semantic_score.key_concepts,
                'entities': semantic_score.extracted_entities,
                'intent_classification': semantic_score.intent_classification,
                'confidence': semantic_score.confidence_level
            }
            
            # Enhance with signal-level semantic analysis
            signal_semantics = await self._analyze_signal_semantics(opportunity.signals)
            analysis['signal_analysis'] = signal_semantics
            
            return analysis
            
        except Exception as e:
            self.logger.warning(f"Semantic analysis failed: {e}")
            return {'relevance_score': 0.0, 'confidence': 0.0}
    
    async def _analyze_signal_semantics(self, signals: List[TrendSignal]) -> Dict:
        """Analyze semantics of individual signals"""
        try:
            if not signals:
                return {'avg_relevance': 0.0, 'semantic_clusters': []}
            
            # Batch analyze signals
            signal_contents = [signal.content for signal in signals[:20]]  # Limit for performance
            semantic_scores = await self.semantic_engine.batch_analyze_signals(signal_contents)
            
            if not semantic_scores:
                return {'avg_relevance': 0.0, 'semantic_clusters': []}
            
            # Calculate aggregate metrics
            avg_relevance = np.mean([score.context_relevance for score in semantic_scores])
            avg_innovation = np.mean([score.innovation_potential for score in semantic_scores])
            
            # Semantic clustering
            similarity_analysis = await self.semantic_engine.analyze_signal_similarity(signal_contents)
            
            return {
                'avg_relevance': avg_relevance,
                'avg_innovation': avg_innovation,
                'semantic_clusters': similarity_analysis.get('clusters', []),
                'avg_similarity': similarity_analysis.get('avg_similarity', 0.0),
                'signal_count': len(semantic_scores)
            }
            
        except Exception as e:
            self.logger.warning(f"Signal semantic analysis failed: {e}")
            return {'avg_relevance': 0.0, 'semantic_clusters': []}
    
    async def _extract_market_insights(self, semantic_analysis: Dict) -> Dict:
        """Extract market insights from semantic analysis"""
        insights = {
            'indicators': [],
            'competitive_analysis': {},
            'market_maturity': 'unknown'
        }
        
        try:
            context_indicators = semantic_analysis.get('context_indicators', [])
            
            # Market timing indicators
            if any('market_timing_early' in indicator for indicator in context_indicators):
                insights['indicators'].append('early_stage_market')
                insights['market_maturity'] = 'early'
            elif any('market_timing_growing' in indicator for indicator in context_indicators):
                insights['indicators'].append('growing_market')
                insights['market_maturity'] = 'growth'
            elif any('market_timing_mature' in indicator for indicator in context_indicators):
                insights['indicators'].append('mature_market')
                insights['market_maturity'] = 'mature'
            
            # Opportunity indicators
            if 'opportunity_indicators' in context_indicators:
                insights['indicators'].append('market_opportunity_identified')
            
            # Pain point indicators
            if 'pain_point_indicators' in context_indicators:
                insights['indicators'].append('pain_point_driven')
            
            # Innovation indicators
            innovation_score = semantic_analysis.get('innovation_score', 0.0)
            if innovation_score > 0.7:
                insights['indicators'].append('high_innovation_potential')
            elif innovation_score > 0.4:
                insights['indicators'].append('moderate_innovation_potential')
            
            # Competitive analysis from entities
            entities = semantic_analysis.get('entities', [])
            companies = [ent for ent in entities if ent.get('label') == 'ORG']
            products = [ent for ent in entities if ent.get('label') == 'PRODUCT']
            
            insights['competitive_analysis'] = {
                'companies_mentioned': len(companies),
                'products_mentioned': len(products),
                'competitive_intensity': 'high' if len(companies) > 5 else 'moderate' if len(companies) > 2 else 'low'
            }
            
        except Exception as e:
            self.logger.warning(f"Market insight extraction failed: {e}")
        
        return insights
    
    async def _perform_temporal_analysis(self, opportunity: TrendOpportunity) -> Dict:
        """Perform temporal pattern analysis on opportunity signals"""
        try:
            # Convert signals to temporal analysis format
            signal_data = []
            for signal in opportunity.signals:
                signal_data.append({
                    'timestamp': signal.timestamp,
                    'engagement_score': signal.engagement_score,
                    'sentiment_score': signal.sentiment_score,
                    'credibility_weight': signal.credibility_weight,
                    'source': signal.source
                })
            
            # Analyze temporal patterns
            patterns = await self.temporal_engine.analyze_temporal_patterns(signal_data)
            
            # Generate emergence signals
            emergence_signals = await self.temporal_engine.generate_emergence_signals(patterns)
            
            # Calculate momentum and growth trajectory
            momentum_score = self._calculate_temporal_momentum(patterns)
            growth_pattern = self._determine_growth_pattern(patterns)
            
            return {
                'patterns': [p.__dict__ for p in patterns],  # Convert to dict for JSON serialization
                'emergence_signals': [s.__dict__ for s in emergence_signals],
                'momentum_score': momentum_score,
                'growth_pattern': growth_pattern,
                'pattern_count': len(patterns),
                'emergence_count': len(emergence_signals)
            }
            
        except Exception as e:
            self.logger.warning(f"Temporal analysis failed: {e}")
            return {'momentum_score': 0.0, 'growth_pattern': 'unknown', 'patterns': []}
    
    def _calculate_temporal_momentum(self, patterns: List[TemporalPattern]) -> float:
        """Calculate overall temporal momentum from patterns"""
        if not patterns:
            return 0.0
        
        momentum_scores = []
        for pattern in patterns:
            if pattern.pattern_type in ['emergence', 'trend']:
                momentum_scores.append(pattern.momentum_score)
            elif pattern.pattern_type == 'seasonal':
                momentum_scores.append(pattern.pattern_strength * 0.6)  # Seasonal patterns have moderate momentum
        
        return np.mean(momentum_scores) if momentum_scores else 0.0
    
    def _determine_growth_pattern(self, patterns: List[TemporalPattern]) -> str:
        """Determine the overall growth pattern from temporal analysis"""
        if not patterns:
            return 'unknown'
        
        # Count pattern types
        pattern_types = [p.pattern_type for p in patterns]
        type_counts = {ptype: pattern_types.count(ptype) for ptype in set(pattern_types)}
        
        # Determine dominant pattern
        if 'emergence' in type_counts and type_counts['emergence'] > 0:
            # Check emergence velocity
            emergence_patterns = [p for p in patterns if p.pattern_type == 'emergence']
            avg_velocity = np.mean([p.emergence_velocity for p in emergence_patterns])
            
            if avg_velocity > 0.7:
                return 'explosive_growth'
            elif avg_velocity > 0.4:
                return 'rapid_growth'
            else:
                return 'steady_growth'
        
        elif 'trend' in type_counts and type_counts['trend'] > 0:
            trend_patterns = [p for p in patterns if p.pattern_type == 'trend']
            avg_slope = np.mean([p.trend_slope for p in trend_patterns if hasattr(p, 'trend_slope')])
            
            if avg_slope > 0:
                return 'linear_growth'
            else:
                return 'declining'
        
        elif 'seasonal' in type_counts:
            return 'cyclical'
        
        elif 'anomaly' in type_counts:
            return 'volatile'
        
        return 'stable'
    
    async def _predict_emergence(self, opportunity: TrendOpportunity, semantic_analysis: Dict, temporal_analysis: Dict) -> Dict:
        """Predict trend emergence based on semantic and temporal analysis"""
        try:
            # Base emergence probability from temporal analysis
            emergence_signals = temporal_analysis.get('emergence_signals', [])
            base_probability = np.mean([
                signal.get('emergence_score', 0.0) 
                for signal in emergence_signals
            ]) if emergence_signals else 0.0
            
            # Semantic enhancement factors
            semantic_relevance = semantic_analysis.get('relevance_score', 0.0)
            innovation_potential = semantic_analysis.get('innovation_score', 0.0)
            
            # Market context factors
            market_indicators = semantic_analysis.get('context_indicators', [])
            early_stage_boost = 0.2 if any('early' in indicator for indicator in market_indicators) else 0.0
            
            # Calculate enhanced emergence probability
            enhanced_probability = min(
                base_probability + 
                (semantic_relevance * 0.3) + 
                (innovation_potential * 0.2) + 
                early_stage_boost,
                1.0
            )
            
            # Determine optimal timing
            optimal_timing = 'immediate' if enhanced_probability > 0.8 else \
                            'short_term' if enhanced_probability > 0.6 else \
                            'medium_term' if enhanced_probability > 0.4 else 'uncertain'
            
            # Identify risk factors
            risks = []
            if temporal_analysis.get('momentum_score', 0.0) < 0.3:
                risks.append('low_momentum')
            if semantic_analysis.get('confidence', 0.0) < 0.5:
                risks.append('uncertain_context')
            if 'competitive' in str(semantic_analysis.get('competitive_analysis', {})):
                risks.append('high_competition')
            
            return {
                'probability': enhanced_probability,
                'base_probability': base_probability,
                'semantic_enhancement': enhanced_probability - base_probability,
                'optimal_timing': optimal_timing,
                'risks': risks,
                'confidence': min(semantic_analysis.get('confidence', 0.0) + 0.2, 1.0)
            }
            
        except Exception as e:
            self.logger.warning(f"Emergence prediction failed: {e}")
            return {'probability': 0.0, 'optimal_timing': 'uncertain', 'risks': ['analysis_failed']}
    
    async def _assess_market_timing(self, semantic_analysis: Dict, temporal_analysis: Dict, emergence_prediction: Dict) -> float:
        """Assess optimal market timing score"""
        try:
            # Temporal momentum component
            momentum_component = temporal_analysis.get('momentum_score', 0.0) * 0.4
            
            # Emergence probability component
            emergence_component = emergence_prediction.get('probability', 0.0) * 0.3
            
            # Market maturity component (early stage gets higher timing score)
            market_maturity = semantic_analysis.get('market_maturity', 'unknown')
            maturity_component = {
                'early': 0.3,
                'growth': 0.2,
                'mature': 0.1,
                'unknown': 0.15
            }.get(market_maturity, 0.15)
            
            # Innovation potential component
            innovation_component = semantic_analysis.get('innovation_score', 0.0) * 0.1
            
            timing_score = momentum_component + emergence_component + maturity_component + innovation_component
            return min(timing_score, 1.0)
            
        except:
            return 0.5  # Default moderate timing score
    
    def _calculate_intelligence_score(self, intelligent_opp: IntelligentTrendOpportunity) -> float:
        """Calculate integrated intelligence score"""
        try:
            # Phase 1 foundation score (from original momentum)
            foundation_score = intelligent_opp.original_opportunity.momentum_score
            
            # Phase 2 enhancement scores
            semantic_score = intelligent_opp.semantic_relevance
            temporal_score = intelligent_opp.temporal_momentum
            
            # Weighted combination based on configuration
            intelligence_score = (
                foundation_score * self.config['foundation_weight'] +
                semantic_score * self.config['semantic_weight'] +
                temporal_score * self.config['temporal_weight']
            )
            
            # Boost for high innovation potential
            if intelligent_opp.innovation_potential > 0.7:
                intelligence_score *= 1.2
            
            # Boost for high emergence probability
            if intelligent_opp.emergence_probability > 0.7:
                intelligence_score *= 1.15
            
            return min(intelligence_score, 1.0)
            
        except:
            return 0.0
    
    async def _apply_temporal_enhancement(self, opportunities: List[IntelligentTrendOpportunity]) -> List[IntelligentTrendOpportunity]:
        """Apply additional temporal enhancements to opportunities"""
        # For now, return as-is. Future enhancement: cross-opportunity temporal correlation
        return opportunities
    
    async def _rank_intelligent_opportunities(self, opportunities: List[IntelligentTrendOpportunity]) -> List[IntelligentTrendOpportunity]:
        """Rank opportunities by integrated intelligence score"""
        try:
            # Sort by intelligence score (descending)
            ranked_opportunities = sorted(
                opportunities,
                key=lambda opp: (
                    opp.intelligence_score,
                    opp.emergence_probability,
                    opp.market_timing_score
                ),
                reverse=True
            )
            
            return ranked_opportunities
            
        except Exception as e:
            self.logger.warning(f"Ranking failed: {e}")
            return opportunities
    
    def _update_integration_stats(self, opportunities_count: int, processing_time: float):
        """Update integration performance statistics"""
        self.integration_stats['opportunities_enriched'] += opportunities_count
        
        # Update average processing time
        current_avg = self.integration_stats['avg_processing_time']
        total_processed = self.integration_stats['opportunities_enriched']
        if total_processed > 0:
            self.integration_stats['avg_processing_time'] = (
                (current_avg * (total_processed - opportunities_count) + processing_time) / total_processed
            )
        else:
            self.integration_stats['avg_processing_time'] = processing_time
    
    def get_integration_stats(self) -> Dict:
        """Get current integration performance statistics"""
        stats = self.integration_stats.copy()
        
        # Add component statistics
        stats.update({
            'semantic_engine_stats': self.semantic_engine.get_performance_stats(),
            'temporal_engine_stats': self.temporal_engine.get_performance_stats()
        })
        
        return stats
    
    async def analyze_opportunity_context(self, opportunity: IntelligentTrendOpportunity) -> Dict:
        """Provide detailed context analysis for an opportunity"""
        try:
            context_analysis = {
                'semantic_insights': {
                    'business_relevance': opportunity.semantic_relevance,
                    'innovation_level': opportunity.innovation_potential,
                    'key_concepts': opportunity.semantic_analysis.get('key_concepts', []),
                    'market_context': opportunity.business_context
                },
                'temporal_insights': {
                    'momentum': opportunity.temporal_momentum,
                    'growth_trajectory': opportunity.growth_trajectory,
                    'pattern_analysis': opportunity.temporal_analysis.get('patterns', [])
                },
                'market_insights': {
                    'timing_score': opportunity.market_timing_score,
                    'emergence_probability': opportunity.emergence_probability,
                    'optimal_entry': opportunity.optimal_entry_timing,
                    'risk_factors': opportunity.risk_factors
                },
                'competitive_insights': opportunity.competitive_insights,
                'overall_intelligence': opportunity.intelligence_score
            }
            
            return context_analysis
            
        except Exception as e:
            self.logger.error(f"Context analysis failed: {e}")
            return {}

# Global integration engine instance
_integration_engine = None

def get_semantic_trend_integration_engine() -> SemanticTrendIntegrationEngine:
    """Get or create the global semantic trend integration engine instance"""
    global _integration_engine
    if _integration_engine is None:
        _integration_engine = SemanticTrendIntegrationEngine()
    return _integration_engine 