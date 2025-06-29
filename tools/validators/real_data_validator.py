#!/usr/bin/env python3
"""
Real-Time Data Validation System - Groundbreaking Quality Assurance
Ensures data authenticity, quality, and reliability in real-time
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import logging
from dataclasses import dataclass, field
import hashlib
import re
from urllib.parse import urlparse
import numpy as np

logger = logging.getLogger(__name__)

@dataclass
class DataQualityMetrics:
    """Comprehensive data quality metrics"""
    authenticity_score: float  # 0-1, how authentic the data appears
    freshness_score: float     # 0-1, how recent the data is
    relevance_score: float     # 0-1, how relevant to business trends
    source_credibility: float  # 0-1, credibility of the source
    content_quality: float     # 0-1, quality of the content
    engagement_validity: float # 0-1, validity of engagement metrics
    overall_quality: float     # 0-1, weighted overall score
    
    # Detailed breakdowns
    quality_flags: List[str] = field(default_factory=list)
    validation_details: Dict = field(default_factory=dict)
    confidence_interval: Tuple[float, float] = (0.0, 0.0)

@dataclass
class ValidatedSignal:
    """Signal with comprehensive validation"""
    original_signal: object
    quality_metrics: DataQualityMetrics
    validation_timestamp: datetime
    is_verified: bool
    verification_method: str
    risk_level: str  # 'low', 'medium', 'high'
    recommended_action: str
    
class GroundbreakingDataValidator:
    """Revolutionary real-time data validation system"""
    
    def __init__(self):
        self.session = None
        
        # Validation thresholds
        self.quality_thresholds = {
            'minimum_overall_quality': 0.6,
            'minimum_authenticity': 0.7,
            'minimum_source_credibility': 0.5,
            'maximum_risk_tolerance': 0.3
        }
        
        # Source credibility database
        self.source_credibility_db = {
            'reddit.com': 0.75,
            'github.com': 0.95,
            'news.ycombinator.com': 0.90,
            'stackoverflow.com': 0.85,
            'dev.to': 0.80,
            'techcrunch.com': 0.85,
            'venturebeat.com': 0.80,
            'wired.com': 0.85,
            'medium.com': 0.70,
            'twitter.com': 0.65,
            'linkedin.com': 0.75
        }
        
        # Content quality patterns
        self.quality_patterns = {
            'high_quality_indicators': [
                r'\b(analysis|research|study|data|statistics|report)\b',
                r'\b(methodology|framework|algorithm|implementation)\b',
                r'\b(results|findings|conclusion|evidence)\b',
                r'\b(peer.reviewed|published|academic|scientific)\b'
            ],
            'low_quality_indicators': [
                r'\b(clickbait|viral|trending|hot)\b',
                r'\b(you won\'t believe|shocking|amazing|incredible)\b',
                r'\b(secret|hack|trick|cheat)\b',
                r'[!]{3,}|[?]{3,}|[A-Z]{10,}'
            ],
            'spam_indicators': [
                r'\b(buy now|limited time|act fast|don\'t miss)\b',
                r'\b(make money|get rich|earn \$\d+)\b',
                r'\b(free|discount|sale|offer)\b',
                r'bit\.ly|tinyurl|goo\.gl'
            ]
        }
        
        # Real-time validation cache
        self.validation_cache = {}
        self.cache_ttl = 3600  # 1 hour
        
        # Validation statistics
        self.validation_stats = {
            'total_validated': 0,
            'high_quality_count': 0,
            'medium_quality_count': 0,
            'low_quality_count': 0,
            'rejected_count': 0,
            'avg_validation_time_ms': 0.0
        }
    
    async def validate_signals_realtime(self, signals: List) -> List[ValidatedSignal]:
        """Validate signals in real-time with comprehensive quality checks"""
        
        print(f"🔍 Starting real-time validation of {len(signals)} signals...")
        
        self.session = aiohttp.ClientSession()
        
        try:
            validated_signals = []
            
            # Process signals in parallel batches
            batch_size = 10
            for i in range(0, len(signals), batch_size):
                batch = signals[i:i + batch_size]
                
                # Validate batch in parallel
                validation_tasks = [
                    self._validate_single_signal(signal) 
                    for signal in batch
                ]
                
                batch_results = await asyncio.gather(*validation_tasks, return_exceptions=True)
                
                for result in batch_results:
                    if isinstance(result, ValidatedSignal):
                        validated_signals.append(result)
                        self._update_validation_stats(result)
                    elif isinstance(result, Exception):
                        logger.error(f"Validation error: {result}")
            
            # Filter by quality
            high_quality_signals = [
                signal for signal in validated_signals 
                if signal.quality_metrics.overall_quality >= self.quality_thresholds['minimum_overall_quality']
            ]
            
            print(f"✅ Validation complete:")
            print(f"   📊 Total processed: {len(validated_signals)}")
            print(f"   🏆 High quality: {len(high_quality_signals)}")
            print(f"   📈 Quality rate: {len(high_quality_signals)/len(validated_signals)*100:.1f}%")
            
            return high_quality_signals
            
        finally:
            await self.session.close()
    
    async def _validate_single_signal(self, signal) -> ValidatedSignal:
        """Validate a single signal comprehensively"""
        
        start_time = time.time()
        
        try:
            # Check cache first
            signal_hash = self._generate_signal_hash(signal)
            if signal_hash in self.validation_cache:
                cache_entry = self.validation_cache[signal_hash]
                if time.time() - cache_entry['timestamp'] < self.cache_ttl:
                    return cache_entry['validated_signal']
            
            # Perform comprehensive validation
            quality_metrics = await self._calculate_quality_metrics(signal)
            
            # Determine verification status
            is_verified = quality_metrics.overall_quality >= self.quality_thresholds['minimum_overall_quality']
            
            # Determine risk level
            risk_level = self._calculate_risk_level(quality_metrics)
            
            # Generate recommendation
            recommendation = self._generate_recommendation(quality_metrics, risk_level)
            
            # Create validated signal
            validated_signal = ValidatedSignal(
                original_signal=signal,
                quality_metrics=quality_metrics,
                validation_timestamp=datetime.now(),
                is_verified=is_verified,
                verification_method='comprehensive_realtime',
                risk_level=risk_level,
                recommended_action=recommendation
            )
            
            # Cache result
            self.validation_cache[signal_hash] = {
                'validated_signal': validated_signal,
                'timestamp': time.time()
            }
            
            # Update timing stats
            validation_time = (time.time() - start_time) * 1000
            self._update_timing_stats(validation_time)
            
            return validated_signal
            
        except Exception as e:
            # Create fallback validated signal for failed validation
            fallback_metrics = DataQualityMetrics(
                authenticity_score=0.5,
                freshness_score=0.5,
                relevance_score=0.5,
                source_credibility=0.5,
                content_quality=0.5,
                engagement_validity=0.5,
                overall_quality=0.5,
                quality_flags=['VALIDATION_FAILED'],
                validation_details={'error': str(e)},
                confidence_interval=(0.3, 0.7)
            )
            
            return ValidatedSignal(
                original_signal=signal,
                quality_metrics=fallback_metrics,
                validation_timestamp=datetime.now(),
                is_verified=False,
                verification_method='fallback_due_to_error',
                risk_level='high',
                recommended_action='REVIEW - Validation failed'
            )
    
    async def _calculate_quality_metrics(self, signal) -> DataQualityMetrics:
        """Calculate comprehensive quality metrics"""
        
        # 1. Authenticity Score
        authenticity_score = await self._calculate_authenticity_score(signal)
        
        # 2. Freshness Score
        freshness_score = self._calculate_freshness_score(signal)
        
        # 3. Relevance Score
        relevance_score = self._calculate_relevance_score(signal)
        
        # 4. Source Credibility
        source_credibility = self._calculate_source_credibility(signal)
        
        # 5. Content Quality
        content_quality = self._calculate_content_quality(signal)
        
        # 6. Engagement Validity
        engagement_validity = self._calculate_engagement_validity(signal)
        
        # 7. Overall Quality (weighted combination)
        overall_quality = self._calculate_overall_quality({
            'authenticity': authenticity_score,
            'freshness': freshness_score,
            'relevance': relevance_score,
            'source_credibility': source_credibility,
            'content_quality': content_quality,
            'engagement_validity': engagement_validity
        })
        
        # Generate quality flags
        quality_flags = self._generate_quality_flags({
            'authenticity': authenticity_score,
            'freshness': freshness_score,
            'relevance': relevance_score,
            'source_credibility': source_credibility,
            'content_quality': content_quality,
            'engagement_validity': engagement_validity
        })
        
        # Calculate confidence interval
        confidence_interval = self._calculate_confidence_interval(overall_quality)
        
        return DataQualityMetrics(
            authenticity_score=authenticity_score,
            freshness_score=freshness_score,
            relevance_score=relevance_score,
            source_credibility=source_credibility,
            content_quality=content_quality,
            engagement_validity=engagement_validity,
            overall_quality=overall_quality,
            quality_flags=quality_flags,
            validation_details={
                'validation_method': 'comprehensive',
                'timestamp': datetime.now().isoformat(),
                'signal_source': signal.source,
                'content_length': len(signal.content)
            },
            confidence_interval=confidence_interval
        )
    
    async def _calculate_authenticity_score(self, signal) -> float:
        """Calculate authenticity score using multiple methods"""
        
        authenticity_factors = []
        
        # 1. URL validation
        if hasattr(signal, 'url') and signal.url:
            url_score = await self._validate_url_authenticity(signal.url)
            authenticity_factors.append(url_score)
        
        # 2. Content pattern analysis
        content_score = self._analyze_content_patterns(signal.content)
        authenticity_factors.append(content_score)
        
        # 3. Metadata consistency
        metadata_score = self._check_metadata_consistency(signal)
        authenticity_factors.append(metadata_score)
        
        # 4. Temporal consistency
        temporal_score = self._check_temporal_consistency(signal)
        authenticity_factors.append(temporal_score)
        
        try:
            return np.mean(authenticity_factors) if authenticity_factors else 0.5
        except Exception as e:
            logger.error(f"Authenticity calculation error: {e}")
            return 0.5
    
    async def _validate_url_authenticity(self, url: str) -> float:
        """Validate URL authenticity"""
        
        try:
            parsed_url = urlparse(url)
            
            # Check domain credibility
            domain = parsed_url.netloc.lower()
            base_score = 0.5
            
            # Known credible domains
            for credible_domain, score in self.source_credibility_db.items():
                if credible_domain in domain:
                    base_score = score
                    break
            
            # Check for suspicious patterns
            suspicious_patterns = [
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',  # IP addresses
                r'[a-z]{20,}',  # Very long random strings
                r'bit\.ly|tinyurl|goo\.gl',  # URL shorteners
                r'\.tk|\.ml|\.ga|\.cf'  # Suspicious TLDs
            ]
            
            for pattern in suspicious_patterns:
                if re.search(pattern, domain):
                    base_score *= 0.7  # Reduce score for suspicious patterns
            
            # Try to verify URL exists (with timeout)
            try:
                async with self.session.head(url, timeout=aiohttp.ClientTimeout(total=3)) as response:
                    if response.status == 200:
                        base_score *= 1.1  # Boost for accessible URLs
                    elif response.status >= 400:
                        base_score *= 0.8  # Reduce for error responses
            except:
                base_score *= 0.9  # Slight reduction for inaccessible URLs
            
            return min(1.0, base_score)
            
        except Exception as e:
            logger.warning(f"URL validation error: {e}")
            return 0.5
    
    def _calculate_freshness_score(self, signal) -> float:
        """Calculate freshness score based on timestamp"""
        
        if not hasattr(signal, 'timestamp') or not signal.timestamp:
            return 0.5
        
        # Calculate age in hours
        age_hours = (datetime.now() - signal.timestamp).total_seconds() / 3600
        
        # Freshness decay function
        if age_hours <= 1:
            return 1.0
        elif age_hours <= 6:
            return 0.9
        elif age_hours <= 24:
            return 0.7
        elif age_hours <= 72:
            return 0.5
        elif age_hours <= 168:  # 1 week
            return 0.3
        else:
            return 0.1
    
    def _calculate_relevance_score(self, signal) -> float:
        """Calculate relevance to business trends"""
        
        business_keywords = [
            'startup', 'business', 'saas', 'platform', 'api', 'tool', 'app',
            'revenue', 'growth', 'scale', 'market', 'customer', 'user',
            'ai', 'automation', 'machine learning', 'technology', 'innovation',
            'product', 'service', 'solution', 'problem', 'opportunity'
        ]
        
        content_lower = signal.content.lower()
        keyword_matches = sum(1 for keyword in business_keywords if keyword in content_lower)
        
        # Also check signal keywords if available
        if hasattr(signal, 'keywords') and signal.keywords:
            signal_keyword_matches = sum(1 for keyword in signal.keywords if keyword in business_keywords)
            keyword_matches += signal_keyword_matches
        
        # Normalize score
        max_possible_matches = min(len(business_keywords), 10)  # Cap at 10
        relevance_score = min(1.0, keyword_matches / max_possible_matches)
        
        return relevance_score
    
    def _calculate_source_credibility(self, signal) -> float:
        """Calculate source credibility"""
        
        source = signal.source.lower()
        
        # Direct lookup
        for credible_source, score in self.source_credibility_db.items():
            if credible_source.replace('.com', '') in source:
                return score
        
        # Default score for unknown sources
        return 0.5
    
    def _calculate_content_quality(self, signal) -> float:
        """Calculate content quality score"""
        
        content = signal.content
        quality_score = 0.5  # Base score
        
        # Length check
        if len(content) < 20:
            quality_score *= 0.7  # Too short
        elif len(content) > 1000:
            quality_score *= 0.9  # Very long might be spam
        elif 50 <= len(content) <= 500:
            quality_score *= 1.2  # Good length
        
        # High quality indicators
        for pattern in self.quality_patterns['high_quality_indicators']:
            if re.search(pattern, content, re.IGNORECASE):
                quality_score *= 1.1
        
        # Low quality indicators
        for pattern in self.quality_patterns['low_quality_indicators']:
            if re.search(pattern, content, re.IGNORECASE):
                quality_score *= 0.8
        
        # Spam indicators
        for pattern in self.quality_patterns['spam_indicators']:
            if re.search(pattern, content, re.IGNORECASE):
                quality_score *= 0.6
        
        # Grammar and structure (simplified)
        sentences = content.count('.') + content.count('!') + content.count('?')
        words = len(content.split())
        
        if sentences > 0 and words > 0:
            avg_sentence_length = words / sentences
            if 5 <= avg_sentence_length <= 25:  # Reasonable sentence length
                quality_score *= 1.1
        
        return min(1.0, quality_score)
    
    def _calculate_engagement_validity(self, signal) -> float:
        """Calculate engagement validity score"""
        
        if not hasattr(signal, 'engagement_score'):
            return 0.5
        
        engagement = signal.engagement_score
        
        # Basic sanity checks
        if engagement < 0:
            return 0.0  # Negative engagement is invalid
        
        if engagement == 0:
            return 0.3  # Zero engagement might be valid but suspicious
        
        # Check for reasonable engagement ranges by source
        source_engagement_ranges = {
            'reddit': (1, 10000),
            'github': (1, 5000),
            'hacker_news': (1, 1000),
            'stackoverflow': (1, 500),
            'dev_to': (1, 1000)
        }
        
        source = signal.source.lower()
        for source_name, (min_eng, max_eng) in source_engagement_ranges.items():
            if source_name in source:
                if min_eng <= engagement <= max_eng:
                    return 1.0
                elif engagement > max_eng:
                    return 0.7  # Suspiciously high
                else:
                    return 0.8  # Low but valid
        
        # Default validation for unknown sources
        if 1 <= engagement <= 1000:
            return 0.9
        elif engagement > 1000:
            return 0.6  # Suspiciously high for unknown source
        else:
            return 0.5
    
    def _calculate_overall_quality(self, scores: Dict[str, float]) -> float:
        """Calculate weighted overall quality score"""
        
        weights = {
            'authenticity': 0.25,
            'source_credibility': 0.20,
            'content_quality': 0.20,
            'relevance': 0.15,
            'engagement_validity': 0.10,
            'freshness': 0.10
        }
        
        overall = sum(scores[metric] * weights[metric] for metric in scores)
        return min(1.0, overall)
    
    def _generate_quality_flags(self, scores: Dict[str, float]) -> List[str]:
        """Generate quality flags based on scores"""
        
        flags = []
        
        if scores['authenticity'] < 0.6:
            flags.append('LOW_AUTHENTICITY')
        
        if scores['source_credibility'] < 0.5:
            flags.append('UNTRUSTED_SOURCE')
        
        if scores['content_quality'] < 0.5:
            flags.append('LOW_CONTENT_QUALITY')
        
        if scores['relevance'] < 0.3:
            flags.append('LOW_RELEVANCE')
        
        if scores['engagement_validity'] < 0.5:
            flags.append('SUSPICIOUS_ENGAGEMENT')
        
        if scores['freshness'] < 0.3:
            flags.append('STALE_DATA')
        
        return flags
    
    def _calculate_confidence_interval(self, overall_quality: float) -> Tuple[float, float]:
        """Calculate confidence interval for quality score"""
        
        # Simplified confidence interval based on score
        margin = 0.1 if overall_quality > 0.7 else 0.15
        
        lower = max(0.0, overall_quality - margin)
        upper = min(1.0, overall_quality + margin)
        
        return (lower, upper)
    
    def _analyze_content_patterns(self, content: str) -> float:
        """Analyze content patterns for authenticity"""
        
        # Check for bot-like patterns
        bot_patterns = [
            r'^(.+)\1{3,}',  # Repeated phrases
            r'[A-Z]{10,}',   # All caps words
            r'(.)\1{5,}',    # Repeated characters
            r'\b\w{1,2}\b(\s+\b\w{1,2}\b){5,}'  # Too many short words
        ]
        
        authenticity_score = 1.0
        
        for pattern in bot_patterns:
            if re.search(pattern, content):
                authenticity_score *= 0.8
        
        return max(0.1, authenticity_score)
    
    def _check_metadata_consistency(self, signal) -> float:
        """Check metadata consistency"""
        
        # Basic consistency checks
        consistency_score = 1.0
        
        # Check if source matches URL domain
        if hasattr(signal, 'url') and signal.url:
            try:
                domain = urlparse(signal.url).netloc.lower()
                source = signal.source.lower()
                
                if source not in domain and domain not in source:
                    consistency_score *= 0.7
            except:
                consistency_score *= 0.9
        
        return consistency_score
    
    def _check_temporal_consistency(self, signal) -> float:
        """Check temporal consistency"""
        
        if not hasattr(signal, 'timestamp'):
            return 0.5
        
        # Check if timestamp is reasonable
        now = datetime.now()
        signal_time = signal.timestamp
        
        # Future timestamps are suspicious
        if signal_time > now + timedelta(minutes=5):
            return 0.3
        
        # Very old timestamps might be suspicious depending on source
        age_days = (now - signal_time).days
        if age_days > 30:
            return 0.6
        
        return 1.0
    
    def _calculate_risk_level(self, quality_metrics: DataQualityMetrics) -> str:
        """Calculate risk level based on quality metrics"""
        
        if quality_metrics.overall_quality >= 0.8:
            return 'low'
        elif quality_metrics.overall_quality >= 0.6:
            return 'medium'
        else:
            return 'high'
    
    def _generate_recommendation(self, quality_metrics: DataQualityMetrics, risk_level: str) -> str:
        """Generate recommendation based on quality and risk"""
        
        if risk_level == 'low':
            return 'ACCEPT - High quality signal, safe to use'
        elif risk_level == 'medium':
            return 'REVIEW - Medium quality, manual review recommended'
        else:
            return 'REJECT - Low quality, high risk signal'
    
    def _generate_signal_hash(self, signal) -> str:
        """Generate hash for signal caching"""
        
        content_hash = hashlib.md5(signal.content.encode()).hexdigest()
        source_hash = hashlib.md5(signal.source.encode()).hexdigest()
        
        return f"{source_hash}_{content_hash}"[:16]
    
    def _update_validation_stats(self, validated_signal: ValidatedSignal) -> None:
        """Update validation statistics"""
        
        self.validation_stats['total_validated'] += 1
        
        quality = validated_signal.quality_metrics.overall_quality
        
        if quality >= 0.8:
            self.validation_stats['high_quality_count'] += 1
        elif quality >= 0.6:
            self.validation_stats['medium_quality_count'] += 1
        else:
            self.validation_stats['low_quality_count'] += 1
        
        if not validated_signal.is_verified:
            self.validation_stats['rejected_count'] += 1
    
    def _update_timing_stats(self, validation_time_ms: float) -> None:
        """Update timing statistics"""
        
        current_avg = self.validation_stats['avg_validation_time_ms']
        total_count = self.validation_stats['total_validated']
        
        if total_count <= 1:
            self.validation_stats['avg_validation_time_ms'] = validation_time_ms
        else:
            # Running average
            self.validation_stats['avg_validation_time_ms'] = (
                (current_avg * (total_count - 1) + validation_time_ms) / total_count
            )
    
    def get_validation_report(self) -> Dict:
        """Get comprehensive validation report"""
        
        total = self.validation_stats['total_validated']
        
        if total == 0:
            return {'error': 'No signals validated yet'}
        
        return {
            'validation_summary': {
                'total_signals_validated': total,
                'high_quality_signals': self.validation_stats['high_quality_count'],
                'medium_quality_signals': self.validation_stats['medium_quality_count'],
                'low_quality_signals': self.validation_stats['low_quality_count'],
                'rejected_signals': self.validation_stats['rejected_count']
            },
            'quality_rates': {
                'high_quality_rate': self.validation_stats['high_quality_count'] / total if total > 0 else 0.0,
                'medium_quality_rate': self.validation_stats['medium_quality_count'] / total if total > 0 else 0.0,
                'low_quality_rate': self.validation_stats['low_quality_count'] / total if total > 0 else 0.0,
                'rejection_rate': self.validation_stats['rejected_count'] / total if total > 0 else 0.0
            },
            'performance': {
                'avg_validation_time_ms': self.validation_stats['avg_validation_time_ms'],
                'cache_size': len(self.validation_cache)
            },
            'thresholds': self.quality_thresholds
        }

# Test the validation system
async def test_data_validation():
    """Test the data validation system"""
    
    validator = GroundbreakingDataValidator()
    
    # Mock signals for testing
    class MockSignal:
        def __init__(self, source, content, engagement_score, timestamp, url=None, keywords=None):
            self.source = source
            self.content = content
            self.engagement_score = engagement_score
            self.timestamp = timestamp
            self.url = url or f"https://{source}/test"
            self.keywords = keywords or []
    
    test_signals = [
        # High quality signals
        MockSignal('reddit', 'Comprehensive analysis of AI automation trends in customer service industry', 150, datetime.now() - timedelta(hours=2)),
        MockSignal('github', 'Machine learning framework for business process automation', 89, datetime.now() - timedelta(hours=1)),
        
        # Medium quality signals
        MockSignal('dev_to', 'How to build AI chatbots for startups', 45, datetime.now() - timedelta(hours=6)),
        MockSignal('stackoverflow', 'API integration best practices', 23, datetime.now() - timedelta(hours=12)),
        
        # Low quality signals
        MockSignal('unknown_source', 'AMAZING!!! You won\'t believe this new startup hack!!!', 5000, datetime.now() - timedelta(days=30)),
        MockSignal('suspicious_site', 'Make money fast with this secret method', 10000, datetime.now() + timedelta(hours=1))  # Future timestamp
    ]
    
    # Validate signals
    validated_signals = await validator.validate_signals_realtime(test_signals)
    
    print(f"\n🔍 VALIDATION RESULTS:")
    print(f"📊 Validated {len(validated_signals)} high-quality signals out of {len(test_signals)} total")
    
    for i, validated in enumerate(validated_signals, 1):
        metrics = validated.quality_metrics
        print(f"\n✅ Signal #{i}:")
        print(f"   📈 Overall Quality: {metrics.overall_quality:.3f}")
        print(f"   🔒 Authenticity: {metrics.authenticity_score:.3f}")
        print(f"   🏢 Source Credibility: {metrics.source_credibility:.3f}")
        print(f"   📝 Content Quality: {metrics.content_quality:.3f}")
        print(f"   ⚠️ Risk Level: {validated.risk_level}")
        print(f"   💡 Recommendation: {validated.recommended_action}")
        if metrics.quality_flags:
            print(f"   🚩 Flags: {', '.join(metrics.quality_flags)}")
    
    # Get validation report
    report = validator.get_validation_report()
    print(f"\n📋 VALIDATION REPORT:")
    print(f"High Quality Rate: {report['quality_rates']['high_quality_rate']:.1%}")
    print(f"Rejection Rate: {report['quality_rates']['rejection_rate']:.1%}")
    print(f"Avg Validation Time: {report['performance']['avg_validation_time_ms']:.1f}ms")

if __name__ == "__main__":
    asyncio.run(test_data_validation()) 