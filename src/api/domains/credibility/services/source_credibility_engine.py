"""
Source Credibility Engine - Luciq Groundbreaking Methods Phase 1 Task 4
Revolutionary platform credibility scoring and historical reliability tracking system.
"""

import json
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import numpy as np

@dataclass
class CredibilityScore:
    """Comprehensive credibility scoring for data sources"""
    platform: str
    overall_score: float  # 0.0-1.0
    reliability_score: float  # Historical accuracy
    freshness_score: float  # How recent/current
    influence_score: float  # Platform reach/impact
    consistency_score: float  # Signal consistency
    verification_score: float  # External verification
    last_updated: datetime
    
    def to_dict(self):
        return {
            'platform': self.platform,
            'overall_score': self.overall_score,
            'reliability_score': self.reliability_score,
            'freshness_score': self.freshness_score,
            'influence_score': self.influence_score,
            'consistency_score': self.consistency_score,
            'verification_score': self.verification_score,
            'last_updated': self.last_updated.isoformat()
        }

@dataclass
class SourceReliabilityMetric:
    """Historical reliability tracking for sources"""
    source_id: str
    platform: str
    accuracy_rate: float
    signal_count: int
    false_positive_rate: float
    trend_prediction_accuracy: float
    last_verification: datetime
    reliability_trend: str  # 'improving', 'stable', 'declining'

