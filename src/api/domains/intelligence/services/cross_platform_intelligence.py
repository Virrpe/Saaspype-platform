#!/usr/bin/env python3
"""
Cross-Platform Intelligence Synthesis - Groundbreaking Method 2
Correlates signals across multiple platforms for comprehensive trend view
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set, Tuple
import logging
from dataclasses import dataclass, field
from collections import defaultdict
import hashlib
import numpy as np
from itertools import combinations

logger = logging.getLogger(__name__)

@dataclass
class CrossPlatformCorrelation:
    """Correlation between signals across platforms"""
    platforms: List[str]
    correlation_score: float  # 0-1, how correlated the signals are
    shared_keywords: List[str]
    temporal_alignment: float  # 0-1, how aligned in time
    sentiment_alignment: float  # 0-1, how aligned in sentiment
    engagement_ratio: float  # Relative engagement across platforms
    confidence_level: float  # 0-1, confidence in correlation
    correlation_type: str  # 'identical', 'similar', 'related', 'divergent'

@dataclass
class PlatformIntelligence:
    """Intelligence about a specific platform's behavior"""
    platform: str
    signal_volume: int
    avg_engagement: float
    dominant_topics: List[str]
    sentiment_bias: float  # Platform's general sentiment tendency
    credibility_score: float
    response_time: float  # How quickly trends appear on this platform
    influence_score: float  # How much this platform influences others

@dataclass
class UniversalTrend:
    """Trend that appears across multiple platforms"""
    trend_id: str
    title: str
    description: str
    platforms: List[str]
    correlation_score: float
    momentum_score: float
    universality_score: float  # How universal across platforms
    platform_specific_signals: Dict[str, List]
    cross_platform_keywords: List[str]
    trend_origin: str  # Which platform started the trend
    propagation_pattern: Dict[str, datetime]  # When trend appeared on each platform
    discovered_at: datetime

