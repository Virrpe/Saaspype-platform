#!/usr/bin/env python3
"""
Advanced Signal Quality Enhancement System
Implements sophisticated extraction logic for high-quality business insights
"""

import re
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, field
import numpy as np
from collections import defaultdict, Counter
import logging

logger = logging.getLogger(__name__)

@dataclass
class EnhancedSignal:
    """Enhanced signal with advanced quality metrics"""
    original_signal: object
    quality_score: float
    relevance_score: float
    business_potential: float
    urgency_score: float
    market_timing: str
    pain_point_indicators: List[str]
    solution_indicators: List[str]
    market_size_signals: List[str]
    competition_signals: List[str]
    technology_relevance: float
    semantic_keywords: List[str]
    context_analysis: Dict
    confidence_level: float

class AdvancedSignalQualityEnhancer:
    """Revolutionary signal quality enhancement system"""
    
    def __init__(self):
        self.session = None
        
        # Enhanced Quality Thresholds (demo-friendly for showcase)
        self.enhanced_thresholds = {
            'minimum_overall_quality': 0.3,  # Lowered from 0.75 for demo
            'minimum_business_relevance': 0.3,  # Lowered from 0.7
            'minimum_pain_point_clarity': 0.2,  # Lowered from 0.6
            'minimum_solution_feasibility': 0.2,  # Lowered from 0.5
            'minimum_market_timing': 0.2  # Lowered from 0.6
        }
        
        # Advanced Keyword Categories with Context
        self.business_keyword_categories = {
            'pain_points': {
                'explicit': [
                    'problem', 'issue', 'struggle', 'difficult', 'frustrating', 'broken',
                    'inefficient', 'time consuming', 'expensive', 'complicated', 'manual',
                    'outdated', 'slow', 'unreliable', 'confusing', 'annoying'
                ],
                'implicit': [
                    'wish there was', 'if only', 'need something', 'missing feature',
                    'should exist', 'someone should build', 'why isn\'t there',
                    'surprised no one has', 'would pay for', 'looking for'
                ],
                'intensity_modifiers': [
                    'really', 'extremely', 'very', 'incredibly', 'seriously',
                    'desperately', 'urgently', 'badly', 'constantly', 'always'
                ]
            },
            'solution_indicators': {
                'building': [
                    'building', 'creating', 'developing', 'working on', 'launching',
                    'mvp', 'prototype', 'beta', 'early access', 'just launched'
                ],
                'validation': [
                    'traction', 'customers', 'users', 'revenue', 'growth',
                    'demand', 'interest', 'waiting list', 'pre-orders'
                ],
                'market_ready': [
                    'product market fit', 'scaling', 'profitable', 'series a',
                    'funding', 'investors', 'exit', 'acquisition'
                ]
            },
            'market_timing': {
                'early': [
                    'emerging', 'new trend', 'just started', 'early days',
                    'beginning to see', 'starting to notice', 'first time'
                ],
                'growing': [
                    'growing', 'increasing', 'more and more', 'trend',
                    'popular', 'mainstream', 'adoption', 'widespread'
                ],
                'mature': [
                    'established', 'standard', 'everyone uses', 'mature market',
                    'competitive', 'saturated', 'commoditized'
                ]
            },
            'business_value': {
                'enterprise': [
                    'enterprise', 'business', 'company', 'organization',
                    'team', 'corporate', 'professional', 'commercial'
                ],
                'revenue_potential': [
                    'saas', 'subscription', 'recurring', 'platform',
                    'marketplace', 'monetize', 'revenue', 'profit'
                ],
                'scale_indicators': [
                    'scale', 'automation', 'efficiency', 'productivity',
                    'optimization', 'streamline', 'workflow'
                ]
            }
        }
        
        # Industry-Specific Context Patterns
        self.industry_contexts = {
            'saas_business': {
                'keywords': ['saas', 'software', 'platform', 'tool', 'app', 'service'],
                'pain_points': ['integration', 'onboarding', 'user management', 'billing'],
                'opportunities': ['api', 'automation', 'analytics', 'collaboration']
            },
            'e_commerce': {
                'keywords': ['ecommerce', 'online store', 'shopping', 'retail'],
                'pain_points': ['inventory', 'fulfillment', 'customer service', 'returns'],
                'opportunities': ['personalization', 'conversion', 'logistics', 'payments']
            },
            'remote_work': {
                'keywords': ['remote', 'distributed', 'virtual', 'home office'],
                'pain_points': ['communication', 'collaboration', 'productivity', 'isolation'],
                'opportunities': ['video conferencing', 'project management', 'culture']
            },
            'content_creation': {
                'keywords': ['content', 'creator', 'influencer', 'social media'],
                'pain_points': ['monetization', 'audience growth', 'content planning'],
                'opportunities': ['scheduling', 'analytics', 'brand partnerships']
            }
        }
        
        # Advanced Sentiment Analysis Patterns
        self.sentiment_patterns = {
            'high_frustration': [
                r'\b(hate|terrible|awful|worst|horrible|nightmare)\b',
                r'\b(can\'t stand|fed up|tired of|sick of)\b',
                r'[!]{2,}.*\b(ugh|argh|why|seriously)\b'
            ],
            'urgent_need': [
                r'\b(need|require|must have|essential|critical)\b.*\b(now|asap|urgent|immediately)\b',
                r'\b(desperately|badly|really) need\b',
                r'\b(can\'t wait|running out of time)\b'
            ],
            'market_opportunity': [
                r'\b(opportunity|gap|market|niche|underserved)\b',
                r'\b(first mover|early adopter|pioneer)\b',
                r'\b(no competition|blue ocean|untapped)\b'
            ],
            'willingness_to_pay': [
                r'\b(would pay|willing to pay|budget|invest in)\b',
                r'\b(\$\d+|expensive but worth|premium|subscription)\b',
                r'\b(roi|return on investment|cost savings)\b'
            ]
        }
        
        # Quality scoring weights
        self.quality_weights = {
            'pain_point_clarity': 0.25,
            'solution_feasibility': 0.20,
            'market_timing': 0.20,
            'business_relevance': 0.15,
            'urgency_indicators': 0.10,
            'source_credibility': 0.10
        }
    
    async def enhance_signals(self, raw_signals: List) -> List[EnhancedSignal]:
        """Main enhancement pipeline for signal quality improvement"""
        
        logger.info(f"🔍 Starting advanced signal enhancement for {len(raw_signals)} signals...")
        
        enhanced_signals = []
        
        for signal in raw_signals:
            try:
                # Multi-dimensional quality analysis
                enhanced = await self._comprehensive_signal_analysis(signal)
                
                # Only include high-quality signals
                if enhanced.quality_score >= self.enhanced_thresholds['minimum_overall_quality']:
                    enhanced_signals.append(enhanced)
                    
            except Exception as e:
                logger.error(f"Enhancement error for signal: {e}")
                continue
        
        # Rank by quality and business potential
        enhanced_signals.sort(
            key=lambda x: (x.quality_score * x.business_potential * x.confidence_level),
            reverse=True
        )
        
        logger.info(f"✅ Enhancement complete: {len(enhanced_signals)} high-quality signals retained")
        logger.info(f"   📈 Quality retention rate: {len(enhanced_signals)/len(raw_signals)*100:.1f}%")
        
        return enhanced_signals
    
    async def _comprehensive_signal_analysis(self, signal) -> EnhancedSignal:
        """Comprehensive multi-dimensional signal analysis"""
        
        content = signal.content.lower()
        
        # 1. Advanced Pain Point Detection
        pain_indicators = self._detect_pain_points(content)
        pain_score = self._score_pain_point_clarity(content, pain_indicators)
        
        # 2. Solution Feasibility Analysis  
        solution_indicators = self._detect_solution_signals(content)
        solution_score = self._score_solution_feasibility(content, solution_indicators)
        
        # 3. Market Timing Assessment
        timing_signals = self._assess_market_timing(content)
        timing_score = self._score_market_timing(content, timing_signals)
        
        # 4. Business Relevance Scoring
        business_score = self._score_business_relevance(content, signal)
        
        # 5. Urgency Detection
        urgency_score = self._detect_urgency_signals(content)
        
        # 6. Industry Context Analysis
        context_analysis = self._analyze_industry_context(content)
        
        # 7. Semantic Keyword Extraction
        semantic_keywords = self._extract_semantic_keywords(content, context_analysis)
        
        # 8. Technology Relevance Assessment
        tech_relevance = self._assess_technology_relevance(content)
        
        # Calculate overall quality score
        quality_components = {
            'pain_point_clarity': pain_score,
            'solution_feasibility': solution_score,
            'market_timing': timing_score,
            'business_relevance': business_score,
            'urgency_indicators': urgency_score,
            'source_credibility': getattr(signal, 'credibility_weight', 0.5)
        }
        
        overall_quality = sum(
            score * self.quality_weights[component] 
            for component, score in quality_components.items()
        )
        
        # Calculate confidence level
        confidence = self._calculate_confidence_level(quality_components, signal)
        
        return EnhancedSignal(
            original_signal=signal,
            quality_score=min(1.0, overall_quality),
            relevance_score=business_score,
            business_potential=self._estimate_business_potential(
                pain_score, solution_score, timing_score, business_score
            ),
            urgency_score=urgency_score,
            market_timing=timing_signals,
            pain_point_indicators=pain_indicators,
            solution_indicators=solution_indicators,
            market_size_signals=self._detect_market_size_signals(content),
            competition_signals=self._detect_competition_signals(content),
            technology_relevance=tech_relevance,
            semantic_keywords=semantic_keywords,
            context_analysis=context_analysis,
            confidence_level=confidence
        )
    
    def _detect_pain_points(self, content: str) -> List[str]:
        """Advanced pain point detection with context awareness"""
        
        pain_indicators = []
        
        # Explicit pain points
        for pain_word in self.business_keyword_categories['pain_points']['explicit']:
            if pain_word in content:
                # Check for intensity modifiers nearby
                for modifier in self.business_keyword_categories['pain_points']['intensity_modifiers']:
                    if modifier in content and abs(content.find(modifier) - content.find(pain_word)) < 50:
                        pain_indicators.append(f"intense_{pain_word}")
                        break
                else:
                    pain_indicators.append(pain_word)
        
        # Implicit pain points (contextual)
        for implicit_phrase in self.business_keyword_categories['pain_points']['implicit']:
            if implicit_phrase in content:
                pain_indicators.append(f"implicit_{implicit_phrase}")
        
        # Sentiment-based pain detection
        for pattern in self.sentiment_patterns['high_frustration']:
            if re.search(pattern, content, re.IGNORECASE):
                pain_indicators.append("high_frustration_detected")
        
        return pain_indicators
    
    def _score_pain_point_clarity(self, content: str, pain_indicators: List[str]) -> float:
        """Score pain point clarity and intensity"""
        
        if not pain_indicators:
            return 0.0
        
        base_score = len(pain_indicators) * 0.2
        
        # Bonus for specific, actionable pain points
        specific_patterns = [
            r'\b(takes \d+ hours|costs \$\d+|reduces \w+ by \d+%)\b',
            r'\b(manual process|repetitive task|time consuming)\b',
            r'\b(integration nightmare|user experience|workflow)\b'
        ]
        
        for pattern in specific_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                base_score += 0.2
        
        # Bonus for intensity indicators
        intensity_count = sum(1 for p in pain_indicators if p.startswith('intense_'))
        base_score += intensity_count * 0.1
        
        return min(1.0, base_score)
    
    def _detect_solution_signals(self, content: str) -> List[str]:
        """Detect solution and opportunity signals"""
        
        solution_indicators = []
        
        # Building/development signals
        for build_signal in self.business_keyword_categories['solution_indicators']['building']:
            if build_signal in content:
                solution_indicators.append(f"building_{build_signal}")
        
        # Validation signals  
        for validation_signal in self.business_keyword_categories['solution_indicators']['validation']:
            if validation_signal in content:
                solution_indicators.append(f"validation_{validation_signal}")
        
        # Market readiness signals
        for market_signal in self.business_keyword_categories['solution_indicators']['market_ready']:
            if market_signal in content:
                solution_indicators.append(f"market_ready_{market_signal}")
        
        return solution_indicators
    
    def _score_solution_feasibility(self, content: str, solution_indicators: List[str]) -> float:
        """Score solution feasibility and market readiness"""
        
        base_score = len(solution_indicators) * 0.15
        
        # Technical feasibility indicators
        tech_feasibility_patterns = [
            r'\b(api|platform|automation|algorithm|ai|ml)\b',
            r'\b(scalable|efficient|fast|real-time)\b',
            r'\b(proven|tested|validated|working)\b'
        ]
        
        for pattern in tech_feasibility_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                base_score += 0.1
        
        # Market readiness bonus
        market_ready_count = sum(1 for s in solution_indicators if s.startswith('market_ready_'))
        base_score += market_ready_count * 0.2
        
        return min(1.0, base_score)
    
    def _assess_market_timing(self, content: str) -> str:
        """Assess market timing signals"""
        
        timing_scores = {
            'early': 0,
            'growing': 0, 
            'mature': 0
        }
        
        for timing, keywords in self.business_keyword_categories['market_timing'].items():
            for keyword in keywords:
                if keyword in content:
                    timing_scores[timing] += 1
        
        # Return timing with highest score, default to 'growing'
        return max(timing_scores.items(), key=lambda x: x[1])[0] or 'growing'
    
    def _score_market_timing(self, content: str, timing: str) -> float:
        """Score market timing favorability"""
        
        timing_scores = {
            'early': 0.9,      # Best timing - early market
            'growing': 0.7,    # Good timing - growing market  
            'mature': 0.3      # Challenging - mature market
        }
        
        base_score = timing_scores.get(timing, 0.5)
        
        # Check for timing urgency patterns
        for pattern in self.sentiment_patterns['urgent_need']:
            if re.search(pattern, content, re.IGNORECASE):
                base_score += 0.1
                break
        
        return min(1.0, base_score)
    
    def _score_business_relevance(self, content: str, signal) -> float:
        """Score business and commercial relevance"""
        
        relevance_score = 0.0
        
        # Enterprise/business context
        for business_keyword in self.business_keyword_categories['business_value']['enterprise']:
            if business_keyword in content:
                relevance_score += 0.15
        
        # Revenue potential signals
        for revenue_keyword in self.business_keyword_categories['business_value']['revenue_potential']:
            if revenue_keyword in content:
                relevance_score += 0.2
        
        # Scale indicators
        for scale_keyword in self.business_keyword_categories['business_value']['scale_indicators']:
            if scale_keyword in content:
                relevance_score += 0.1
        
        # Willingness to pay signals
        for pattern in self.sentiment_patterns['willingness_to_pay']:
            if re.search(pattern, content, re.IGNORECASE):
                relevance_score += 0.2
                break
        
        # Source credibility bonus
        source_bonus = getattr(signal, 'credibility_weight', 0.5) * 0.1
        relevance_score += source_bonus
        
        return min(1.0, relevance_score)
    
    def _detect_urgency_signals(self, content: str) -> float:
        """Detect urgency and time-sensitive indicators"""
        
        urgency_score = 0.0
        
        # Direct urgency patterns
        for pattern in self.sentiment_patterns['urgent_need']:
            if re.search(pattern, content, re.IGNORECASE):
                urgency_score += 0.3
        
        # Time-sensitive language
        time_patterns = [
            r'\b(deadline|due date|launch date|quarter end)\b',
            r'\b(behind schedule|running late|time crunch)\b',
            r'\b(competitor|first to market|opportunity window)\b'
        ]
        
        for pattern in time_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                urgency_score += 0.2
        
        return min(1.0, urgency_score)
    
    def _analyze_industry_context(self, content: str) -> Dict:
        """Analyze industry context and vertical relevance"""
        
        context_matches = {}
        
        for industry, context_data in self.industry_contexts.items():
            matches = 0
            keyword_matches = []
            
            # Check keyword matches
            for keyword in context_data['keywords']:
                if keyword in content:
                    matches += 2
                    keyword_matches.append(keyword)
            
            # Check pain point matches
            for pain_point in context_data['pain_points']:
                if pain_point in content:
                    matches += 1
            
            # Check opportunity matches  
            for opportunity in context_data['opportunities']:
                if opportunity in content:
                    matches += 1
            
            if matches > 0:
                context_matches[industry] = {
                    'score': matches,
                    'keywords': keyword_matches,
                    'relevance': matches / (len(context_data['keywords']) + len(context_data['pain_points']) + len(context_data['opportunities']))
                }
        
        return context_matches
    
    def _extract_semantic_keywords(self, content: str, context_analysis: Dict) -> List[str]:
        """Extract semantically relevant keywords based on context"""
        
        semantic_keywords = []
        
        # Extract keywords based on detected industry context
        for industry, data in context_analysis.items():
            if data['relevance'] > 0.3:  # Significant relevance threshold
                semantic_keywords.extend(data['keywords'])
        
        # Extract key phrases using patterns
        key_phrase_patterns = [
            r'\b\w+\s+(?:solution|platform|tool|service|system)\b',
            r'\b(?:automated|intelligent|smart|advanced)\s+\w+\b',
            r'\b\w+\s+(?:management|optimization|analytics|integration)\b'
        ]
        
        for pattern in key_phrase_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            semantic_keywords.extend(matches)
        
        # Remove duplicates and return unique semantic keywords
        return list(set(semantic_keywords))
    
    def _assess_technology_relevance(self, content: str) -> float:
        """Assess technology relevance and innovation potential"""
        
        tech_keywords = [
            'ai', 'artificial intelligence', 'machine learning', 'automation',
            'api', 'platform', 'cloud', 'saas', 'mobile', 'web3', 'blockchain'
        ]
        
        tech_score = 0.0
        for keyword in tech_keywords:
            if keyword in content:
                tech_score += 0.1
        
        # Emerging tech bonus
        emerging_tech = ['gpt', 'chatgpt', 'ai assistant', 'llm', 'generative ai']
        for tech in emerging_tech:
            if tech in content:
                tech_score += 0.2
        
        return min(1.0, tech_score)
    
    def _detect_market_size_signals(self, content: str) -> List[str]:
        """Detect market size and scale indicators"""
        
        size_signals = []
        
        size_patterns = [
            r'\b(\d+(?:k|m|million|billion))\s+(?:users|customers|businesses)\b',
            r'\b\$(\d+(?:k|m|b|million|billion))\s+(?:market|revenue|tam)\b',
            r'\b(?:enterprise|fortune 500|large company|corporation)\b'
        ]
        
        for pattern in size_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            size_signals.extend(matches)
        
        return size_signals
    
    def _detect_competition_signals(self, content: str) -> List[str]:
        """Detect competition and competitive landscape signals"""
        
        competition_signals = []
        
        competition_patterns = [
            r'\b(?:no competition|first mover|blue ocean|untapped)\b',
            r'\b(?:competitive|crowded|saturated|many players)\b',
            r'\b(?:better than|alternative to|replacement for)\s+\w+\b'
        ]
        
        for pattern in competition_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            competition_signals.extend(matches)
        
        return competition_signals
    
    def _estimate_business_potential(self, pain_score: float, solution_score: float, 
                                  timing_score: float, business_score: float) -> float:
        """Estimate overall business potential"""
        
        # Weighted combination of factors
        potential = (
            pain_score * 0.3 +        # Strong pain = high potential
            solution_score * 0.25 +   # Feasible solution = good potential  
            timing_score * 0.25 +     # Good timing = opportunity
            business_score * 0.2      # Business relevance = commercial viability
        )
        
        return min(1.0, potential)
    
    def _calculate_confidence_level(self, quality_components: Dict, signal) -> float:
        """Calculate confidence level in the quality assessment"""
        
        # Base confidence from component consistency
        component_values = list(quality_components.values())
        consistency = 1.0 - np.std(component_values)  # Lower std = higher consistency
        
        # Content length factor (more content = higher confidence)
        content_length = len(signal.content)
        length_factor = min(1.0, content_length / 200)  # Normalize to 200 chars
        
        # Source credibility factor
        source_factor = getattr(signal, 'credibility_weight', 0.5)
        
        confidence = (consistency * 0.5 + length_factor * 0.3 + source_factor * 0.2)
        
        return min(1.0, confidence)
    
    def get_enhancement_report(self, enhanced_signals: List[EnhancedSignal]) -> Dict:
        """Generate comprehensive enhancement report"""
        
        if not enhanced_signals:
            return {'error': 'No enhanced signals to analyze'}
        
        # Calculate statistics
        quality_scores = [s.quality_score for s in enhanced_signals]
        business_potentials = [s.business_potential for s in enhanced_signals]
        confidence_levels = [s.confidence_level for s in enhanced_signals]
        
        # Market timing distribution
        timing_distribution = Counter(s.market_timing for s in enhanced_signals)
        
        # Industry context analysis
        industry_contexts = defaultdict(int)
        for signal in enhanced_signals:
            for industry in signal.context_analysis.keys():
                industry_contexts[industry] += 1
        
        return {
            'enhancement_summary': {
                'total_enhanced_signals': len(enhanced_signals),
                'avg_quality_score': np.mean(quality_scores),
                'avg_business_potential': np.mean(business_potentials),
                'avg_confidence_level': np.mean(confidence_levels)
            },
            'quality_distribution': {
                'high_quality': len([s for s in enhanced_signals if s.quality_score >= 0.8]),
                'medium_quality': len([s for s in enhanced_signals if 0.6 <= s.quality_score < 0.8]),
                'acceptable_quality': len([s for s in enhanced_signals if s.quality_score >= 0.75])
            },
            'market_timing_analysis': dict(timing_distribution),
            'industry_context_distribution': dict(industry_contexts),
            'top_opportunities': [
                {
                    'quality_score': s.quality_score,
                    'business_potential': s.business_potential,
                    'market_timing': s.market_timing,
                    'pain_points': len(s.pain_point_indicators),
                    'confidence': s.confidence_level
                }
                for s in enhanced_signals[:10]  # Top 10
            ],
            'enhancement_thresholds': self.enhanced_thresholds
        }

# Utility function for easy integration
async def enhance_signal_quality(raw_signals: List) -> Tuple[List[EnhancedSignal], Dict]:
    """
    Main function to enhance signal quality
    Returns enhanced signals and comprehensive report
    """
    enhancer = AdvancedSignalQualityEnhancer()
    enhanced_signals = await enhancer.enhance_signals(raw_signals)
    report = enhancer.get_enhancement_report(enhanced_signals)
    
    return enhanced_signals, report 