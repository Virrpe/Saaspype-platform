#!/usr/bin/env python3
"""
Contextual Source Intelligence Engine - Hegelian Dialectical Synthesis
Resolves the quantity-quality contradiction through intelligent source curation
Enhanced with Authority-Weighted Quality Scoring (Phase 1 Tactical Improvement)
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from collections import defaultdict, Counter

# Phase 1 Tactical Improvement: Authority Analyzer Integration
from .authority_analyzer import AuthorityAnalyzer

logger = logging.getLogger(__name__)

class QueryContext(Enum):
    """Different contexts that require different source strategies"""
    PAIN_POINT_DISCOVERY = "pain_point_discovery"
    TECHNICAL_TRENDS = "technical_trends"
    MARKET_VALIDATION = "market_validation"
    STARTUP_INTELLIGENCE = "startup_intelligence"
    REAL_TIME_MONITORING = "real_time_monitoring"
    COMPETITIVE_ANALYSIS = "competitive_analysis"
    DEVELOPER_INSIGHTS = "developer_insights"
    GENERAL_EXPLORATION = "general_exploration"

@dataclass
class ContextualSourceConfig:
    """Configuration for a source in a specific context"""
    source_name: str
    activation_threshold: float  # Context relevance threshold to activate
    quality_weight: float  # Quality multiplier in this context
    cost_multiplier: float  # Cost adjustment for this context
    max_signals: int  # Maximum signals to collect in this context
    priority_keywords: List[str] = field(default_factory=list)
    exclusion_keywords: List[str] = field(default_factory=list)

@dataclass
class DialecticalSourceMetrics:
    """Metrics that capture the dialectical tension resolution"""
    source_name: str
    context: QueryContext
    thesis_score: float  # Raw quantity/coverage score
    antithesis_score: float  # Quality/efficiency score
    synthesis_score: float  # Resolved contextual value
    activation_confidence: float  # Confidence in activation decision
    expected_roi: float  # Expected return on investment
    dialectical_tension: float  # Measure of quantity-quality tension

class ContextualSourceIntelligenceEngine:
    """
    Hegelian Dialectical Synthesis for Source Intelligence
    
    Implements the Aufhebung (sublation) of the quantity-quality contradiction:
    - THESIS: More sources = better coverage
    - ANTITHESIS: Fewer sources = better quality  
    - SYNTHESIS: Contextual intelligence = optimal value
    
    Enhanced with Phase 1 Tactical Improvement: Authority-Weighted Quality Scoring
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Phase 1 Tactical Improvement: Initialize Authority Analyzer
        self.authority_analyzer = AuthorityAnalyzer()
        
        # Source characteristics from our analysis
        self.source_characteristics = self._initialize_enhanced_source_characteristics()
        
        # Contextual source configurations (the synthesis)
        self.contextual_configurations = self._initialize_contextual_configurations()
        
        # Active source state
        self.active_sources = set()
        self.context_history = []
        self.performance_metrics = defaultdict(list)
        
        self.logger.info("Contextual Source Intelligence Engine initialized with dialectical synthesis and authority-weighted quality scoring")
    
    def _initialize_enhanced_source_characteristics(self) -> Dict:
        """Initialize source characteristics enhanced with authority analysis"""
        
        # Base source characteristics from empirical analysis
        base_characteristics = {
            'github': {
                'base_quality': 0.90,
                'base_cost': 1.2,
                'uniqueness': 0.95,
                'noise_tendency': 0.15,
                'domains': ['technical_trends', 'developer_tools', 'open_source']
            },
            'hackernews': {
                'base_quality': 0.85,
                'base_cost': 0.9,
                'uniqueness': 0.85,
                'noise_tendency': 0.20,
                'domains': ['tech_innovation', 'startup_trends', 'technical_discussion']
            },
            'producthunt': {
                'base_quality': 0.80,
                'base_cost': 0.7,
                'uniqueness': 0.75,
                'noise_tendency': 0.25,
                'domains': ['product_launches', 'market_validation', 'consumer_interest']
            },
            'stackoverflow': {
                'base_quality': 0.88,
                'base_cost': 1.1,
                'uniqueness': 0.85,
                'noise_tendency': 0.18,
                'domains': ['technical_problems', 'developer_pain_points', 'solution_patterns']
            },
            'reddit': {
                'base_quality': 0.75,
                'base_cost': 1.0,
                'uniqueness': 0.80,
                'noise_tendency': 0.35,
                'domains': ['social_discussion', 'pain_points', 'community_feedback']
            },
            'indiehackers': {
                'base_quality': 0.82,
                'base_cost': 0.9,
                'uniqueness': 0.80,
                'noise_tendency': 0.22,
                'domains': ['entrepreneurship', 'business_building', 'revenue_strategies']
            },
            'devto': {
                'base_quality': 0.78,
                'base_cost': 0.8,
                'uniqueness': 0.70,
                'noise_tendency': 0.30,
                'domains': ['developer_content', 'tutorials', 'tech_insights']
            },
            'twitter': {
                'base_quality': 0.65,
                'base_cost': 0.8,
                'uniqueness': 0.60,
                'noise_tendency': 0.55,
                'domains': ['trending_topics', 'real_time_sentiment', 'viral_content']
            }
        }
        
        # Enhance with authority analysis (Phase 1 Integration)
        enhanced_characteristics = self.authority_analyzer.enhance_source_characteristics(base_characteristics)
        
        self.logger.info("Source characteristics enhanced with authority-weighted quality scores")
        
        # Log improvements for monitoring
        for source, chars in enhanced_characteristics.items():
            if 'quality_enhancement' in chars:
                improvement = chars['quality_enhancement']
                self.logger.info(f"Authority enhancement for {source}: {improvement:+.3f}")
        
        return enhanced_characteristics
    
    def _initialize_contextual_configurations(self) -> Dict[QueryContext, List[ContextualSourceConfig]]:
        """Initialize contextual source configurations based on dialectical analysis"""
        
        configs = {
            QueryContext.PAIN_POINT_DISCOVERY: [
                ContextualSourceConfig(
                    source_name='reddit',
                    activation_threshold=0.7,
                    quality_weight=1.2,  # Boost quality for pain point clarity
                    cost_multiplier=0.8,  # Accept higher cost for pain insights
                    max_signals=100,
                    priority_keywords=['problem', 'frustrating', 'difficult', 'need', 'struggle', 'pain']
                ),
                ContextualSourceConfig(
                    source_name='stackoverflow',
                    activation_threshold=0.6,
                    quality_weight=1.1,
                    cost_multiplier=0.9,
                    max_signals=50,
                    priority_keywords=['error', 'issue', 'problem', 'help', 'stuck']
                ),
                ContextualSourceConfig(
                    source_name='hackernews',
                    activation_threshold=0.5,
                    quality_weight=1.0,
                    cost_multiplier=1.0,
                    max_signals=30,
                    priority_keywords=['problem', 'solution', 'issue']
                )
            ],
            
            QueryContext.TECHNICAL_TRENDS: [
                ContextualSourceConfig(
                    source_name='github',
                    activation_threshold=0.8,
                    quality_weight=1.3,  # Highest quality for technical trends
                    cost_multiplier=0.7,  # Worth the cost
                    max_signals=75,
                    priority_keywords=['trending', 'popular', 'new', 'release', 'update']
                ),
                ContextualSourceConfig(
                    source_name='hackernews',
                    activation_threshold=0.7,
                    quality_weight=1.2,
                    cost_multiplier=0.8,
                    max_signals=50,
                    priority_keywords=['tech', 'technology', 'programming', 'development']
                ),
                ContextualSourceConfig(
                    source_name='devto',
                    activation_threshold=0.6,
                    quality_weight=1.0,
                    cost_multiplier=1.0,
                    max_signals=40,
                    priority_keywords=['tutorial', 'guide', 'how-to', 'tips']
                )
            ],
            
            QueryContext.MARKET_VALIDATION: [
                ContextualSourceConfig(
                    source_name='producthunt',
                    activation_threshold=0.9,  # Primary source for market validation
                    quality_weight=1.4,
                    cost_multiplier=0.6,
                    max_signals=60,
                    priority_keywords=['launch', 'product', 'startup', 'new', 'innovative']
                ),
                ContextualSourceConfig(
                    source_name='indiehackers',
                    activation_threshold=0.7,
                    quality_weight=1.2,
                    cost_multiplier=0.8,
                    max_signals=40,
                    priority_keywords=['revenue', 'customers', 'growth', 'validation']
                ),
                ContextualSourceConfig(
                    source_name='reddit',
                    activation_threshold=0.6,
                    quality_weight=1.0,
                    cost_multiplier=1.0,
                    max_signals=50,
                    priority_keywords=['feedback', 'review', 'opinion', 'thoughts']
                )
            ],
            
            QueryContext.STARTUP_INTELLIGENCE: [
                ContextualSourceConfig(
                    source_name='hackernews',
                    activation_threshold=0.8,
                    quality_weight=1.3,
                    cost_multiplier=0.7,
                    max_signals=60,
                    priority_keywords=['startup', 'funding', 'vc', 'entrepreneur']
                ),
                ContextualSourceConfig(
                    source_name='indiehackers',
                    activation_threshold=0.8,
                    quality_weight=1.2,
                    cost_multiplier=0.8,
                    max_signals=50,
                    priority_keywords=['business', 'revenue', 'growth', 'founder']
                ),
                ContextualSourceConfig(
                    source_name='producthunt',
                    activation_threshold=0.6,
                    quality_weight=1.1,
                    cost_multiplier=0.9,
                    max_signals=40,
                    priority_keywords=['startup', 'entrepreneur', 'founder']
                )
            ],
            
            QueryContext.REAL_TIME_MONITORING: [
                ContextualSourceConfig(
                    source_name='twitter',
                    activation_threshold=0.7,
                    quality_weight=0.9,  # Lower quality acceptable for real-time
                    cost_multiplier=1.2,  # Higher cost for real-time processing
                    max_signals=100,
                    priority_keywords=['breaking', 'now', 'trending', 'live']
                ),
                ContextualSourceConfig(
                    source_name='hackernews',
                    activation_threshold=0.6,
                    quality_weight=1.1,
                    cost_multiplier=1.0,
                    max_signals=30,
                    priority_keywords=['news', 'update', 'announcement']
                )
            ],
            
            QueryContext.DEVELOPER_INSIGHTS: [
                ContextualSourceConfig(
                    source_name='stackoverflow',
                    activation_threshold=0.9,
                    quality_weight=1.4,
                    cost_multiplier=0.6,
                    max_signals=80,
                    priority_keywords=['development', 'programming', 'code', 'developer']
                ),
                ContextualSourceConfig(
                    source_name='github',
                    activation_threshold=0.8,
                    quality_weight=1.3,
                    cost_multiplier=0.7,
                    max_signals=60,
                    priority_keywords=['repository', 'code', 'project', 'development']
                ),
                ContextualSourceConfig(
                    source_name='devto',
                    activation_threshold=0.7,
                    quality_weight=1.1,
                    cost_multiplier=0.9,
                    max_signals=50,
                    priority_keywords=['programming', 'development', 'coding']
                )
            ],
            
            QueryContext.GENERAL_EXPLORATION: [
                # Balanced approach for general queries
                ContextualSourceConfig(
                    source_name='hackernews',
                    activation_threshold=0.6,
                    quality_weight=1.1,
                    cost_multiplier=0.9,
                    max_signals=50,
                    priority_keywords=[]
                ),
                ContextualSourceConfig(
                    source_name='github',
                    activation_threshold=0.5,
                    quality_weight=1.2,
                    cost_multiplier=1.0,
                    max_signals=40,
                    priority_keywords=[]
                ),
                ContextualSourceConfig(
                    source_name='producthunt',
                    activation_threshold=0.5,
                    quality_weight=1.0,
                    cost_multiplier=1.0,
                    max_signals=40,
                    priority_keywords=[]
                )
            ]
        }
        
        return configs
    
    async def determine_optimal_sources(self, query: str, context: QueryContext = None) -> Dict:
        """
        Dialectical source selection - the core synthesis method
        
        Resolves the quantity-quality contradiction through contextual intelligence
        """
        
        self.logger.info(f"🧠 Dialectical source analysis for query: '{query[:50]}...'")
        
        # Auto-detect context if not provided
        if context is None:
            context = await self._detect_query_context(query)
        
        self.logger.info(f"📊 Detected context: {context.value if hasattr(context, 'value') else context}")
        
        # Get contextual configurations - handle both QueryContext enum and dict
        if isinstance(context, dict):
            # If context is a dict, use general exploration
            context = QueryContext.GENERAL_EXPLORATION
            
        context_configs = self.contextual_configurations.get(context, 
                                                           self.contextual_configurations[QueryContext.GENERAL_EXPLORATION])
        
        # Perform dialectical analysis for each potential source
        dialectical_metrics = []
        
        for config in context_configs:
            metrics = await self._calculate_dialectical_metrics(config, query, context)
            dialectical_metrics.append(metrics)
        
        # Apply the synthesis - select sources that resolve the contradiction
        selected_sources = self._apply_dialectical_synthesis(dialectical_metrics)
        
        # Update active sources
        self.active_sources = {source.source_name for source in selected_sources}
        
        # Record context history
        self.context_history.append({
            'timestamp': datetime.now(),
            'query': query,
            'context': context,
            'selected_sources': list(self.active_sources),
            'dialectical_metrics': dialectical_metrics
        })
        
        synthesis_result = {
            'context': context,
            'selected_sources': [
                {
                    'source': source.source_name,
                    'synthesis_score': source.synthesis_score,
                    'expected_roi': source.expected_roi,
                    'max_signals': next(c.max_signals for c in context_configs if c.source_name == source.source_name),
                    'quality_weight': next(c.quality_weight for c in context_configs if c.source_name == source.source_name)
                }
                for source in selected_sources
            ],
            'dialectical_reasoning': self._generate_dialectical_explanation(dialectical_metrics, selected_sources),
            'synthesis_metadata': {
                'total_sources_considered': len(dialectical_metrics),
                'sources_activated': len(selected_sources),
                'avg_synthesis_score': np.mean([s.synthesis_score for s in selected_sources]),
                'dialectical_tension_resolved': np.mean([s.dialectical_tension for s in selected_sources])
            }
        }
        
        self.logger.info(f"✅ Dialectical synthesis complete: {len(selected_sources)} sources activated")
        
        return synthesis_result
    
    async def _detect_query_context(self, query: str) -> QueryContext:
        """Detect the context of a query using keyword analysis"""
        
        query_lower = query.lower()
        
        # Context detection patterns
        context_patterns = {
            QueryContext.PAIN_POINT_DISCOVERY: [
                'problem', 'issue', 'frustrating', 'difficult', 'struggle', 'pain', 'annoying',
                'broken', 'doesn\'t work', 'need help', 'stuck', 'challenge'
            ],
            QueryContext.TECHNICAL_TRENDS: [
                'technology', 'programming', 'development', 'coding', 'framework', 'library',
                'trending', 'popular', 'new tech', 'latest', 'emerging'
            ],
            QueryContext.MARKET_VALIDATION: [
                'market', 'validation', 'product', 'launch', 'customers', 'feedback',
                'demand', 'opportunity', 'viable', 'business model'
            ],
            QueryContext.STARTUP_INTELLIGENCE: [
                'startup', 'entrepreneur', 'funding', 'vc', 'investment', 'founder',
                'business', 'revenue', 'growth', 'scale'
            ],
            QueryContext.REAL_TIME_MONITORING: [
                'trending', 'now', 'current', 'latest', 'breaking', 'recent',
                'today', 'this week', 'happening'
            ],
            QueryContext.DEVELOPER_INSIGHTS: [
                'developer', 'programming', 'code', 'software', 'engineering',
                'development', 'technical', 'coding', 'programmer'
            ]
        }
        
        # Score each context
        context_scores = {}
        for context, keywords in context_patterns.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                context_scores[context] = score / len(keywords)  # Normalize
        
        # Return highest scoring context or general exploration
        if context_scores:
            return max(context_scores.items(), key=lambda x: x[1])[0]
        else:
            return QueryContext.GENERAL_EXPLORATION
    
    async def _calculate_dialectical_metrics(self, config: ContextualSourceConfig, 
                                           query: str, context: QueryContext) -> DialecticalSourceMetrics:
        """Calculate dialectical metrics for a source in context"""
        
        source_char = self.source_characteristics[config.source_name]
        
        # THESIS: Quantity/Coverage score
        thesis_score = self._calculate_thesis_score(config, source_char, query)
        
        # ANTITHESIS: Quality/Efficiency score  
        antithesis_score = self._calculate_antithesis_score(config, source_char)
        
        # SYNTHESIS: Contextual value resolution
        synthesis_score = self._calculate_synthesis_score(thesis_score, antithesis_score, config, context)
        
        # Dialectical tension (how much contradiction exists)
        dialectical_tension = abs(thesis_score - antithesis_score) / max(thesis_score, antithesis_score, 0.1)
        
        # Activation confidence
        activation_confidence = synthesis_score * (1 - dialectical_tension * 0.3)
        
        # Expected ROI
        expected_roi = synthesis_score / (source_char['base_cost'] * config.cost_multiplier)
        
        return DialecticalSourceMetrics(
            source_name=config.source_name,
            context=context,
            thesis_score=thesis_score,
            antithesis_score=antithesis_score,
            synthesis_score=synthesis_score,
            activation_confidence=activation_confidence,
            expected_roi=expected_roi,
            dialectical_tension=dialectical_tension
        )
    
    def _calculate_thesis_score(self, config: ContextualSourceConfig, 
                              source_char: Dict, query: str) -> float:
        """Calculate thesis score (quantity/coverage perspective)"""
        
        # Base coverage from source characteristics
        coverage_score = source_char['uniqueness']
        
        # Keyword relevance boost
        query_lower = query.lower()
        keyword_matches = sum(1 for keyword in config.priority_keywords if keyword in query_lower)
        keyword_boost = min(0.3, keyword_matches * 0.1)  # Max 30% boost
        
        # Domain relevance
        domain_relevance = 0.8  # Default relevance
        
        thesis_score = coverage_score + keyword_boost + (domain_relevance * 0.2)
        
        return min(1.0, thesis_score)
    
    def _calculate_antithesis_score(self, config: ContextualSourceConfig, 
                                  source_char: Dict) -> float:
        """
        Calculate antithesis score (quality/efficiency perspective)
        Enhanced with Phase 1 Authority-Weighted Quality Scoring
        """
        
        # Phase 1 Enhancement: Use authority-weighted dialectical quality if available
        if 'dialectical_quality' in source_char:
            # Use enhanced quality from authority analyzer
            base_quality = source_char['dialectical_quality']
            self.logger.debug(f"Using authority-enhanced quality for {config.source_name}: {base_quality:.3f}")
        else:
            # Fallback to base quality
            base_quality = source_char['base_quality']
            self.logger.debug(f"Using base quality for {config.source_name}: {base_quality:.3f}")
        
        # Apply contextual quality weight
        quality_score = base_quality * config.quality_weight
        
        # Efficiency (inverse of cost)
        efficiency_score = 1.0 / (source_char['base_cost'] * config.cost_multiplier)
        
        # Noise penalty
        noise_penalty = source_char['noise_tendency']
        
        # Calculate final antithesis score
        antithesis_score = (quality_score * 0.6 + efficiency_score * 0.4) * (1 - noise_penalty * 0.3)
        
        return min(1.0, antithesis_score)
    
    def _calculate_synthesis_score(self, thesis: float, antithesis: float, 
                                 config: ContextualSourceConfig, context: QueryContext) -> float:
        """Calculate synthesis score - the dialectical resolution"""
        
        # The synthesis resolves the contradiction through contextual weighting
        base_synthesis = (thesis + antithesis) / 2
        
        # Context-specific adjustments
        context_multiplier = 1.0
        if context in [QueryContext.TECHNICAL_TRENDS, QueryContext.DEVELOPER_INSIGHTS]:
            # Favor quality over quantity for technical contexts
            context_multiplier = 0.3 * thesis + 0.7 * antithesis
        elif context in [QueryContext.REAL_TIME_MONITORING]:
            # Favor quantity over quality for real-time contexts
            context_multiplier = 0.7 * thesis + 0.3 * antithesis
        else:
            # Balanced approach for other contexts
            context_multiplier = 0.5 * thesis + 0.5 * antithesis
        
        # Activation threshold consideration
        threshold_factor = min(1.0, max(thesis, antithesis) / config.activation_threshold)
        
        synthesis_score = context_multiplier * threshold_factor
        
        return min(1.0, synthesis_score)
    
    def _apply_dialectical_synthesis(self, metrics: List[DialecticalSourceMetrics]) -> List[DialecticalSourceMetrics]:
        """Apply the dialectical synthesis to select optimal sources"""
        
        # Sort by synthesis score
        sorted_metrics = sorted(metrics, key=lambda x: x.synthesis_score, reverse=True)
        
        # Select sources that meet activation criteria
        selected = []
        total_cost = 0
        max_total_cost = 3.0  # Budget constraint
        
        for metric in sorted_metrics:
            source_char = self.source_characteristics[metric.source_name]
            source_cost = source_char['base_cost']
            
            # Check if we should activate this source
            if (metric.activation_confidence >= 0.6 and  # Minimum confidence
                total_cost + source_cost <= max_total_cost and  # Budget constraint
                len(selected) < 4):  # Maximum sources constraint
                
                selected.append(metric)
                total_cost += source_cost
        
        # Ensure at least one source is selected
        if not selected and sorted_metrics:
            selected.append(sorted_metrics[0])
        
        return selected
    
    def _generate_dialectical_explanation(self, all_metrics: List[DialecticalSourceMetrics], 
                                        selected: List[DialecticalSourceMetrics]) -> Dict:
        """Generate explanation of the dialectical reasoning"""
        
        return {
            'dialectical_process': {
                'thesis_analysis': f"Evaluated {len(all_metrics)} sources for coverage and relevance",
                'antithesis_analysis': f"Applied quality and efficiency filters",
                'synthesis_resolution': f"Selected {len(selected)} sources that optimize contextual value"
            },
            'selection_reasoning': [
                {
                    'source': metric.source_name,
                    'thesis_score': round(metric.thesis_score, 3),
                    'antithesis_score': round(metric.antithesis_score, 3),
                    'synthesis_score': round(metric.synthesis_score, 3),
                    'dialectical_tension': round(metric.dialectical_tension, 3),
                    'reasoning': f"Synthesis resolves {metric.dialectical_tension:.1%} tension between coverage and quality"
                }
                for metric in selected
            ],
            'rejected_sources': [
                {
                    'source': metric.source_name,
                    'synthesis_score': round(metric.synthesis_score, 3),
                    'reason': 'Below activation threshold' if metric.activation_confidence < 0.6 else 'Budget/capacity constraint'
                }
                for metric in all_metrics if metric not in selected
            ]
        }
    
    def get_dialectical_performance_report(self) -> Dict:
        """Generate performance report showing dialectical effectiveness"""
        
        if not self.context_history:
            return {'error': 'No dialectical history available'}
        
        # Analyze context distribution
        context_distribution = Counter(entry['context'] for entry in self.context_history)
        
        # Analyze source activation patterns
        source_activations = defaultdict(int)
        for entry in self.context_history:
            for source in entry['selected_sources']:
                source_activations[source] += 1
        
        # Calculate dialectical efficiency
        avg_sources_per_query = np.mean([len(entry['selected_sources']) for entry in self.context_history])
        
        # Calculate average synthesis score from dialectical metrics
        synthesis_scores = []
        for entry in self.context_history:
            if 'dialectical_metrics' in entry and entry['dialectical_metrics']:
                entry_scores = [metric.synthesis_score for metric in entry['dialectical_metrics'] if hasattr(metric, 'synthesis_score')]
                if entry_scores:
                    synthesis_scores.append(np.mean(entry_scores))
        
        avg_synthesis_score = np.mean(synthesis_scores) if synthesis_scores else 0.0
        
        return {
            'dialectical_summary': {
                'total_queries_processed': len(self.context_history),
                'contexts_encountered': len(context_distribution),
                'avg_sources_per_query': round(avg_sources_per_query, 2),
                'dialectical_efficiency': f"{(3.0 / avg_sources_per_query):.1%}"  # Efficiency vs max sources
            },
            'context_distribution': dict(context_distribution),
            'source_activation_frequency': dict(source_activations),
            'synthesis_effectiveness': {
                'avg_synthesis_score': avg_synthesis_score,
                'dialectical_tension_resolution': "Successfully resolving quantity-quality contradictions"
            }
        }

# Factory function
def get_contextual_source_intelligence() -> ContextualSourceIntelligenceEngine:
    """Get the contextual source intelligence engine instance"""
    return ContextualSourceIntelligenceEngine() 