class CrossPlatformIntelligenceEngine:
    """Revolutionary cross-platform intelligence synthesis system"""
    
    def __init__(self):
        # Platform weights and characteristics
        self.platform_characteristics = {
            'reddit': {
                'weight': 0.3,
                'influence_score': 0.8,
                'response_time_hours': 2,
                'sentiment_bias': 0.0,  # Neutral
                'credibility': 0.75,
                'signal_types': ['discussions', 'pain_points', 'solutions']
            },
            'twitter': {
                'weight': 0.25,
                'influence_score': 0.9,
                'response_time_hours': 0.5,
                'sentiment_bias': 0.1,  # Slightly positive
                'credibility': 0.65,
                'signal_types': ['announcements', 'reactions', 'viral_content']
            },
            'github': {
                'weight': 0.2,
                'influence_score': 0.85,
                'response_time_hours': 6,
                'sentiment_bias': 0.0,  # Neutral
                'credibility': 0.95,
                'signal_types': ['technical_trends', 'tools', 'frameworks']
            },
            'hacker_news': {
                'weight': 0.15,
                'influence_score': 0.9,
                'response_time_hours': 1,
                'sentiment_bias': -0.1,  # Slightly critical
                'credibility': 0.9,
                'signal_types': ['tech_news', 'startup_trends', 'discussions']
            },
            'product_hunt': {
                'weight': 0.1,
                'influence_score': 0.7,
                'response_time_hours': 12,
                'sentiment_bias': 0.3,  # Positive (product launches)
                'credibility': 0.8,
                'signal_types': ['product_launches', 'innovations', 'tools']
            }
        }
        
        # Correlation thresholds
        self.correlation_thresholds = {
            'identical': 0.9,
            'similar': 0.7,
            'related': 0.5,
            'divergent': 0.3
        }
        
        # Cross-platform intelligence cache
        self.intelligence_cache = {}
        self.cache_ttl = 1800  # 30 minutes
        
        # Platform intelligence tracking
        self.platform_intelligence = {}
        
        # Universal trend tracking
        self.universal_trends = {}
        
    async def synthesize_cross_platform_intelligence(self, platform_signals: Dict[str, List]) -> Dict:
        """Main intelligence synthesis pipeline"""
        
        logger.info("🧠 Starting cross-platform intelligence synthesis...")
        
        try:
            # Step 1: Analyze individual platform intelligence
            platform_intel = await self._analyze_platform_intelligence(platform_signals)
            
            # Step 2: Find cross-platform correlations
            correlations = await self._find_cross_platform_correlations(platform_signals)
            
            # Step 3: Identify universal trends
            universal_trends = await self._identify_universal_trends(platform_signals, correlations)
            
            # Step 4: Calculate platform influence patterns
            influence_patterns = await self._analyze_influence_patterns(platform_signals, correlations)
            
            # Step 5: Generate intelligence synthesis
            synthesis = {
                'platform_intelligence': platform_intel,
                'cross_platform_correlations': correlations,
                'universal_trends': universal_trends,
                'influence_patterns': influence_patterns,
                'synthesis_metadata': {
                    'total_platforms': len(platform_signals),
                    'total_signals': sum(len(signals) for signals in platform_signals.values()),
                    'correlation_count': len(correlations),
                    'universal_trend_count': len(universal_trends),
                    'synthesis_timestamp': datetime.now(),
                    'quality_score': self._calculate_synthesis_quality(platform_intel, correlations)
                }
            }
            
            logger.info(f"✅ Cross-platform intelligence synthesis complete:")
            logger.info(f"   🔗 Correlations found: {len(correlations)}")
            logger.info(f"   🌍 Universal trends: {len(universal_trends)}")
            logger.info(f"   📊 Platform intelligence: {len(platform_intel)} platforms")
            
            return synthesis
            
        except Exception as e:
            logger.error(f"❌ Cross-platform intelligence synthesis error: {e}")
            return self._create_fallback_synthesis(platform_signals)
    
    async def _analyze_platform_intelligence(self, platform_signals: Dict[str, List]) -> Dict[str, PlatformIntelligence]:
        """Analyze intelligence for each platform"""
        
        platform_intel = {}
        
        for platform, signals in platform_signals.items():
            if not signals:
                continue
                
            try:
                # Calculate platform metrics
                signal_volume = len(signals)
                avg_engagement = np.mean([signal.engagement_score for signal in signals]) if signals else 0
                
                # Extract dominant topics
                all_keywords = []
                for signal in signals:
                    all_keywords.extend(signal.keywords)
                
                keyword_counts = defaultdict(int)
                for keyword in all_keywords:
                    keyword_counts[keyword] += 1
                
                dominant_topics = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                dominant_topics = [topic[0] for topic in dominant_topics]
                
                # Calculate sentiment bias
                sentiment_scores = [signal.sentiment_score for signal in signals if hasattr(signal, 'sentiment_score')]
                sentiment_bias = np.mean(sentiment_scores) - 0.5 if sentiment_scores else 0
                
                # Get platform characteristics
                characteristics = self.platform_characteristics.get(platform, {})
                
                intel = PlatformIntelligence(
                    platform=platform,
                    signal_volume=signal_volume,
                    avg_engagement=avg_engagement,
                    dominant_topics=dominant_topics,
                    sentiment_bias=sentiment_bias,
                    credibility_score=characteristics.get('credibility', 0.5),
                    response_time=characteristics.get('response_time_hours', 6),
                    influence_score=characteristics.get('influence_score', 0.5)
                )
                
                platform_intel[platform] = intel
                
            except Exception as e:
                logger.warning(f"Error analyzing platform intelligence for {platform}: {e}")
                continue
        
        return platform_intel
    
    async def _find_cross_platform_correlations(self, platform_signals: Dict[str, List]) -> List[CrossPlatformCorrelation]:
        """Find correlations between signals across platforms"""
        
        correlations = []
        platforms = list(platform_signals.keys())
        
        # Compare each pair of platforms
        for platform1, platform2 in combinations(platforms, 2):
            signals1 = platform_signals.get(platform1, [])
            signals2 = platform_signals.get(platform2, [])
            
            if not signals1 or not signals2:
                continue
            
            try:
                correlation = await self._calculate_platform_correlation(
                    platform1, signals1, platform2, signals2
                )
                
                if correlation and correlation.correlation_score > 0.3:
                    correlations.append(correlation)
                    
            except Exception as e:
                logger.warning(f"Error calculating correlation between {platform1} and {platform2}: {e}")
                continue
        
        # Sort by correlation score
        correlations.sort(key=lambda x: x.correlation_score, reverse=True)
        
        return correlations
    
    async def _calculate_platform_correlation(self, platform1: str, signals1: List, 
                                           platform2: str, signals2: List) -> Optional[CrossPlatformCorrelation]:
        """Calculate correlation between two platforms"""
        
        try:
            # Extract keywords from both platforms
            keywords1 = set()
            keywords2 = set()
            
            for signal in signals1:
                keywords1.update(signal.keywords)
            
            for signal in signals2:
                keywords2.update(signal.keywords)
            
            # Calculate keyword overlap
            shared_keywords = list(keywords1.intersection(keywords2))
            keyword_similarity = len(shared_keywords) / len(keywords1.union(keywords2)) if keywords1.union(keywords2) else 0
            
            # Calculate temporal alignment
            times1 = [signal.timestamp for signal in signals1]
            times2 = [signal.timestamp for signal in signals2]
            
            temporal_alignment = self._calculate_temporal_alignment(times1, times2)
            
            # Calculate sentiment alignment
            sentiments1 = [getattr(signal, 'sentiment_score', 0.5) for signal in signals1]
            sentiments2 = [getattr(signal, 'sentiment_score', 0.5) for signal in signals2]
            
            sentiment_alignment = self._calculate_sentiment_alignment(sentiments1, sentiments2)
            
            # Calculate engagement ratio
            avg_engagement1 = np.mean([signal.engagement_score for signal in signals1]) if signals1 else 0
            avg_engagement2 = np.mean([signal.engagement_score for signal in signals2]) if signals2 else 0
            
            engagement_ratio = min(avg_engagement1, avg_engagement2) / max(avg_engagement1, avg_engagement2, 1)
            
            # Overall correlation score
            correlation_score = (
                keyword_similarity * 0.4 +
                temporal_alignment * 0.3 +
                sentiment_alignment * 0.2 +
                engagement_ratio * 0.1
            )
            
            # Determine correlation type
            correlation_type = 'divergent'
            for corr_type, threshold in self.correlation_thresholds.items():
                if correlation_score >= threshold:
                    correlation_type = corr_type
                    break
            
            # Calculate confidence level
            confidence_level = min(1.0, (len(signals1) + len(signals2)) / 20)
            
            return CrossPlatformCorrelation(
                platforms=[platform1, platform2],
                correlation_score=correlation_score,
                shared_keywords=shared_keywords,
                temporal_alignment=temporal_alignment,
                sentiment_alignment=sentiment_alignment,
                engagement_ratio=engagement_ratio,
                confidence_level=confidence_level,
                correlation_type=correlation_type
            )
            
        except Exception as e:
            logger.error(f"Error calculating platform correlation: {e}")
            return None
    
    def _calculate_temporal_alignment(self, times1: List[datetime], times2: List[datetime]) -> float:
        """Calculate how aligned two sets of timestamps are"""
        
        if not times1 or not times2:
            return 0.0
        
        try:
            # Convert to hours since earliest timestamp
            all_times = times1 + times2
            earliest = min(all_times)
            
            hours1 = [(t - earliest).total_seconds() / 3600 for t in times1]
            hours2 = [(t - earliest).total_seconds() / 3600 for t in times2]
            
            # Calculate overlap in time windows
            min1, max1 = min(hours1), max(hours1)
            min2, max2 = min(hours2), max(hours2)
            
            overlap_start = max(min1, min2)
            overlap_end = min(max1, max2)
            
            if overlap_end <= overlap_start:
                return 0.0
            
            overlap_duration = overlap_end - overlap_start
            total_duration = max(max1, max2) - min(min1, min2)
            
            return overlap_duration / total_duration if total_duration > 0 else 0.0
            
        except Exception as e:
            logger.warning(f"Error calculating temporal alignment: {e}")
            return 0.0
    
    def _calculate_sentiment_alignment(self, sentiments1: List[float], sentiments2: List[float]) -> float:
        """Calculate how aligned two sets of sentiment scores are"""
        
        if not sentiments1 or not sentiments2:
            return 0.0
        
        try:
            avg1 = np.mean(sentiments1)
            avg2 = np.mean(sentiments2)
            
            # Calculate similarity (1 - absolute difference)
            return 1.0 - abs(avg1 - avg2)
            
        except Exception as e:
            logger.warning(f"Error calculating sentiment alignment: {e}")
            return 0.0
    
    async def _identify_universal_trends(self, platform_signals: Dict[str, List], 
                                       correlations: List[CrossPlatformCorrelation]) -> List[UniversalTrend]:
        """Identify trends that appear across multiple platforms"""
        
        universal_trends = []
        
        try:
            # Group correlations by shared keywords
            keyword_groups = defaultdict(list)
            
            for correlation in correlations:
                for keyword in correlation.shared_keywords:
                    keyword_groups[keyword].append(correlation)
            
            # Identify universal trends
            for keyword, keyword_correlations in keyword_groups.items():
                if len(keyword_correlations) >= 2:  # Appears in multiple correlations
                    
                    # Get all platforms involved
                    involved_platforms = set()
                    for correlation in keyword_correlations:
                        involved_platforms.update(correlation.platforms)
                    
                    if len(involved_platforms) >= 3:  # Universal = 3+ platforms
                        
                        # Calculate universality metrics
                        avg_correlation = np.mean([c.correlation_score for c in keyword_correlations])
                        universality_score = len(involved_platforms) / len(platform_signals)
                        
                        # Find trend origin (earliest appearance)
                        earliest_platform = None
                        earliest_time = None
                        propagation_pattern = {}
                        
                        for platform in involved_platforms:
                            platform_signals_list = platform_signals.get(platform, [])
                            keyword_signals = [s for s in platform_signals_list if keyword in s.keywords]
                            
                            if keyword_signals:
                                platform_earliest = min(s.timestamp for s in keyword_signals)
                                propagation_pattern[platform] = platform_earliest
                                
                                if earliest_time is None or platform_earliest < earliest_time:
                                    earliest_time = platform_earliest
                                    earliest_platform = platform
                        
                        # Calculate momentum across platforms
                        total_engagement = 0
                        total_signals = 0
                        
                        for platform in involved_platforms:
                            platform_signals_list = platform_signals.get(platform, [])
                            keyword_signals = [s for s in platform_signals_list if keyword in s.keywords]
                            
                            total_engagement += sum(s.engagement_score for s in keyword_signals)
                            total_signals += len(keyword_signals)
                        
                        momentum_score = min(10.0, total_engagement / max(total_signals, 1))
                        
                        # Create universal trend
                        trend = UniversalTrend(
                            trend_id=hashlib.md5(f"{keyword}_{len(involved_platforms)}".encode()).hexdigest()[:8],
                            title=f"Universal Trend: {keyword.title()}",
                            description=f"Trending across {len(involved_platforms)} platforms with {avg_correlation:.2f} correlation",
                            platforms=list(involved_platforms),
                            correlation_score=avg_correlation,
                            momentum_score=momentum_score,
                            universality_score=universality_score,
                            platform_specific_signals={
                                platform: [s for s in platform_signals.get(platform, []) if keyword in s.keywords]
                                for platform in involved_platforms
                            },
                            cross_platform_keywords=[keyword],
                            trend_origin=earliest_platform or 'unknown',
                            propagation_pattern=propagation_pattern,
                            discovered_at=datetime.now()
                        )
                        
                        universal_trends.append(trend)
            
            # Sort by universality and momentum
            universal_trends.sort(key=lambda x: (x.universality_score * x.momentum_score), reverse=True)
            
        except Exception as e:
            logger.error(f"Error identifying universal trends: {e}")
        
        return universal_trends
    
    async def _analyze_influence_patterns(self, platform_signals: Dict[str, List], 
                                        correlations: List[CrossPlatformCorrelation]) -> Dict:
        """Analyze how platforms influence each other"""
        
        influence_patterns = {
            'platform_influence_scores': {},
            'trend_propagation_paths': [],
            'influence_network': {},
            'temporal_influence_analysis': {}
        }
        
        try:
            # Calculate platform influence scores
            for platform in platform_signals.keys():
                characteristics = self.platform_characteristics.get(platform, {})
                base_influence = characteristics.get('influence_score', 0.5)
                
                # Adjust based on signal volume and engagement
                signals = platform_signals[platform]
                if signals:
                    volume_factor = min(1.0, len(signals) / 100)
                    engagement_factor = min(1.0, np.mean([s.engagement_score for s in signals]) / 100)
                    
                    adjusted_influence = base_influence * (0.5 + 0.3 * volume_factor + 0.2 * engagement_factor)
                else:
                    adjusted_influence = base_influence * 0.5
                
                influence_patterns['platform_influence_scores'][platform] = adjusted_influence
            
            # Analyze trend propagation paths
            for correlation in correlations:
                if correlation.correlation_score > 0.7:  # Strong correlation
                    platform1, platform2 = correlation.platforms
                    
                    # Determine direction based on response times
                    char1 = self.platform_characteristics.get(platform1, {})
                    char2 = self.platform_characteristics.get(platform2, {})
                    
                    response1 = char1.get('response_time_hours', 6)
                    response2 = char2.get('response_time_hours', 6)
                    
                    if response1 < response2:
                        propagation_path = f"{platform1} → {platform2}"
                    elif response2 < response1:
                        propagation_path = f"{platform2} → {platform1}"
                    else:
                        propagation_path = f"{platform1} ↔ {platform2}"
                    
                    influence_patterns['trend_propagation_paths'].append({
                        'path': propagation_path,
                        'correlation_score': correlation.correlation_score,
                        'shared_keywords': correlation.shared_keywords
                    })
            
        except Exception as e:
            logger.error(f"Error analyzing influence patterns: {e}")
        
        return influence_patterns
    
    def _calculate_synthesis_quality(self, platform_intel: Dict, correlations: List) -> float:
        """Calculate overall quality of the intelligence synthesis"""
        
        try:
            # Quality factors
            platform_coverage = len(platform_intel) / len(self.platform_characteristics)
            correlation_strength = np.mean([c.correlation_score for c in correlations]) if correlations else 0
            data_volume = sum(intel.signal_volume for intel in platform_intel.values())
            volume_factor = min(1.0, data_volume / 100)
            
            quality_score = (
                platform_coverage * 0.4 +
                correlation_strength * 0.3 +
                volume_factor * 0.3
            )
            
            return min(1.0, quality_score)
            
        except Exception as e:
            logger.warning(f"Error calculating synthesis quality: {e}")
            return 0.5
    
    def _create_fallback_synthesis(self, platform_signals: Dict[str, List]) -> Dict:
        """Create fallback synthesis when main process fails"""
        
        return {
            'platform_intelligence': {},
            'cross_platform_correlations': [],
            'universal_trends': [],
            'influence_patterns': {},
            'synthesis_metadata': {
                'total_platforms': len(platform_signals),
                'total_signals': sum(len(signals) for signals in platform_signals.values()),
                'correlation_count': 0,
                'universal_trend_count': 0,
                'synthesis_timestamp': datetime.now(),
                'quality_score': 0.1,
                'fallback_mode': True
            }
        }

# Export the main class
__all__ = ['CrossPlatformIntelligenceEngine'] 