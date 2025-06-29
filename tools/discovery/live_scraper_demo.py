#!/usr/bin/env python3
"""
Live Scraper Demo - Real Data Collection & Database Storage
Collects real market opportunities and saves high-scoring ideas to database
"""

import sys
import os
sys.path.append('src')

import asyncio
import json
import sqlite3
from datetime import datetime
from typing import List, Dict

from api.domains.streaming.services.trend_detection_service import CrossPlatformTrendDetector

class LiveScraperDemo:
    """Live demonstration of scraper network with database storage"""
    
    def __init__(self):
        self.detector = CrossPlatformTrendDetector()
        self.db_path = "luciq_discovery.db"
        self.min_score_threshold = 7.0  # Only save high-quality opportunities
        self.min_confidence_threshold = 0.6  # Minimum confidence level
        
    def init_database(self):
        """Initialize database for storing opportunities"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create opportunities table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS live_opportunities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                momentum_score REAL,
                confidence_level REAL,
                market_timing TEXT,
                competition_density TEXT,
                revenue_potential TEXT,
                estimated_market_size TEXT,
                technical_complexity TEXT,
                keywords TEXT,
                sources TEXT,
                discovered_at TIMESTAMP,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized")
    
    def save_opportunity_to_db(self, opportunity):
        """Save high-scoring opportunity to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO live_opportunities 
            (title, description, momentum_score, confidence_level, market_timing, 
             competition_density, revenue_potential, estimated_market_size, 
             technical_complexity, keywords, sources, discovered_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            opportunity.title,
            opportunity.description,
            opportunity.momentum_score,
            opportunity.confidence_level,
            opportunity.market_timing,
            opportunity.competition_density,
            opportunity.revenue_potential,
            opportunity.estimated_market_size,
            opportunity.technical_complexity,
            json.dumps(opportunity.keywords),
            json.dumps(opportunity.sources),
            opportunity.discovered_at.isoformat()
        ))
        
        conn.commit()
        conn.close()
        print(f"💾 SAVED TO DATABASE: {opportunity.title}")
    
    def should_save_opportunity(self, opportunity) -> bool:
        """Determine if opportunity meets quality thresholds for saving"""
        # Check momentum score
        if opportunity.momentum_score < self.min_score_threshold:
            return False
            
        # Check confidence level
        if opportunity.confidence_level < self.min_confidence_threshold:
            return False
            
        # Prefer emerging/hot market timing
        if opportunity.market_timing in ['emerging', 'hot']:
            return True
            
        # High momentum can override timing
        if opportunity.momentum_score >= 8.5:
            return True
            
        # High revenue potential
        if 'High' in opportunity.revenue_potential or '$1M+' in opportunity.revenue_potential:
            return True
            
        return False
    
    async def run_live_demo(self):
        """Run live scraper demo with real data collection"""
        print("🚀 LIVE SCRAPER DEMO - REAL DATA COLLECTION")
        print("=" * 60)
        
        # Initialize database
        self.init_database()
        
        # Show active sources
        active_sources = [source for source, config in self.detector.data_sources.items() if config['enabled']]
        print(f"📊 Active Sources ({len(active_sources)}): {', '.join(active_sources)}")
        print(f"🎯 Quality Thresholds: Score ≥{self.min_score_threshold}, Confidence ≥{self.min_confidence_threshold}")
        print("\n🔄 Starting real-time data collection...")
        
        try:
            # Collect real data from all sources
            opportunities = await self.detector.detect_cross_platform_trends(hours_back=12)
            
            print(f"\n✅ COLLECTION COMPLETE: {len(opportunities)} opportunities found")
            
            # Score and filter opportunities
            high_quality_opportunities = []
            saved_count = 0
            
            print("\n🏆 OPPORTUNITY ANALYSIS & SCORING:")
            print("=" * 60)
            
            for i, opp in enumerate(opportunities):
                print(f"\n#{i+1} 📈 {opp.title}")
                print(f"   💰 Revenue: {opp.revenue_potential}")
                print(f"   📊 Market: {opp.estimated_market_size}")
                print(f"   🚀 Momentum: {opp.momentum_score:.1f}/10")
                print(f"   ⏰ Timing: {opp.market_timing}")
                print(f"   🏆 Competition: {opp.competition_density}")
                print(f"   🎯 Confidence: {opp.confidence_level:.2f}")
                print(f"   📍 Sources: {len(opp.sources)} platforms")
                print(f"   🔑 Keywords: {opp.keywords[:5]}")
                
                # Check if opportunity should be saved
                if self.should_save_opportunity(opp):
                    high_quality_opportunities.append(opp)
                    self.save_opportunity_to_db(opp)
                    saved_count += 1
                    print(f"   ✅ SAVED TO DATABASE (High Quality)")
                else:
                    print(f"   ⚠️  Below threshold (not saved)")
            
            # Summary
            print(f"\n📊 DEMO SUMMARY:")
            print("=" * 40)
            print(f"🔍 Total Opportunities Found: {len(opportunities)}")
            print(f"💾 High-Quality Saved to DB: {saved_count}")
            print(f"📈 Save Rate: {(saved_count/len(opportunities)*100):.1f}%")
            print(f"🎯 Average Momentum Score: {sum(opp.momentum_score for opp in opportunities)/len(opportunities):.1f}")
            
            if high_quality_opportunities:
                print(f"\n🏆 TOP SAVED OPPORTUNITIES:")
                for i, opp in enumerate(high_quality_opportunities[:3]):
                    print(f"   {i+1}. {opp.title} (Score: {opp.momentum_score:.1f})")
            
            # Show database status
            self.show_database_stats()
            
        except Exception as e:
            print(f"❌ Error during demo: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Clean up
            await self.detector.close()
            print("\n🧹 Cleanup complete")
    
    def show_database_stats(self):
        """Show current database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count total opportunities
        cursor.execute("SELECT COUNT(*) FROM live_opportunities")
        total_count = cursor.fetchone()[0]
        
        # Count by momentum score ranges
        cursor.execute("SELECT COUNT(*) FROM live_opportunities WHERE momentum_score >= 8.0")
        high_score_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM live_opportunities WHERE momentum_score >= 7.0 AND momentum_score < 8.0")
        medium_score_count = cursor.fetchone()[0]
        
        # Recent additions (last 24 hours)
        cursor.execute("SELECT COUNT(*) FROM live_opportunities WHERE saved_at >= datetime('now', '-1 day')")
        recent_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"\n💾 DATABASE STATUS:")
        print("=" * 30)
        print(f"📊 Total Opportunities: {total_count}")
        print(f"🏆 High Score (≥8.0): {high_score_count}")
        print(f"📈 Medium Score (7.0-8.0): {medium_score_count}")
        print(f"🕐 Added Last 24h: {recent_count}")

async def main():
    """Main demo function"""
    demo = LiveScraperDemo()
    await demo.run_live_demo()

if __name__ == "__main__":
    asyncio.run(main()) 