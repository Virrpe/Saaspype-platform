#!/usr/bin/env python3
"""
OVERNIGHT DISCOVERY CYCLE - Enhanced Multi-Platform Pain Point Analysis
Intelligent rate limiting, resource monitoring, and data accumulation across 15+ platforms
"""

import time
import json
import os
import psutil
import threading
import asyncio
from datetime import datetime, timedelta
import requests
from pathlib import Path
import random
from typing import List, Dict

class OvernightDiscoveryEngine:
    def __init__(self):
        self.running = False
        self.cycle_count = 0
        self.total_ideas = 0
        self.start_time = None
        self.data_dir = Path("overnight_discovery_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Safety limits (conservative for overnight)
        self.max_cpu_usage = 60  # Conservative CPU limit
        self.max_memory_usage = 85  # Memory limit (you're at 82.9% now)
        self.min_cycle_interval = 600  # 10 minutes minimum between cycles
        self.max_cycles_per_hour = 6  # Conservative rate limiting
        self.max_total_cycles = 50  # Safety limit for overnight
        
        # Enhanced multi-platform discovery settings
        self.platforms_per_cycle = 3  # Rotate through 3 platforms per cycle
        self.max_items_per_platform = 5  # Limit items per platform for performance
        
        # Platform rotation schedule (15+ platforms)
        self.all_platforms = [
            'reddit', 'twitter', 'hacker_news', 'github', 'product_hunt', 
            'indie_hackers', 'dev_to', 'stack_overflow', 'ycombinator',
            'medium', 'linkedin', 'quora', 'betalist', 'angellist', 'crunchbase'
        ]
        
        # Initialize multi-platform analyzer
        self.multi_platform_analyzer = None
        
        print("🌙 ENHANCED OVERNIGHT DISCOVERY ENGINE INITIALIZED")
        print(f"📁 Data directory: {self.data_dir}")
        print(f"🛡️ Safety limits: CPU<{self.max_cpu_usage}%, Memory<{self.max_memory_usage}%")
        print(f"⏱️ Min cycle interval: {self.min_cycle_interval}s ({self.min_cycle_interval/60:.1f} min)")
        print(f"🔄 Max cycles/hour: {self.max_cycles_per_hour}")
        print(f"🌐 Multi-platform: {len(self.all_platforms)} platforms available")
        print(f"🎯 Platforms per cycle: {self.platforms_per_cycle}")
    
    async def initialize_multi_platform_analyzer(self):
        """Initialize the multi-platform pain point analyzer"""
        try:
            # Import the enhanced analyzer
            import sys
            sys.path.append('.')
            from multi_platform_pain_analyzer import MultiPlatformPainAnalyzer
            
            self.multi_platform_analyzer = MultiPlatformPainAnalyzer()
            print("🧠 Multi-platform pain point analyzer initialized")
            return True
        except Exception as e:
            print(f"⚠️ Could not initialize multi-platform analyzer: {e}")
            print("🔄 Falling back to basic discovery methods")
            return False
    
    def check_system_health(self):
        """Check if system is healthy enough to continue"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('.').percent
        available_gb = psutil.virtual_memory().available / (1024**3)
        
        health_status = {
            'cpu_percent': cpu_percent,
            'memory_percent': memory_percent,
            'disk_percent': disk_percent,
            'available_gb': available_gb,
            'healthy': True,
            'warnings': []
        }
        
        if cpu_percent > self.max_cpu_usage:
            health_status['healthy'] = False
            health_status['warnings'].append(f"High CPU usage: {cpu_percent:.1f}%")
        
        if memory_percent > self.max_memory_usage:
            health_status['healthy'] = False
            health_status['warnings'].append(f"High memory usage: {memory_percent:.1f}%")
        
        if available_gb < 1.0:
            health_status['healthy'] = False
            health_status['warnings'].append(f"Low available memory: {available_gb:.1f} GB")
        
        if disk_percent > 90:
            health_status['healthy'] = False
            health_status['warnings'].append(f"Low disk space: {100-disk_percent:.1f}% free")
        
        return health_status
    
    async def safe_discovery_cycle(self):
        """Run a single safe discovery cycle with enhanced multi-platform analysis"""
        cycle_start = time.time()
        
        print(f"\n🔄 ENHANCED CYCLE #{self.cycle_count + 1} STARTING...")
        print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
        
        # Check system health before starting
        health = self.check_system_health()
        print(f"🏥 System: CPU {health['cpu_percent']:.1f}%, Memory {health['memory_percent']:.1f}%, Available {health['available_gb']:.1f}GB")
        
        if not health['healthy']:
            print(f"⚠️ SYSTEM HEALTH WARNING:")
            for warning in health['warnings']:
                print(f"   • {warning}")
            print("😴 Sleeping for 15 minutes to let system recover...")
            time.sleep(900)  # 15 minutes
            return False
        
        try:
            # Initialize multi-platform analyzer if not done
            if self.multi_platform_analyzer is None:
                await self.initialize_multi_platform_analyzer()
            
            # Run enhanced multi-platform discovery
            if self.multi_platform_analyzer:
                ideas_found = await self.run_enhanced_multi_platform_discovery()
            else:
                # Fallback to lightweight discovery
                ideas_found = await self.run_lightweight_discovery()
            
            # Save results
            self.save_cycle_results(ideas_found, health)
            
            self.cycle_count += 1
            self.total_ideas += len(ideas_found)
            
            cycle_duration = time.time() - cycle_start
            print(f"✅ Enhanced cycle completed in {cycle_duration:.1f}s")
            print(f"💡 Found {len(ideas_found)} high-quality pain points")
            print(f"📊 Total: {self.total_ideas} ideas in {self.cycle_count} cycles")
            
            return True
            
        except Exception as e:
            print(f"❌ Enhanced cycle failed: {e}")
            print("😴 Sleeping for 10 minutes before retry...")
            time.sleep(600)  # 10 minutes
            return False
    
    async def run_enhanced_multi_platform_discovery(self):
        """Run enhanced discovery across multiple platforms"""
        print("🧠 ENHANCED MULTI-PLATFORM DISCOVERY")
        print("-" * 50)
        
        # Select platforms for this cycle (rotate through all platforms)
        start_idx = (self.cycle_count * self.platforms_per_cycle) % len(self.all_platforms)
        cycle_platforms = []
        for i in range(self.platforms_per_cycle):
            idx = (start_idx + i) % len(self.all_platforms)
            cycle_platforms.append(self.all_platforms[idx])
        
        print(f"🎯 Analyzing platforms: {', '.join(cycle_platforms)}")
        
        all_pain_points = []
        
        try:
            # Use the mega scraper for comprehensive data collection
            print("📊 Phase 1: Multi-platform data collection...")
            
            # Run a lightweight version of the mega scraper (shorter time window)
            mega_results = await self.run_lightweight_mega_scraper(hours_back=6)  # Shorter window for overnight
            
            if mega_results and isinstance(mega_results, dict) and mega_results.get('opportunities'):
                opportunities = mega_results['opportunities']
                if isinstance(opportunities, list) and len(opportunities) > 0:
                    print(f"✅ Collected {len(opportunities)} opportunities from mega scraper")
                    
                    # Apply enhanced pain point analysis to the collected data
                    print("🧠 Phase 2: Enhanced pain point analysis...")
                    print(f"🎯 Processing {len(opportunities)} opportunities from enhanced mega scraper")
                    
                    for opportunity in opportunities[:20]:  # Limit for performance
                        # Convert opportunity to content item format
                        content_item = {
                            'title': opportunity.get('title', ''),
                            'description': opportunity.get('description', ''),
                            'source': opportunity.get('source', 'unknown'),
                            'url': opportunity.get('url', ''),
                            'score': opportunity.get('score', 0),
                            'platform_type': 'mega_scraper'
                        }
                        
                        # Apply enhanced analysis
                        analysis = await self.multi_platform_analyzer._analyze_content_item(content_item)
                        
                        if analysis and analysis['total_score'] >= 6:  # Quality threshold
                            pain_point = {
                                'title': f"Enhanced Discovery: {analysis['pain_point'][:60]}...",
                                'problem': analysis['pain_point'],
                                'solution': analysis['opportunity_description'],
                                'source': analysis['source_platform'],
                                'cycle': self.cycle_count + 1,
                                'timestamp': datetime.now().isoformat(),
                                'confidence_score': int(analysis['confidence'] * 10),
                                'discovery_type': 'enhanced_multi_platform',
                                
                                # Enhanced fields
                                'market_size_score': analysis['market_size'],
                                'urgency_score': analysis['urgency'],
                                'solution_gap_score': analysis['solution_gap'],
                                'monetization_score': analysis['monetization'],
                                'total_opportunity_score': analysis['total_score'],
                                'business_domain': analysis['domain'],
                                'platform_context': analysis['platform_context'],
                                'validation_signals': analysis['validation_signals'],
                                'source_url': content_item['url']
                            }
                            all_pain_points.append(pain_point)
                    
                    print(f"🎯 Enhanced analysis complete: {len(all_pain_points)} high-quality pain points identified")
            
            else:
                print("⚠️ Mega scraper returned no data, falling back to platform-specific discovery")
                # Fallback to platform-specific discovery
                for platform in cycle_platforms:
                    try:
                        platform_ideas = await self.discover_from_platform(platform)
                        all_pain_points.extend(platform_ideas)
                        print(f"   ✅ {platform}: {len(platform_ideas)} pain points")
                        
                        # Add delay between platforms
                        await asyncio.sleep(2)
                        
                    except Exception as e:
                        print(f"   ❌ {platform}: {e}")
                        continue
        
        except Exception as e:
            print(f"❌ Enhanced discovery failed: {e}")
            print("🔄 Falling back to basic discovery...")
            # Final fallback to basic discovery
            all_pain_points = await self.run_lightweight_discovery()
        
        # Sort by quality score
        all_pain_points.sort(key=lambda x: x.get('total_opportunity_score', x.get('confidence_score', 0)), reverse=True)
        
        print(f"🏆 Final results: {len(all_pain_points)} pain points across {len(set(p['source'] for p in all_pain_points))} platforms")
        
        return all_pain_points
    
    async def run_lightweight_mega_scraper(self, hours_back=6):
        """Run a lightweight version of the mega scraper for overnight cycles"""
        try:
            # Import and run mega scraper with reduced scope
            from mega_source_scraper import MegaSourceScraper
            
            mega_scraper = MegaSourceScraper()
            
            # Temporarily reduce the scope for overnight operation
            original_sources = mega_scraper.additional_sources.copy()
            
            # Enable only the fastest, most reliable sources for overnight
            fast_sources = ['ycombinator', 'medium', 'quora']
            for source_name in mega_scraper.additional_sources:
                if source_name not in fast_sources:
                    mega_scraper.additional_sources[source_name]['enabled'] = False
            
            print(f"🚀 Running lightweight mega scraper (fast sources only)...")
            results = await mega_scraper.scrape_all_sources(hours_back)
            
            # Restore original configuration
            mega_scraper.additional_sources = original_sources
            
            await mega_scraper.close()
            return results
            
        except Exception as e:
            print(f"⚠️ Lightweight mega scraper failed: {e}")
            return None
    
    async def discover_from_platform(self, platform):
        """Discover pain points from a specific platform"""
        ideas = []
        
        try:
            if platform == 'reddit':
                # Use enhanced Reddit discovery
                subreddits = ['startups', 'entrepreneur', 'smallbusiness', 'SaaS']
                selected_subreddit = subreddits[self.cycle_count % len(subreddits)]
                ideas = await self.discover_subreddit_ideas(selected_subreddit, limit=self.max_items_per_platform)
                
            elif platform in ['twitter', 'hacker_news', 'github', 'product_hunt', 'indie_hackers']:
                # Use core detector for these platforms
                ideas = await self.discover_from_core_platform(platform)
                
            else:
                # For other platforms, use basic discovery
                print(f"   🔄 {platform}: Using basic discovery (platform-specific integration needed)")
                
        except Exception as e:
            print(f"   ❌ Platform discovery failed for {platform}: {e}")
        
        return ideas
    
    async def discover_from_core_platform(self, platform):
        """Use the core trend detector for specific platforms"""
        try:
            from src.api.domains.streaming.services.trend_detection_service import CrossPlatformTrendDetector
            
            detector = CrossPlatformTrendDetector()
            
            # Get signals from specific platform
            if platform == 'twitter':
                signals = await detector._collect_twitter_signals(hours_back=6)
            elif platform == 'hacker_news':
                signals = await detector._collect_hacker_news_signals(hours_back=6)
            elif platform == 'github':
                signals = await detector._collect_github_signals(hours_back=6)
            elif platform == 'product_hunt':
                signals = await detector._collect_product_hunt_signals(hours_back=6)
            elif platform == 'indie_hackers':
                signals = await detector._collect_indiehackers_signals(hours_back=6)
            else:
                signals = []
            
            # Convert signals to pain points using enhanced analysis
            ideas = []
            for signal in signals[:self.max_items_per_platform]:
                content_item = {
                    'title': signal.content[:100],
                    'description': signal.content,
                    'source': platform,
                    'url': signal.url,
                    'score': signal.engagement_score,
                    'platform_type': 'core_detector'
                }
                
                # Apply enhanced analysis if available
                if self.multi_platform_analyzer:
                    analysis = await self.multi_platform_analyzer._analyze_content_item(content_item)
                    if analysis and analysis['total_score'] >= 6:
                        idea = {
                            'title': f"Platform Discovery: {analysis['pain_point'][:60]}...",
                            'problem': analysis['pain_point'],
                            'solution': analysis['opportunity_description'],
                            'source': platform,
                            'cycle': self.cycle_count + 1,
                            'timestamp': datetime.now().isoformat(),
                            'confidence_score': int(analysis['confidence'] * 10),
                            'discovery_type': f'{platform}_enhanced',
                            'total_opportunity_score': analysis['total_score'],
                            'business_domain': analysis['domain'],
                            'validation_signals': analysis['validation_signals']
                        }
                        ideas.append(idea)
            
            await detector.close()
            return ideas
            
        except Exception as e:
            print(f"   ❌ Core platform discovery failed for {platform}: {e}")
            return []

    async def run_lightweight_discovery(self):
        """Run a lightweight version of our discovery system (fallback)"""
        ideas = []
        
        # Rotate through different subreddits each cycle
        all_subreddits = [
            "entrepreneur", "startups", "smallbusiness", "freelance", "SaaS",
            "business", "marketing", "webdev", "productivity", "indiehackers",
            "sales", "ecommerce", "consulting", "remotework", "nocode",
            "digitalnomad", "passive_income", "sidehustle", "financialindependence"
        ]
        
        # Select different subreddits each cycle
        subreddits_per_cycle = 2
        start_idx = (self.cycle_count * subreddits_per_cycle) % len(all_subreddits)
        cycle_subreddits = []
        for i in range(subreddits_per_cycle):
            idx = (start_idx + i) % len(all_subreddits)
            cycle_subreddits.append(all_subreddits[idx])
        
        print(f"🎯 Fallback: Analyzing subreddits: {', '.join(cycle_subreddits)}")
        
        # Use our existing discovery system but lightweight
        for subreddit in cycle_subreddits:
            try:
                # Add delay to be nice to Reddit and reduce system load
                await asyncio.sleep(3)
                
                # Try to use our real discovery system
                subreddit_ideas = await self.discover_from_subreddit(subreddit)
                ideas.extend(subreddit_ideas)
                    
            except Exception as e:
                print(f"⚠️ Error with r/{subreddit}: {e}")
                print(f"🔄 Skipping r/{subreddit} - NO MOCK DATA, only real data")
                # Skip this subreddit completely - no mock data allowed
                continue
        
        return ideas
    
    async def discover_from_subreddit(self, subreddit):
        """Try to use our real discovery system for a subreddit"""
        ideas = []
        
        try:
            # Try to call our existing API
            response = requests.get(f"http://localhost:8000/api/discovery/subreddit/{subreddit}", 
                                  timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                # Process real API response
                for item in data.get('ideas', [])[:3]:  # Reduced for overnight
                    idea = {
                        'title': item.get('title', f'Discovery from r/{subreddit}'),
                        'problem': item.get('problem', 'Pain point identified'),
                        'solution': item.get('solution', 'Solution opportunity'),
                        'source': subreddit,
                        'cycle': self.cycle_count + 1,
                        'timestamp': datetime.now().isoformat(),
                        'confidence_score': item.get('score', 3),
                        'discovery_type': 'api_real'
                    }
                    ideas.append(idea)
            else:
                raise Exception(f"API returned {response.status_code}")
                
        except Exception as e:
            # Fallback to our existing scraping logic
            print(f"   API failed for r/{subreddit}, using real Reddit scraping")
            
            # Use our actual Reddit scraping system
            try:
                scraped_ideas = self.scrape_reddit_subreddit(subreddit)
                ideas.extend(scraped_ideas)
            except Exception as scrape_error:
                print(f"   ❌ Reddit scraping failed for r/{subreddit}: {scrape_error}")
                print(f"   🔄 Skipping r/{subreddit} - NO MOCK DATA, only real data")
                # NO FALLBACK TO MOCK DATA - we only want real data
                # If Reddit fails, we simply skip this subreddit and try others
                pass
        
        return ideas
    
    def scrape_reddit_subreddit(self, subreddit):
        """Scrape Reddit subreddit for real pain points and business ideas"""
        ideas = []
        
        try:
            # Use Reddit's JSON API (public, no auth needed)
            url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
            headers = {
                'User-Agent': 'Luciq Discovery Bot 1.0 (Business Idea Research)'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', {}).get('children', [])
                
                ideas_found = 0
                for post_data in posts:
                    if ideas_found >= 3:  # Reduced for overnight
                        break
                        
                    post = post_data.get('data', {})
                    title = post.get('title', '')
                    selftext = post.get('selftext', '')
                    
                    # Skip if no content
                    if not title or len(title) < 10:
                        continue
                    
                    # Look for pain points and problems
                    pain_indicators = ['problem', 'issue', 'struggle', 'difficult', 'hard', 'frustrating', 
                                     'annoying', 'hate', 'wish', 'need', 'want', 'looking for', 'help']
                    
                    text_to_check = (title + ' ' + selftext).lower()
                    has_pain_point = any(indicator in text_to_check for indicator in pain_indicators)
                    
                    # Generate business idea from the post
                    if has_pain_point or len(selftext) > 50:  # Either pain point or substantial content
                        idea = {
                            'title': f"Reddit Discovery: {title[:80]}{'...' if len(title) > 80 else ''}",
                            'problem': selftext[:200] + '...' if len(selftext) > 200 else selftext or title,
                            'solution': f"Business opportunity addressing r/{subreddit} community need",
                            'source': subreddit,
                            'cycle': self.cycle_count + 1,
                            'timestamp': datetime.now().isoformat(),
                            'confidence_score': 4 if has_pain_point else 3,
                            'discovery_type': 'reddit_scraping',
                            'reddit_url': f"https://reddit.com{post.get('permalink', '')}",
                            'reddit_score': post.get('score', 0),
                            'reddit_comments': post.get('num_comments', 0)
                        }
                        ideas.append(idea)
                        ideas_found += 1
                
                print(f"   ✅ Scraped {len(ideas)} real ideas from r/{subreddit}")
                
            else:
                raise Exception(f"Reddit API returned {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Reddit scraping failed: {e}")
            raise e
        
        return ideas

    async def discover_subreddit_ideas(self, subreddit: str, limit: int = 5) -> List[Dict]:
        """Discover business ideas from a subreddit using enhanced pain point analysis"""
        try:
            # Import here to avoid circular imports
            import sys
            sys.path.append('src')
            from api.domains.discovery.services.discovery_service import DiscoveryService
            
            # Use the enhanced discovery service
            discovery_service = DiscoveryService()
            
            # Run enhanced pain point discovery
            result = await discovery_service.discover_pain_points(subreddit, limit)
            
            # Convert to overnight discovery format
            ideas = []
            for pain_point in result.get('pain_points', []):
                idea = {
                    'title': f"Enhanced Discovery: {pain_point['title'][:60]}...",
                    'problem': pain_point['description'],
                    'solution': f"SaaS solution addressing {pain_point['industry']} pain point with {pain_point['total_score']}/10 opportunity score",
                    'source': subreddit,
                    'cycle': self.cycle_count,
                    'timestamp': datetime.now().isoformat(),
                    'confidence_score': int(pain_point['confidence'] * 10),  # Convert to 1-10 scale
                    'discovery_type': 'enhanced_llm_analysis',
                    'reddit_url': pain_point['url'],
                    'reddit_score': pain_point['reddit_metrics']['score'],
                    'reddit_comments': pain_point['reddit_metrics']['num_comments'],
                    
                    # Enhanced fields
                    'market_size_score': pain_point['market_size_score'],
                    'urgency_score': pain_point['urgency_score'],
                    'solution_gap_score': pain_point['solution_gap_score'],
                    'monetization_score': pain_point['monetization_score'],
                    'total_opportunity_score': pain_point['total_score'],
                    'business_domain': pain_point['industry'],
                    'validation_signals': pain_point['pain_indicators']
                }
                ideas.append(idea)
            
            # Also include opportunities
            for opportunity in result.get('ranked_opportunities', []):
                idea = {
                    'title': f"Market Discovery: {opportunity['title'][:60]}...",
                    'problem': f"Market opportunity in {opportunity['domain']} targeting {opportunity['target_market']}",
                    'solution': opportunity['title'],
                    'source': subreddit,
                    'cycle': self.cycle_count,
                    'timestamp': datetime.now().isoformat(),
                    'confidence_score': int(opportunity['confidence'] * 10),
                    'discovery_type': 'business_opportunity',
                    'reddit_url': '',
                    'reddit_score': opportunity['reddit_metrics']['score'],
                    'reddit_comments': opportunity['reddit_metrics']['num_comments'],
                    
                    # Enhanced fields
                    'market_size_score': opportunity['market_size'],
                    'urgency_score': opportunity['urgency'],
                    'solution_gap_score': opportunity['solution_gap'],
                    'monetization_score': opportunity['monetization'],
                    'total_opportunity_score': opportunity['score'],
                    'business_domain': opportunity['domain'],
                    'target_market': opportunity['target_market']
                }
                ideas.append(idea)
            
            return ideas
            
        except Exception as e:
            print(f"Error in enhanced subreddit discovery for r/{subreddit}: {e}")
            # Fallback to basic scraping if enhanced analysis fails
            return self.scrape_reddit_subreddit(subreddit)
    
    def save_cycle_results(self, ideas, health_status):
        """Save cycle results to disk with enhanced metadata"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Calculate enhanced metrics
        total_score_sum = sum(idea.get('total_opportunity_score', idea.get('confidence_score', 0)) for idea in ideas)
        avg_quality_score = total_score_sum / len(ideas) if ideas else 0
        
        # Domain distribution
        domain_counts = {}
        for idea in ideas:
            domain = idea.get('business_domain', 'unknown')
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        # Platform distribution
        platform_counts = {}
        for idea in ideas:
            platform = idea.get('source', 'unknown')
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        cycle_data = {
            'cycle_number': self.cycle_count + 1,
            'timestamp': timestamp,
            'ideas_found': len(ideas),
            'ideas': ideas,
            'system_health': health_status,
            'enhanced_metrics': {
                'avg_quality_score': avg_quality_score,
                'domain_distribution': domain_counts,
                'platform_distribution': platform_counts,
                'discovery_types': {
                    'enhanced_multi_platform': len([i for i in ideas if i.get('discovery_type') == 'enhanced_multi_platform']),
                    'enhanced_llm_analysis': len([i for i in ideas if i.get('discovery_type') == 'enhanced_llm_analysis']),
                    'platform_enhanced': len([i for i in ideas if 'enhanced' in i.get('discovery_type', '')]),
                    'basic_discovery': len([i for i in ideas if 'enhanced' not in i.get('discovery_type', '')])
                }
            },
            'runtime_stats': {
                'total_cycles': self.cycle_count + 1,
                'total_ideas': self.total_ideas + len(ideas),
                'uptime_minutes': (time.time() - self.start_time.timestamp()) / 60 if self.start_time else 0,
                'avg_ideas_per_cycle': (self.total_ideas + len(ideas)) / (self.cycle_count + 1)
            }
        }
        
        # Save individual cycle
        cycle_file = self.data_dir / f"enhanced_cycle_{timestamp}.json"
        with open(cycle_file, 'w') as f:
            json.dump(cycle_data, f, indent=2)
        
        # Update master log
        master_file = self.data_dir / "enhanced_overnight_discovery_log.json"
        if master_file.exists():
            with open(master_file, 'r') as f:
                master_data = json.load(f)
        else:
            master_data = {'cycles': [], 'summary': {}}
        
        master_data['cycles'].append({
            'cycle': self.cycle_count + 1,
            'timestamp': timestamp,
            'ideas_found': len(ideas),
            'avg_quality_score': avg_quality_score,
            'cpu_usage': health_status['cpu_percent'],
            'memory_usage': health_status['memory_percent'],
            'available_gb': health_status['available_gb'],
            'platforms_used': len(platform_counts),
            'domains_covered': len(domain_counts)
        })
        
        # Calculate summary statistics
        all_quality_scores = [c.get('avg_quality_score', 0) for c in master_data['cycles'] if c.get('avg_quality_score')]
        
        master_data['summary'] = {
            'total_cycles': self.cycle_count + 1,
            'total_ideas': self.total_ideas + len(ideas),
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'last_update': timestamp,
            'avg_ideas_per_cycle': (self.total_ideas + len(ideas)) / (self.cycle_count + 1),
            'avg_quality_score': sum(all_quality_scores) / len(all_quality_scores) if all_quality_scores else 0,
            'avg_cpu_usage': sum(c['cpu_usage'] for c in master_data['cycles']) / len(master_data['cycles']),
            'avg_memory_usage': sum(c['memory_usage'] for c in master_data['cycles']) / len(master_data['cycles']),
            'total_platforms_used': len(set().union(*[c.get('platforms_used', []) for c in master_data['cycles']])),
            'enhanced_discovery_rate': len([c for c in master_data['cycles'] if c.get('avg_quality_score', 0) > 6]) / len(master_data['cycles']) * 100
        }
        
        with open(master_file, 'w') as f:
            json.dump(master_data, f, indent=2)
        
        print(f"💾 Enhanced data saved to {cycle_file}")
        print(f"📊 Quality metrics: Avg score {avg_quality_score:.1f}/10, {len(platform_counts)} platforms, {len(domain_counts)} domains")
    
    def calculate_sleep_time(self):
        """Calculate intelligent sleep time based on system load and rate limits"""
        base_sleep = self.min_cycle_interval
        
        # Get current system load
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        
        # Increase sleep time if system is under stress
        if cpu_percent > 50:
            base_sleep *= 1.5
        if memory_percent > 80:
            base_sleep *= 1.3
        
        # Add some randomization to avoid predictable patterns
        jitter = random.uniform(0.8, 1.2)
        final_sleep = int(base_sleep * jitter)
        
        # Ensure we don't exceed rate limits
        cycles_this_hour = len([c for c in getattr(self, 'recent_cycles', []) 
                               if datetime.now() - datetime.fromisoformat(c) < timedelta(hours=1)])
        
        if cycles_this_hour >= self.max_cycles_per_hour:
            # Sleep until next hour
            next_hour = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            sleep_until_next_hour = (next_hour - datetime.now()).total_seconds()
            final_sleep = max(final_sleep, int(sleep_until_next_hour))
        
        return final_sleep
    
    async def run_overnight_cycle(self, duration_hours=8):
        """Run the enhanced overnight discovery cycle"""
        print("🌙 STARTING ENHANCED OVERNIGHT DISCOVERY CYCLE")
        print("=" * 60)
        print(f"⏰ Duration: {duration_hours} hours")
        print(f"🌐 Multi-platform: {len(self.all_platforms)} platforms available")
        print(f"🧠 Enhanced pain point analysis: ENABLED")
        print()
        
        self.running = True
        self.start_time = datetime.now()
        end_time = self.start_time + timedelta(hours=duration_hours)
        
        print(f"🚀 Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🏁 End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Initialize the multi-platform analyzer
        await self.initialize_multi_platform_analyzer()
        
        try:
            while self.running and datetime.now() < end_time and self.cycle_count < self.max_total_cycles:
                # Run enhanced discovery cycle
                success = await self.safe_discovery_cycle()
                
                if not success:
                    print("⚠️ Cycle failed, continuing with next cycle...")
                
                # Check if we should continue
                if not self.running:
                    break
                
                if datetime.now() >= end_time:
                    print("⏰ Time limit reached")
                    break
                
                if self.cycle_count >= self.max_total_cycles:
                    print(f"🛑 Maximum cycles ({self.max_total_cycles}) reached")
                    break
                
                # Calculate intelligent sleep time
                sleep_time = self.calculate_sleep_time()
                next_cycle_time = datetime.now() + timedelta(seconds=sleep_time)
                
                print(f"😴 Sleeping for {sleep_time//60:.0f}m {sleep_time%60:.0f}s until {next_cycle_time.strftime('%H:%M:%S')}")
                print("-" * 60)
                
                # Sleep with periodic health checks
                sleep_start = time.time()
                while time.time() - sleep_start < sleep_time and self.running:
                    await asyncio.sleep(min(60, sleep_time - (time.time() - sleep_start)))  # Check every minute
                    
                    # Quick health check during sleep
                    if time.time() - sleep_start > 300:  # After 5 minutes of sleep
                        health = self.check_system_health()
                        if not health['healthy']:
                            print(f"\n⚠️ System health degraded during sleep:")
                            for warning in health['warnings']:
                                print(f"   • {warning}")
                            print("😴 Extending sleep for system recovery...")
                            await asyncio.sleep(300)  # Extra 5 minutes
        
        except KeyboardInterrupt:
            print("\n🛑 Keyboard interrupt received")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        finally:
            self.running = False
            
            # Clean up
            if self.multi_platform_analyzer:
                try:
                    await self.multi_platform_analyzer.close()
                except:
                    pass
        
        # Final summary
        duration = datetime.now() - self.start_time
        print(f"\n🎉 ENHANCED OVERNIGHT DISCOVERY COMPLETE!")
        print("=" * 50)
        print(f"⏱️ Total runtime: {duration}")
        print(f"🔄 Cycles completed: {self.cycle_count}")
        print(f"💡 Total ideas discovered: {self.total_ideas}")
        print(f"📊 Average ideas per cycle: {self.total_ideas/self.cycle_count:.1f}" if self.cycle_count > 0 else "📊 No cycles completed")
        print(f"📁 Data saved in: {self.data_dir}")
        print(f"🧠 Enhanced analysis: {'ACTIVE' if self.multi_platform_analyzer else 'FALLBACK'}")
    
    def stop_cycle(self):
        """Stop the overnight cycle gracefully"""
        print("\n🛑 Stopping overnight discovery cycle...")
        self.running = False

def main():
    """Main function to run enhanced overnight discovery"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhanced Overnight Discovery Cycle')
    parser.add_argument('--hours', type=int, default=8, help='Duration in hours (default: 8)')
    parser.add_argument('--max-cycles', type=int, default=50, help='Maximum cycles (default: 50)')
    
    args = parser.parse_args()
    
    # Create and run the enhanced engine
    engine = OvernightDiscoveryEngine()
    engine.max_total_cycles = args.max_cycles
    
    try:
        # Run the enhanced overnight cycle
        asyncio.run(engine.run_overnight_cycle(duration_hours=args.hours))
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        engine.stop_cycle()

if __name__ == "__main__":
    main()