class SourceCredibilityEngine:
    """
    Revolutionary Source Credibility Engine
    
    Implements dynamic platform credibility scoring with:
    - Historical reliability tracking
    - Multi-dimensional credibility assessment
    - Real-time source weighting
    - Trend-based credibility adjustment
    """
    
    def __init__(self, db_path: str = "luciq_credibility.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        
        # Platform base credibility scores (industry knowledge)
        self.base_platform_scores = {
            'reddit': {
                'base_credibility': 0.75,
                'influence_multiplier': 0.85,
                'freshness_decay': 0.1,  # How fast signals lose relevance
                'verification_weight': 0.8
            },
            'twitter': {
                'base_credibility': 0.70,
                'influence_multiplier': 0.95,
                'freshness_decay': 0.05,  # Very fresh content
                'verification_weight': 0.6
            },
            'github': {
                'base_credibility': 0.90,
                'influence_multiplier': 0.75,
                'freshness_decay': 0.15,
                'verification_weight': 0.95
            },
            'hackernews': {
                'base_credibility': 0.85,
                'influence_multiplier': 0.80,
                'freshness_decay': 0.08,
                'verification_weight': 0.85
            },
            'producthunt': {
                'base_credibility': 0.80,
                'influence_multiplier': 0.70,
                'freshness_decay': 0.12,
                'verification_weight': 0.75
            },
            'devto': {
                'base_credibility': 0.78,
                'influence_multiplier': 0.65,
                'freshness_decay': 0.15,
                'verification_weight': 0.80
            },
            'stackoverflow': {
                'base_credibility': 0.92,
                'influence_multiplier': 0.85,
                'freshness_decay': 0.20,
                'verification_weight': 0.90
            },
            'indiehackers': {
                'base_credibility': 0.82,
                'influence_multiplier': 0.70,
                'freshness_decay': 0.10,
                'verification_weight': 0.85
            }
        }
        
        # Initialize database
        self._init_database()
        
        # Load historical data
        self.platform_scores = self._load_platform_scores()
        self.source_reliability = self._load_source_reliability()
        
        self.logger.info("SourceCredibilityEngine initialized with dynamic scoring")
    
    def _init_database(self):
        """Initialize SQLite database for credibility tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Platform credibility scores table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS platform_credibility (
            platform TEXT PRIMARY KEY,
            overall_score REAL,
            reliability_score REAL,
            freshness_score REAL,
            influence_score REAL,
            consistency_score REAL,
            verification_score REAL,
            last_updated TEXT,
            total_signals INTEGER DEFAULT 0,
            verified_signals INTEGER DEFAULT 0,
            false_positives INTEGER DEFAULT 0
        )
        ''')
        
        # Source reliability tracking table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS source_reliability (
            source_id TEXT PRIMARY KEY,
            platform TEXT,
            accuracy_rate REAL,
            signal_count INTEGER,
            false_positive_rate REAL,
            trend_prediction_accuracy REAL,
            last_verification TEXT,
            reliability_trend TEXT,
            created_at TEXT,
            updated_at TEXT
        )
        ''')
        
        # Signal verification history table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS signal_verification (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            signal_id TEXT,
            platform TEXT,
            source_id TEXT,
            predicted_trend TEXT,
            actual_outcome TEXT,
            verification_date TEXT,
            accuracy_score REAL,
            notes TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
        
        self.logger.info("Credibility database initialized")
    
    def _load_platform_scores(self) -> Dict[str, CredibilityScore]:
        """Load existing platform scores or initialize with base scores"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM platform_credibility')
        rows = cursor.fetchall()
        
        platform_scores = {}
        
        if not rows:
            # Initialize with base scores
            for platform, config in self.base_platform_scores.items():
                score = CredibilityScore(
                    platform=platform,
                    overall_score=config['base_credibility'],
                    reliability_score=config['base_credibility'],
                    freshness_score=0.8,  # Default freshness
                    influence_score=config['influence_multiplier'],
                    consistency_score=0.75,  # Default consistency
                    verification_score=config['verification_weight'],
                    last_updated=datetime.now()
                )
                platform_scores[platform] = score
                
                # Save to database
                cursor.execute('''
                INSERT INTO platform_credibility 
                (platform, overall_score, reliability_score, freshness_score, 
                 influence_score, consistency_score, verification_score, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    platform, score.overall_score, score.reliability_score,
                    score.freshness_score, score.influence_score, 
                    score.consistency_score, score.verification_score,
                    score.last_updated.isoformat()
                ))
        else:
            # Load existing scores
            for row in rows:
                platform_scores[row[0]] = CredibilityScore(
                    platform=row[0],
                    overall_score=row[1],
                    reliability_score=row[2],
                    freshness_score=row[3],
                    influence_score=row[4],
                    consistency_score=row[5],
                    verification_score=row[6],
                    last_updated=datetime.fromisoformat(row[7])
                )
        
        conn.commit()
        conn.close()
        
        self.logger.info(f"Loaded credibility scores for {len(platform_scores)} platforms")
        return platform_scores
    
    def _load_source_reliability(self) -> Dict[str, SourceReliabilityMetric]:
        """Load source reliability metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM source_reliability')
        rows = cursor.fetchall()
        
        source_reliability = {}
        for row in rows:
            source_reliability[row[0]] = SourceReliabilityMetric(
                source_id=row[0],
                platform=row[1],
                accuracy_rate=row[2],
                signal_count=row[3],
                false_positive_rate=row[4],
                trend_prediction_accuracy=row[5],
                last_verification=datetime.fromisoformat(row[6]),
                reliability_trend=row[7]
            )
        
        conn.close()
        return source_reliability
    
    def calculate_platform_credibility(self, platform: str, 
                                     recent_signals: List[Dict] = None) -> CredibilityScore:
        """
        Calculate comprehensive platform credibility score
        
        Args:
            platform: Platform name
            recent_signals: Recent signals from this platform for analysis
            
        Returns:
            CredibilityScore with multi-dimensional assessment
        """
        if platform not in self.base_platform_scores:
            # Unknown platform - conservative score
            return CredibilityScore(
                platform=platform,
                overall_score=0.5,
                reliability_score=0.5,
                freshness_score=0.5,
                influence_score=0.5,
                consistency_score=0.5,
                verification_score=0.5,
                last_updated=datetime.now()
            )
        
        config = self.base_platform_scores[platform]
        existing_score = self.platform_scores.get(platform)
        
        # Calculate reliability score based on historical data
        reliability_score = self._calculate_reliability_score(platform)
        
        # Calculate freshness score based on recent activity
        freshness_score = self._calculate_freshness_score(platform, recent_signals)
        
        # Influence score from platform configuration
        influence_score = config['influence_multiplier']
        
        # Consistency score based on signal patterns
        consistency_score = self._calculate_consistency_score(platform, recent_signals)
        
        # Verification score based on external validation
        verification_score = self._calculate_verification_score(platform)
        
        # Overall score weighted combination
        overall_score = (
            reliability_score * 0.30 +
            freshness_score * 0.15 +
            influence_score * 0.20 +
            consistency_score * 0.20 +
            verification_score * 0.15
        )
        
        credibility_score = CredibilityScore(
            platform=platform,
            overall_score=overall_score,
            reliability_score=reliability_score,
            freshness_score=freshness_score,
            influence_score=influence_score,
            consistency_score=consistency_score,
            verification_score=verification_score,
            last_updated=datetime.now()
        )
        
        # Update stored score
        self.platform_scores[platform] = credibility_score
        self._save_platform_score(credibility_score)
        
        return credibility_score
    
    def _calculate_reliability_score(self, platform: str) -> float:
        """Calculate platform reliability based on historical accuracy"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent verification data
        cursor.execute('''
        SELECT accuracy_score FROM signal_verification 
        WHERE platform = ? AND verification_date > ?
        ORDER BY verification_date DESC LIMIT 100
        ''', (platform, (datetime.now() - timedelta(days=30)).isoformat()))
        
        recent_scores = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        if not recent_scores:
            # No historical data - use base score
            return self.base_platform_scores[platform]['base_credibility']
        
        # Calculate weighted average (more recent = higher weight)
        weights = np.exp(np.linspace(-1, 0, len(recent_scores)))
        weighted_avg = np.average(recent_scores, weights=weights)
        
        return min(1.0, max(0.0, weighted_avg))
    
    def _calculate_freshness_score(self, platform: str, 
                                 recent_signals: List[Dict] = None) -> float:
        """Calculate platform freshness based on recent activity"""
        if not recent_signals:
            return 0.7  # Default freshness
        
        # Analyze signal timestamps
        now = datetime.now()
        signal_ages = []
        
        for signal in recent_signals:
            if 'timestamp' in signal:
                try:
                    signal_time = datetime.fromisoformat(signal['timestamp'])
                    age_hours = (now - signal_time).total_seconds() / 3600
                    signal_ages.append(age_hours)
                except:
                    continue
        
        if not signal_ages:
            return 0.7
        
        # Fresher signals = higher score
        avg_age = np.mean(signal_ages)
        freshness_score = max(0.0, 1.0 - (avg_age / 24.0))  # Decay over 24 hours
        
        return min(1.0, freshness_score)
    
    def _calculate_consistency_score(self, platform: str, 
                                   recent_signals: List[Dict] = None) -> float:
        """Calculate platform consistency based on signal patterns"""
        if not recent_signals or len(recent_signals) < 3:
            return 0.75  # Default consistency
        
        # Analyze signal quality consistency
        quality_scores = []
        for signal in recent_signals:
            if 'quality_score' in signal:
                quality_scores.append(signal['quality_score'])
        
        if len(quality_scores) < 3:
            return 0.75
        
        # Lower variance = higher consistency
        variance = np.var(quality_scores)
        consistency_score = max(0.0, 1.0 - variance)
        
        return min(1.0, consistency_score)
    
    def _calculate_verification_score(self, platform: str) -> float:
        """Calculate verification score based on external validation"""
        # Use base verification weight adjusted by recent performance
        base_score = self.base_platform_scores[platform]['verification_weight']
        
        # TODO: Add external verification logic here
        # For now, return base score
        return base_score
    
    def get_source_weight(self, platform: str, source_id: str = None) -> float:
        """
        Get dynamic weight for source based on credibility
        
        Args:
            platform: Platform name
            source_id: Specific source identifier (optional)
            
        Returns:
            Weight multiplier (0.0-2.0) for signal weighting
        """
        if platform not in self.platform_scores:
            credibility = self.calculate_platform_credibility(platform)
        else:
            credibility = self.platform_scores[platform]
        
        # Base weight from overall credibility
        base_weight = credibility.overall_score
        
        # Adjust for source-specific reliability if available
        if source_id and source_id in self.source_reliability:
            source_metric = self.source_reliability[source_id]
            source_modifier = source_metric.accuracy_rate * 0.3
            base_weight = base_weight * 0.7 + source_modifier
        
        # Scale to 0.0-2.0 range (allows boosting high-credibility sources)
        weight = base_weight * 2.0
        
        return min(2.0, max(0.1, weight))  # Minimum 0.1, maximum 2.0
    
    def record_signal_verification(self, signal_id: str, platform: str, 
                                 source_id: str, predicted_trend: str,
                                 actual_outcome: str, accuracy_score: float):
        """Record signal verification for credibility tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO signal_verification 
        (signal_id, platform, source_id, predicted_trend, actual_outcome, 
         verification_date, accuracy_score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            signal_id, platform, source_id, predicted_trend, 
            actual_outcome, datetime.now().isoformat(), accuracy_score
        ))
        
        conn.commit()
        conn.close()
        
        # Update source reliability
        self._update_source_reliability(source_id, platform, accuracy_score)
        
        self.logger.info(f"Recorded verification for {signal_id}: {accuracy_score}")
    
    def _update_source_reliability(self, source_id: str, platform: str, 
                                 accuracy_score: float):
        """Update source reliability metrics"""
        if source_id not in self.source_reliability:
            # New source
            self.source_reliability[source_id] = SourceReliabilityMetric(
                source_id=source_id,
                platform=platform,
                accuracy_rate=accuracy_score,
                signal_count=1,
                false_positive_rate=0.0 if accuracy_score > 0.5 else 1.0,
                trend_prediction_accuracy=accuracy_score,
                last_verification=datetime.now(),
                reliability_trend='stable'
            )
        else:
            # Update existing source
            metric = self.source_reliability[source_id]
            
            # Rolling average with decay
            decay_factor = 0.1
            metric.accuracy_rate = (
                metric.accuracy_rate * (1 - decay_factor) + 
                accuracy_score * decay_factor
            )
            metric.signal_count += 1
            metric.last_verification = datetime.now()
            
            # Update trend
            if accuracy_score > metric.accuracy_rate:
                metric.reliability_trend = 'improving'
            elif accuracy_score < metric.accuracy_rate * 0.9:
                metric.reliability_trend = 'declining'
            else:
                metric.reliability_trend = 'stable'
        
        # Save to database
        self._save_source_reliability(self.source_reliability[source_id])
    
    def _save_platform_score(self, score: CredibilityScore):
        """Save platform credibility score to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO platform_credibility 
        (platform, overall_score, reliability_score, freshness_score,
         influence_score, consistency_score, verification_score, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            score.platform, score.overall_score, score.reliability_score,
            score.freshness_score, score.influence_score,
            score.consistency_score, score.verification_score,
            score.last_updated.isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def _save_source_reliability(self, metric: SourceReliabilityMetric):
        """Save source reliability metric to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO source_reliability 
        (source_id, platform, accuracy_rate, signal_count, false_positive_rate,
         trend_prediction_accuracy, last_verification, reliability_trend, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metric.source_id, metric.platform, metric.accuracy_rate,
            metric.signal_count, metric.false_positive_rate,
            metric.trend_prediction_accuracy, metric.last_verification.isoformat(),
            metric.reliability_trend, datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def get_platform_credibility_report(self) -> Dict:
        """Generate comprehensive credibility report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_platforms': len(self.platform_scores),
            'platforms': {},
            'summary': {
                'highest_credibility': None,
                'lowest_credibility': None,
                'average_credibility': 0.0,
                'total_sources_tracked': len(self.source_reliability)
            }
        }
        
        scores = []
        for platform, score in self.platform_scores.items():
            platform_data = score.to_dict()
            
            # Add source count for this platform
            platform_sources = [s for s in self.source_reliability.values() 
                              if s.platform == platform]
            platform_data['source_count'] = len(platform_sources)
            platform_data['weight_multiplier'] = self.get_source_weight(platform)
            
            report['platforms'][platform] = platform_data
            scores.append(score.overall_score)
        
        if scores:
            report['summary']['average_credibility'] = np.mean(scores)
            
            best_platform = max(self.platform_scores.items(), 
                               key=lambda x: x[1].overall_score)
            worst_platform = min(self.platform_scores.items(), 
                                key=lambda x: x[1].overall_score)
            
            report['summary']['highest_credibility'] = {
                'platform': best_platform[0],
                'score': best_platform[1].overall_score
            }
            report['summary']['lowest_credibility'] = {
                'platform': worst_platform[0],
                'score': worst_platform[1].overall_score
            }
        
        return report
    
    def refresh_all_scores(self):
        """Refresh credibility scores for all platforms"""
        self.logger.info("Refreshing all platform credibility scores...")
        
        for platform in self.base_platform_scores.keys():
            self.calculate_platform_credibility(platform)
        
        self.logger.info("All credibility scores refreshed")

# Global instance for easy access
credibility_engine = None

def get_credibility_engine():
    """Get global credibility engine instance"""
    global credibility_engine
    if credibility_engine is None:
        credibility_engine = SourceCredibilityEngine()
    return credibility_engine

if __name__ == "__main__":
    # Test the credibility engine
    engine = SourceCredibilityEngine()
    
    print("🎯 Source Credibility Engine Test")
    print("=" * 50)
    
    # Test platform scoring
    for platform in ['reddit', 'twitter', 'github', 'hackernews']:
        score = engine.calculate_platform_credibility(platform)
        weight = engine.get_source_weight(platform)
        print(f"{platform}: {score.overall_score:.3f} (weight: {weight:.2f}x)")
    
    # Generate report
    report = engine.get_platform_credibility_report()
    print(f"\n📊 Report: {report['total_platforms']} platforms tracked")
    print(f"Average credibility: {report['summary']['average_credibility']:.3f}")
    
    if report['summary']['highest_credibility']:
        best = report['summary']['highest_credibility']
        print(f"Highest: {best['platform']} ({best['score']:.3f})")
    
    print("✅ Source Credibility Engine operational!") 