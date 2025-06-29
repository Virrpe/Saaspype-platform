#!/usr/bin/env python3
"""
Real-time Discovery Monitoring Service - Phase 3
Background service for continuous trend monitoring and alert generation
"""

import time
import json
import logging
import schedule
import sqlite3
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add the API directory to the path
api_dir = Path(__file__).parent.parent.parent / "apps" / "src" / "api"
sys.path.append(str(api_dir))

from trend_detector import run_trend_analysis, TrendDetectionEngine, RealTimeMonitor
from discovery_scraper import quick_discovery_scan

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('realtime_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RealTimeDiscoveryMonitor:
    """Real-time discovery monitoring service"""
    
    def __init__(self, config: dict = None):
        self.config = config or self._default_config()
        self.trend_engine = TrendDetectionEngine()
        self.monitor = RealTimeMonitor(self.trend_engine)
        self.running = False
        self.last_scan_time = None
        self.alert_history = []
        
        # Initialize monitoring
        self.monitor.start_monitoring(self.config['scan_interval_minutes'])
        
        logger.info(f"Real-time monitor initialized with {self.config['scan_interval_minutes']}-minute intervals")
    
    def _default_config(self) -> dict:
        """Default monitoring configuration"""
        return {
            'scan_interval_minutes': 30,
            'target_subreddits': ['startups', 'Entrepreneur', 'SaaS', 'smallbusiness', 'freelance'],
            'posts_per_scan': 5,
            'alert_thresholds': {
                'high_signal': 1.5,
                'trend_velocity': 0.5,
                'anomaly_factor': 2.0
            },
            'max_alerts_per_hour': 10,
            'enable_auto_discovery': True,
            'enable_trend_analysis': True,
            'enable_alert_generation': True
        }
    
    def start_monitoring(self):
        """Start the real-time monitoring service"""
        logger.info("🚀 Starting real-time discovery monitoring service...")
        self.running = True
        
        # Schedule periodic tasks
        schedule.every(self.config['scan_interval_minutes']).minutes.do(self._run_discovery_scan)
        schedule.every(15).minutes.do(self._run_trend_analysis)
        schedule.every(60).minutes.do(self._cleanup_old_data)
        
        logger.info(f"✅ Monitoring service started:")
        logger.info(f"   Discovery scans: every {self.config['scan_interval_minutes']} minutes")
        logger.info(f"   Trend analysis: every 15 minutes")
        logger.info(f"   Data cleanup: every 60 minutes")
        
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logger.info("🛑 Monitoring service stopped by user")
            self.stop_monitoring()
        except Exception as e:
            logger.error(f"❌ Monitoring service error: {e}")
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Stop the monitoring service"""
        self.running = False
        logger.info("🛑 Real-time monitoring service stopped")
    
    def _run_discovery_scan(self):
        """Run automated discovery scan"""
        if not self.config['enable_auto_discovery']:
            return
        
        try:
            logger.info("🔍 Running automated discovery scan...")
            
            # Scan each target subreddit
            new_opportunities = []
            for subreddit in self.config['target_subreddits']:
                try:
                    result = quick_discovery_scan(subreddit, self.config['posts_per_scan'])
                    if result.get('success'):
                        pain_points = result.get('pain_points', [])
                        new_opportunities.extend(pain_points)
                        logger.info(f"   📊 {subreddit}: {len(pain_points)} opportunities found")
                    
                except Exception as e:
                    logger.warning(f"   ⚠️  {subreddit} scan failed: {e}")
            
            # Store discovery results
            if new_opportunities:
                self._store_discovery_results(new_opportunities)
                logger.info(f"✅ Discovery scan complete: {len(new_opportunities)} total opportunities")
            else:
                logger.info("📭 Discovery scan complete: no new opportunities found")
            
            self.last_scan_time = datetime.now()
            
        except Exception as e:
            logger.error(f"❌ Discovery scan failed: {e}")
    
    def _run_trend_analysis(self):
        """Run trend analysis and generate alerts"""
        if not self.config['enable_trend_analysis']:
            return
        
        try:
            logger.info("📈 Running trend analysis...")
            
            # Run comprehensive trend analysis
            trend_report = run_trend_analysis(limit_sessions=50)
            
            if trend_report and trend_report.get('status') != 'fallback_analysis':
                # Generate alerts
                alerts = self._generate_alerts(trend_report)
                
                # Store trend analysis
                self._store_trend_analysis(trend_report)
                
                logger.info(f"✅ Trend analysis complete:")
                logger.info(f"   📊 {trend_report.get('data_points_analyzed', 0)} data points analyzed")
                logger.info(f"   🔥 {len(trend_report.get('trending_keywords', []))} trending keywords")
                logger.info(f"   📈 {len(trend_report.get('emerging_categories', []))} emerging categories")
                logger.info(f"   🚨 {len(alerts)} alerts generated")
                
                # Log top insights
                trending_keywords = trend_report.get('trending_keywords', [])
                if trending_keywords:
                    top_keyword = trending_keywords[0]
                    logger.info(f"   🔥 Top trending: {top_keyword.get('keyword', '')} (velocity: {top_keyword.get('velocity', 0):.2f})")
                
                market_insights = trend_report.get('market_insights', [])
                if market_insights:
                    logger.info(f"   💡 Market insight: {market_insights[0]}")
            
            else:
                logger.warning("⚠️  Trend analysis returned fallback results - insufficient data")
            
        except Exception as e:
            logger.error(f"❌ Trend analysis failed: {e}")
    
    def _generate_alerts(self, trend_report: dict) -> list:
        """Generate and process alerts from trend analysis"""
        if not self.config['enable_alert_generation']:
            return []
        
        try:
            # Check rate limiting
            recent_alerts = [a for a in self.alert_history if a['timestamp'] > datetime.now() - timedelta(hours=1)]
            if len(recent_alerts) >= self.config['max_alerts_per_hour']:
                logger.warning(f"⚠️  Alert rate limit reached: {len(recent_alerts)}/{self.config['max_alerts_per_hour']} per hour")
                return []
            
            # Generate alerts using the monitor
            alerts = self.monitor.check_for_alerts(trend_report)
            
            # Process and store alerts
            processed_alerts = []
            for alert in alerts:
                alert['timestamp'] = datetime.now()
                alert['id'] = f"alert_{int(time.time())}_{len(self.alert_history)}"
                
                # Store in history
                self.alert_history.append(alert)
                processed_alerts.append(alert)
                
                # Log alert
                severity_icon = {'high': '🚨', 'medium': '⚠️', 'low': '💡'}.get(alert.get('severity', 'medium'), '📢')
                logger.info(f"   {severity_icon} ALERT: {alert.get('message', '')}")
            
            # Store alerts in database
            if processed_alerts:
                self._store_alerts(processed_alerts)
            
            return processed_alerts
            
        except Exception as e:
            logger.error(f"❌ Alert generation failed: {e}")
            return []
    
    def _store_discovery_results(self, opportunities: list):
        """Store discovery results in database"""
        try:
            conn = sqlite3.connect(self.trend_engine.database_path)
            cursor = conn.cursor()
            
            # Create a monitoring session record
            session_data = {
                'opportunities': opportunities,
                'scan_timestamp': datetime.now().isoformat(),
                'subreddits_scanned': self.config['target_subreddits'],
                'monitoring_service': 'realtime_monitor',
                'posts_per_subreddit': self.config['posts_per_scan']
            }
            
            cursor.execute("""
                INSERT INTO discovery_sessions (
                    user_id, subreddit, posts_analyzed, pain_points_found, session_data
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                None,  # System user
                'monitoring_service',
                len(opportunities),
                len([o for o in opportunities if o.get('pain_point_indicators')]),
                json.dumps(session_data)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to store discovery results: {e}")
    
    def _store_trend_analysis(self, trend_report: dict):
        """Store trend analysis results"""
        try:
            # Add monitoring metadata
            trend_report['monitoring_metadata'] = {
                'service': 'realtime_monitor',
                'scan_interval': self.config['scan_interval_minutes'],
                'last_scan': self.last_scan_time.isoformat() if self.last_scan_time else None,
                'config': self.config
            }
            
            # Store using trend engine
            self.trend_engine._store_trend_analysis(trend_report)
            
        except Exception as e:
            logger.error(f"Failed to store trend analysis: {e}")
    
    def _store_alerts(self, alerts: list):
        """Store alerts in database"""
        try:
            conn = sqlite3.connect(self.trend_engine.database_path)
            cursor = conn.cursor()
            
            for alert in alerts:
                cursor.execute("""
                    INSERT INTO signal_alerts (
                        alert_type, signal_strength, trend_data, 
                        opportunity_summary, action_required
                    ) VALUES (?, ?, ?, ?, ?)
                """, (
                    alert.get('type', 'unknown'),
                    alert.get('data', {}).get('signal_strength', 0.0),
                    json.dumps(alert.get('data', {})),
                    alert.get('message', ''),
                    f"Review {alert.get('type', 'alert')} with {alert.get('severity', 'medium')} severity"
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to store alerts: {e}")
    
    def _cleanup_old_data(self):
        """Clean up old monitoring data"""
        try:
            logger.info("🧹 Cleaning up old monitoring data...")
            
            # Clean alert history (keep last 24 hours)
            cutoff_time = datetime.now() - timedelta(hours=24)
            self.alert_history = [a for a in self.alert_history if a['timestamp'] > cutoff_time]
            
            # Clean database (keep last 7 days of trend summaries)
            conn = sqlite3.connect(self.trend_engine.database_path)
            cursor = conn.cursor()
            
            cutoff_date = (datetime.now() - timedelta(days=7)).date()
            cursor.execute("DELETE FROM trend_summaries WHERE summary_date < ?", (cutoff_date,))
            
            # Clean old signal alerts (keep last 3 days)
            cutoff_timestamp = datetime.now() - timedelta(days=3)
            cursor.execute("DELETE FROM signal_alerts WHERE alert_timestamp < ?", (cutoff_timestamp,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Cleanup complete: {len(self.alert_history)} alerts in memory")
            
        except Exception as e:
            logger.error(f"❌ Cleanup failed: {e}")
    
    def get_status(self) -> dict:
        """Get current monitoring status"""
        return {
            'running': self.running,
            'last_scan_time': self.last_scan_time.isoformat() if self.last_scan_time else None,
            'alerts_in_memory': len(self.alert_history),
            'config': self.config,
            'uptime': datetime.now().isoformat()
        }

def main():
    """Main function to run the monitoring service"""
    print("🔍 Luciq Real-time Discovery Monitoring Service")
    print("=" * 60)
    
    # Load configuration
    config_file = Path(__file__).parent / "monitor_config.json"
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
        print(f"📋 Loaded configuration from {config_file}")
    else:
        config = None
        print("📋 Using default configuration")
    
    # Initialize and start monitor
    monitor = RealTimeDiscoveryMonitor(config)
    
    print(f"🚀 Starting monitoring service...")
    print(f"   Target subreddits: {monitor.config['target_subreddits']}")
    print(f"   Scan interval: {monitor.config['scan_interval_minutes']} minutes")
    print(f"   Posts per scan: {monitor.config['posts_per_scan']}")
    print(f"   Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        monitor.start_monitoring()
    except KeyboardInterrupt:
        print("\n🛑 Monitoring service stopped by user")
    except Exception as e:
        print(f"\n❌ Monitoring service failed: {e}")

if __name__ == "__main__":
    main() 