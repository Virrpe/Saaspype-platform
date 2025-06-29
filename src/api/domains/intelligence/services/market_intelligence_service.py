#!/usr/bin/env python3
"""
Market Intelligence Service - Real-time market monitoring and analysis
Live updates on opportunity momentum, competition, and market dynamics
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set
import logging
from dataclasses import dataclass, asdict
from collections import defaultdict
import sqlite3
from threading import Lock

from src.api.domains.streaming.services.trend_detection_service import CrossPlatformTrendDetector, TrendOpportunity, TrendSignal

logger = logging.getLogger(__name__)

@dataclass
class MarketUpdate:
    """Real-time market update"""
    opportunity_id: str
    update_type: str  # "momentum_change", "competition_alert", "market_shift"
    severity: str  # "low", "medium", "high", "critical"
    title: str
    description: str
    data: Dict
    timestamp: datetime
    action_required: bool = False

@dataclass
class CompetitorAlert:
    """Competitor activity alert"""
    opportunity_keywords: List[str]
    competitor_name: str
    activity_type: str  # "new_product", "funding", "feature_launch"
    description: str
    impact_level: str  # "low", "medium", "high"
    source_url: str
    detected_at: datetime

@dataclass
class MomentumMetrics:
    """Opportunity momentum tracking"""
    opportunity_id: str
    current_score: float
    previous_score: float
    change_percentage: float
    trend_direction: str  # "rising", "falling", "stable"
    velocity: float  # Rate of change
    confidence_level: float
    last_updated: datetime

class RealTimeMarketIntelligence:
    """Real-time market intelligence and monitoring system"""
    
    def __init__(self):
        self.session = None  # Will be created lazily
        self.db_lock = Lock()
        self._trend_detector = None  # Will be created lazily
        
        # Monitoring configuration
        self.monitoring_config = {
            'update_interval': 300,  # 5 minutes
            'momentum_threshold': 0.15,  # 15% change triggers alert
            'competition_keywords': [
                'launched', 'funding', 'raised', 'acquired', 'partnership',
                'new feature', 'beta', 'product hunt', 'techcrunch'
            ],
            'market_shift_indicators': [
                'regulation', 'policy change', 'market crash', 'boom',
                'disruption', 'breakthrough', 'scandal', 'merger'
            ]
        }
        
        # Active monitoring state
        self.monitored_opportunities = {}
        self.momentum_history = defaultdict(list)
        self.competitor_tracking = defaultdict(list)
        self.market_alerts = []
        
        # Real-time data sources
        self.intelligence_sources = {
            'news_apis': {
                'enabled': True,
                'sources': ['techcrunch', 'venturebeat', 'techstartups']
            },
            'funding_data': {
                'enabled': True,
                'sources': ['crunchbase', 'pitchbook']
            },
            'social_signals': {
                'enabled': True,
                'sources': ['twitter', 'linkedin', 'reddit']
            },
            'product_launches': {
                'enabled': True,
                'sources': ['product_hunt', 'betalist', 'hacker_news']
            }
        }
        
        # Initialize database
        self._init_intelligence_db()
    
    def _init_intelligence_db(self):
        """Initialize market intelligence database"""
        try:
            conn = sqlite3.connect('market_intelligence.db')
            cursor = conn.cursor()
            
            # Market updates table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS market_updates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    opportunity_id TEXT,
                    update_type TEXT,
                    severity TEXT,
                    title TEXT,
                    description TEXT,
                    data TEXT,
                    timestamp DATETIME,
                    action_required BOOLEAN
                )
            ''')
            
            # Momentum tracking table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS momentum_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    opportunity_id TEXT,
                    momentum_score REAL,
                    change_percentage REAL,
                    trend_direction TEXT,
                    velocity REAL,
                    confidence_level REAL,
                    timestamp DATETIME
                )
            ''')
            
            # Competitor alerts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS competitor_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    opportunity_keywords TEXT,
                    competitor_name TEXT,
                    activity_type TEXT,
                    description TEXT,
                    impact_level TEXT,
                    source_url TEXT,
                    detected_at DATETIME
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Market intelligence database initialized")
            
        except Exception as e:
            logger.error(f"Error initializing intelligence database: {e}")
    
    async def start_real_time_monitoring(self, opportunities: List[TrendOpportunity]):
        """Start real-time monitoring for given opportunities"""
        logger.info(f"Starting real-time monitoring for {len(opportunities)} opportunities")
        
        # Store opportunities for monitoring
        for opp in opportunities:
            opp_id = self._generate_opportunity_id(opp)
            self.monitored_opportunities[opp_id] = opp
            
            # Initialize momentum tracking
            initial_momentum = MomentumMetrics(
                opportunity_id=opp_id,
                current_score=opp.momentum_score,
                previous_score=opp.momentum_score,
                change_percentage=0.0,
                trend_direction="stable",
                velocity=0.0,
                confidence_level=opp.confidence_level,
                last_updated=datetime.now()
            )
            self.momentum_history[opp_id].append(initial_momentum)
        
        # Start monitoring tasks
        monitoring_tasks = [
            self._monitor_momentum_changes(),
            self._monitor_competitor_activity(),
            self._monitor_market_shifts(),
            self._generate_intelligence_updates()
        ]
        
        await asyncio.gather(*monitoring_tasks)
    
    async def _monitor_momentum_changes(self):
        """Monitor momentum changes for tracked opportunities"""
        while True:
            try:
                logger.info("Checking momentum changes...")
                
                for opp_id, opportunity in self.monitored_opportunities.items():
                    # Re-analyze current momentum
                    current_trends = await self._get_trend_detector().detect_cross_platform_trends(hours_back=6)
                    
                    # Find matching opportunity in current trends
                    current_momentum = None
                    for trend in current_trends:
                        if self._opportunities_match(opportunity, trend):
                            current_momentum = trend.momentum_score
                            break
                    
                    if current_momentum is not None:
                        # Calculate momentum change
                        previous_momentum = self.momentum_history[opp_id][-1].current_score
                        change_percentage = ((current_momentum - previous_momentum) / previous_momentum) * 100
                        
                        # Determine trend direction and velocity
                        trend_direction = "stable"
                        if change_percentage > 5:
                            trend_direction = "rising"
                        elif change_percentage < -5:
                            trend_direction = "falling"
                        
                        velocity = abs(change_percentage) / 6  # Change per hour
                        
                        # Create momentum metrics
                        momentum_metrics = MomentumMetrics(
                            opportunity_id=opp_id,
                            current_score=current_momentum,
                            previous_score=previous_momentum,
                            change_percentage=change_percentage,
                            trend_direction=trend_direction,
                            velocity=velocity,
                            confidence_level=opportunity.confidence_level,
                            last_updated=datetime.now()
                        )
                        
                        self.momentum_history[opp_id].append(momentum_metrics)
                        
                        # Generate alert if significant change
                        if abs(change_percentage) > self.monitoring_config['momentum_threshold'] * 100:
                            await self._create_momentum_alert(opp_id, momentum_metrics)
                        
                        # Save to database
                        self._save_momentum_data(momentum_metrics)
                
                # Wait before next check
                await asyncio.sleep(self.monitoring_config['update_interval'])
                
            except Exception as e:
                logger.error(f"Error monitoring momentum changes: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    async def _monitor_competitor_activity(self):
        """Monitor competitor activity and new market entrants"""
        while True:
            try:
                logger.info("Monitoring competitor activity...")
                
                for opp_id, opportunity in self.monitored_opportunities.items():
                    # Search for competitor activity
                    competitor_signals = await self._detect_competitor_activity(opportunity)
                    
                    for signal in competitor_signals:
                        # Create competitor alert
                        alert = CompetitorAlert(
                            opportunity_keywords=opportunity.keywords,
                            competitor_name=signal.get('competitor_name', 'Unknown'),
                            activity_type=signal.get('activity_type', 'unknown'),
                            description=signal.get('description', ''),
                            impact_level=signal.get('impact_level', 'medium'),
                            source_url=signal.get('source_url', ''),
                            detected_at=datetime.now()
                        )
                        
                        self.competitor_tracking[opp_id].append(alert)
                        
                        # Generate market update
                        await self._create_competitor_alert(opp_id, alert)
                        
                        # Save to database
                        self._save_competitor_alert(alert)
                
                # Wait before next check
                await asyncio.sleep(self.monitoring_config['update_interval'] * 2)  # Check every 10 minutes
                
            except Exception as e:
                logger.error(f"Error monitoring competitor activity: {e}")
                await asyncio.sleep(120)  # Wait 2 minutes on error
    
    async def _monitor_market_shifts(self):
        """Monitor broader market shifts and regulatory changes"""
        while True:
            try:
                logger.info("Monitoring market shifts...")
                
                # Check for market-wide changes
                market_signals = await self._detect_market_shifts()
                
                for signal in market_signals:
                    # Determine affected opportunities
                    affected_opportunities = self._find_affected_opportunities(signal)
                    
                    for opp_id in affected_opportunities:
                        # Create market shift alert
                        await self._create_market_shift_alert(opp_id, signal)
                
                # Wait before next check
                await asyncio.sleep(self.monitoring_config['update_interval'] * 4)  # Check every 20 minutes
                
            except Exception as e:
                logger.error(f"Error monitoring market shifts: {e}")
                await asyncio.sleep(180)  # Wait 3 minutes on error
    
    async def _generate_intelligence_updates(self):
        """Generate periodic intelligence summaries"""
        while True:
            try:
                # Wait 1 hour between intelligence updates
                await asyncio.sleep(3600)
                
                logger.info("Generating intelligence updates...")
                
                for opp_id, opportunity in self.monitored_opportunities.items():
                    # Generate comprehensive update
                    intelligence_update = await self._generate_opportunity_intelligence(opp_id, opportunity)
                    
                    if intelligence_update:
                        self.market_alerts.append(intelligence_update)
                        self._save_market_update(intelligence_update)
                
            except Exception as e:
                logger.error(f"Error generating intelligence updates: {e}")
    
    async def _detect_competitor_activity(self, opportunity: TrendOpportunity) -> List[Dict]:
        """Detect competitor activity for an opportunity"""
        signals = []
        
        # Simulated competitor detection (would use real APIs in production)
        simulated_activities = [
            {
                'competitor_name': 'TechFlow Inc',
                'activity_type': 'new_product',
                'description': f'Launched new {opportunity.keywords[0]} automation tool',
                'impact_level': 'medium',
                'source_url': 'https://techcrunch.com/example'
            },
            {
                'competitor_name': 'StartupX',
                'activity_type': 'funding',
                'description': f'Raised $5M Series A for {opportunity.keywords[0]} platform',
                'impact_level': 'high',
                'source_url': 'https://venturebeat.com/example'
            }
        ]
        
        # Filter relevant activities
        for activity in simulated_activities:
            if any(keyword in activity['description'].lower() for keyword in opportunity.keywords):
                signals.append(activity)
        
        return signals
    
    async def _detect_market_shifts(self) -> List[Dict]:
        """Detect broader market shifts"""
        # Simulated market shift detection
        shifts = [
            {
                'type': 'regulatory_change',
                'description': 'New AI regulation announced affecting automation tools',
                'impact_keywords': ['ai', 'automation', 'machine learning'],
                'severity': 'medium'
            },
            {
                'type': 'market_trend',
                'description': 'Remote work adoption accelerating post-pandemic',
                'impact_keywords': ['remote work', 'collaboration', 'productivity'],
                'severity': 'high'
            }
        ]
        
        return shifts
    
    def _opportunities_match(self, opp1: TrendOpportunity, opp2: TrendOpportunity) -> bool:
        """Check if two opportunities are the same"""
        # Simple matching based on keywords overlap
        common_keywords = set(opp1.keywords) & set(opp2.keywords)
        return len(common_keywords) > 0
    
    def _generate_opportunity_id(self, opportunity: TrendOpportunity) -> str:
        """Generate unique ID for opportunity"""
        keywords_str = "_".join(sorted(opportunity.keywords))
        return f"opp_{hash(keywords_str) % 1000000}"
    
    def _find_affected_opportunities(self, market_signal: Dict) -> List[str]:
        """Find opportunities affected by market signal"""
        affected = []
        impact_keywords = market_signal.get('impact_keywords', [])
        
        for opp_id, opportunity in self.monitored_opportunities.items():
            if any(keyword in opportunity.keywords for keyword in impact_keywords):
                affected.append(opp_id)
        
        return affected
    
    async def _create_momentum_alert(self, opp_id: str, momentum: MomentumMetrics):
        """Create momentum change alert"""
        opportunity = self.monitored_opportunities[opp_id]
        
        severity = "low"
        if abs(momentum.change_percentage) > 30:
            severity = "high"
        elif abs(momentum.change_percentage) > 20:
            severity = "medium"
        
        direction = "increased" if momentum.change_percentage > 0 else "decreased"
        
        alert = MarketUpdate(
            opportunity_id=opp_id,
            update_type="momentum_change",
            severity=severity,
            title=f"Momentum Alert: {opportunity.title}",
            description=f"Opportunity momentum has {direction} by {abs(momentum.change_percentage):.1f}% in the last 6 hours",
            data={
                'previous_score': momentum.previous_score,
                'current_score': momentum.current_score,
                'change_percentage': momentum.change_percentage,
                'trend_direction': momentum.trend_direction,
                'velocity': momentum.velocity
            },
            timestamp=datetime.now(),
            action_required=severity in ['medium', 'high']
        )
        
        self.market_alerts.append(alert)
        self._save_market_update(alert)
        logger.info(f"Created momentum alert for {opp_id}: {momentum.change_percentage:.1f}% change")
    
    async def _create_competitor_alert(self, opp_id: str, competitor_alert: CompetitorAlert):
        """Create competitor activity alert"""
        opportunity = self.monitored_opportunities[opp_id]
        
        alert = MarketUpdate(
            opportunity_id=opp_id,
            update_type="competition_alert",
            severity=competitor_alert.impact_level,
            title=f"Competitor Alert: {competitor_alert.competitor_name}",
            description=f"New competitor activity detected: {competitor_alert.description}",
            data={
                'competitor_name': competitor_alert.competitor_name,
                'activity_type': competitor_alert.activity_type,
                'impact_level': competitor_alert.impact_level,
                'source_url': competitor_alert.source_url
            },
            timestamp=datetime.now(),
            action_required=competitor_alert.impact_level == 'high'
        )
        
        self.market_alerts.append(alert)
        self._save_market_update(alert)
        logger.info(f"Created competitor alert for {opp_id}: {competitor_alert.competitor_name}")
    
    async def _create_market_shift_alert(self, opp_id: str, market_signal: Dict):
        """Create market shift alert"""
        opportunity = self.monitored_opportunities[opp_id]
        
        alert = MarketUpdate(
            opportunity_id=opp_id,
            update_type="market_shift",
            severity=market_signal.get('severity', 'medium'),
            title=f"Market Shift: {market_signal.get('type', 'Unknown')}",
            description=market_signal.get('description', ''),
            data=market_signal,
            timestamp=datetime.now(),
            action_required=market_signal.get('severity') == 'high'
        )
        
        self.market_alerts.append(alert)
        self._save_market_update(alert)
        logger.info(f"Created market shift alert for {opp_id}")
    
    async def _generate_opportunity_intelligence(self, opp_id: str, opportunity: TrendOpportunity) -> Optional[MarketUpdate]:
        """Generate comprehensive intelligence update for opportunity"""
        # Get recent momentum data
        recent_momentum = self.momentum_history[opp_id][-5:]  # Last 5 data points
        
        # Get recent competitor activity
        recent_competitors = self.competitor_tracking[opp_id][-3:]  # Last 3 alerts
        
        # Generate intelligence summary
        intelligence_data = {
            'momentum_trend': self._analyze_momentum_trend(recent_momentum),
            'competitor_activity': len(recent_competitors),
            'market_position': self._assess_market_position(opportunity, recent_momentum),
            'recommendations': self._generate_recommendations(opportunity, recent_momentum, recent_competitors)
        }
        
        return MarketUpdate(
            opportunity_id=opp_id,
            update_type="intelligence_update",
            severity="low",
            title=f"Intelligence Update: {opportunity.title}",
            description="Comprehensive market intelligence analysis",
            data=intelligence_data,
            timestamp=datetime.now(),
            action_required=False
        )
    
    def _analyze_momentum_trend(self, momentum_data: List[MomentumMetrics]) -> str:
        """Analyze momentum trend over time"""
        if len(momentum_data) < 2:
            return "insufficient_data"
        
        recent_changes = [m.change_percentage for m in momentum_data[-3:]]
        avg_change = sum(recent_changes) / len(recent_changes)
        
        if avg_change > 10:
            return "strong_upward"
        elif avg_change > 5:
            return "moderate_upward"
        elif avg_change < -10:
            return "strong_downward"
        elif avg_change < -5:
            return "moderate_downward"
        else:
            return "stable"
    
    def _assess_market_position(self, opportunity: TrendOpportunity, momentum_data: List[MomentumMetrics]) -> str:
        """Assess current market position"""
        if not momentum_data:
            return "unknown"
        
        current_momentum = momentum_data[-1].current_score
        
        if current_momentum > 8:
            return "market_leader"
        elif current_momentum > 6:
            return "strong_position"
        elif current_momentum > 4:
            return "moderate_position"
        else:
            return "weak_position"
    
    def _generate_recommendations(self, opportunity: TrendOpportunity, momentum_data: List[MomentumMetrics], competitor_alerts: List[CompetitorAlert]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if momentum_data and momentum_data[-1].trend_direction == "rising":
            recommendations.append("Consider accelerating development timeline")
            recommendations.append("Increase marketing investment")
        
        if len(competitor_alerts) > 2:
            recommendations.append("Conduct competitive analysis")
            recommendations.append("Differentiate product positioning")
        
        if opportunity.market_timing == "hot":
            recommendations.append("Fast-track MVP development")
            recommendations.append("Secure funding quickly")
        
        return recommendations
    
    def _save_market_update(self, update: MarketUpdate):
        """Save market update to database"""
        try:
            with self.db_lock:
                conn = sqlite3.connect('market_intelligence.db')
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO market_updates 
                    (opportunity_id, update_type, severity, title, description, data, timestamp, action_required)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    update.opportunity_id,
                    update.update_type,
                    update.severity,
                    update.title,
                    update.description,
                    json.dumps(update.data),
                    update.timestamp.isoformat(),
                    update.action_required
                ))
                
                conn.commit()
                conn.close()
                
        except Exception as e:
            logger.error(f"Error saving market update: {e}")
    
    def _save_momentum_data(self, momentum: MomentumMetrics):
        """Save momentum data to database"""
        try:
            with self.db_lock:
                conn = sqlite3.connect('market_intelligence.db')
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO momentum_tracking 
                    (opportunity_id, momentum_score, change_percentage, trend_direction, velocity, confidence_level, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    momentum.opportunity_id,
                    momentum.current_score,
                    momentum.change_percentage,
                    momentum.trend_direction,
                    momentum.velocity,
                    momentum.confidence_level,
                    momentum.last_updated.isoformat()
                ))
                
                conn.commit()
                conn.close()
                
        except Exception as e:
            logger.error(f"Error saving momentum data: {e}")
    
    def _save_competitor_alert(self, alert: CompetitorAlert):
        """Save competitor alert to database"""
        try:
            with self.db_lock:
                conn = sqlite3.connect('market_intelligence.db')
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO competitor_alerts 
                    (opportunity_keywords, competitor_name, activity_type, description, impact_level, source_url, detected_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    json.dumps(alert.opportunity_keywords),
                    alert.competitor_name,
                    alert.activity_type,
                    alert.description,
                    alert.impact_level,
                    alert.source_url,
                    alert.detected_at.isoformat()
                ))
                
                conn.commit()
                conn.close()
                
        except Exception as e:
            logger.error(f"Error saving competitor alert: {e}")
    
    async def get_live_market_updates(self, hours_back: int = 24) -> List[MarketUpdate]:
        """Get recent market updates"""
        try:
            conn = sqlite3.connect('market_intelligence.db')
            cursor = conn.cursor()
            
            since_time = (datetime.now() - timedelta(hours=hours_back)).isoformat()
            
            cursor.execute('''
                SELECT * FROM market_updates 
                WHERE timestamp > ? 
                ORDER BY timestamp DESC
            ''', (since_time,))
            
            rows = cursor.fetchall()
            conn.close()
            
            updates = []
            for row in rows:
                update = MarketUpdate(
                    opportunity_id=row[1],
                    update_type=row[2],
                    severity=row[3],
                    title=row[4],
                    description=row[5],
                    data=json.loads(row[6]),
                    timestamp=datetime.fromisoformat(row[7]),
                    action_required=bool(row[8])
                )
                updates.append(update)
            
            return updates
            
        except Exception as e:
            logger.error(f"Error getting market updates: {e}")
            return []
    
    async def get_opportunity_momentum(self, opportunity_id: str, days_back: int = 7) -> List[MomentumMetrics]:
        """Get momentum history for an opportunity"""
        try:
            conn = sqlite3.connect('market_intelligence.db')
            cursor = conn.cursor()
            
            since_time = (datetime.now() - timedelta(days=days_back)).isoformat()
            
            cursor.execute('''
                SELECT * FROM momentum_tracking 
                WHERE opportunity_id = ? AND timestamp > ?
                ORDER BY timestamp ASC
            ''', (opportunity_id, since_time))
            
            rows = cursor.fetchall()
            conn.close()
            
            momentum_data = []
            for row in rows:
                momentum = MomentumMetrics(
                    opportunity_id=row[1],
                    current_score=row[2],
                    previous_score=0,  # Would need to calculate
                    change_percentage=row[3],
                    trend_direction=row[4],
                    velocity=row[5],
                    confidence_level=row[6],
                    last_updated=datetime.fromisoformat(row[7])
                )
                momentum_data.append(momentum)
            
            return momentum_data
            
        except Exception as e:
            logger.error(f"Error getting momentum data: {e}")
            return []
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()

    def _get_trend_detector(self):
        """Get or create trend detector instance"""
        if self._trend_detector is None:
            self._trend_detector = CrossPlatformTrendDetector()
        return self._trend_detector

# Note: Global instance removed to prevent async session creation during import
# Use get_market_intelligence() from main.py instead 