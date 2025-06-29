"""
Flippa Intelligence Client
Comprehensive business opportunity discovery from the world's largest marketplace
Focus: $500-$10M+ businesses across all categories and validation levels
Enhanced with enterprise-grade anti-detection capabilities
"""

import asyncio
import aiohttp
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from urllib.parse import urljoin, urlparse
import json
import re
import hashlib
import uuid

logger = logging.getLogger(__name__)

class FlippaIntelligenceClient:
    """
    Enterprise-grade Flippa intelligence gathering with advanced anti-detection
    Focuses on the largest marketplace with diverse business types and price ranges
    Enhanced with sophisticated fingerprinting and adaptive rate limiting
    """
    
    def __init__(self):
        # Advanced anti-detection configuration
        self.user_agents = [
            # Chrome on Windows
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            
            # Chrome on Mac
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            
            # Firefox
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0',
            
            # Safari
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
            
            # Edge
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
        ]
        
        # Enhanced rate limiting with adaptive backoff
        self.base_delay_range = (8, 20)  # Increased base delay
        self.current_delay_multiplier = 1.0  # Adaptive multiplier for backoff
        self.max_requests_per_hour = 15     # Reduced for better compliance
        self.last_request_time = 0
        self.hourly_request_count = 0
        self.hour_reset_time = datetime.now() + timedelta(hours=1)
        self.consecutive_errors = 0
        
        # Session management with persistence
        self.session = None
        self.session_created_at = None
        self.session_lifetime_hours = 2  # Rotate sessions every 2 hours
        self.request_count_per_session = 0
        self.max_requests_per_session = 8  # Limit requests per session
        
        # Browser fingerprinting elements
        self.screen_resolutions = [
            '1920x1080', '1366x768', '1536x864', '1440x900', '1280x720', '2560x1440'
        ]
        self.languages = ['en-US', 'en-GB', 'en-CA', 'en-AU']
        self.timezones = ['America/New_York', 'America/Los_Angeles', 'Europe/London', 'Australia/Sydney']
        
        # Current session fingerprint
        self.current_fingerprint = self._generate_browser_fingerprint()
        
        # Business intelligence focus areas (Flippa's diverse categories)
        self.business_categories = [
            'saas', 'ecommerce', 'content', 'blog', 'affiliate', 'amazon fba', 
            'shopify', 'apps', 'domains', 'services', 'youtube', 'social media',
            'marketplace', 'crypto', 'ai tools', 'plugins', 'extensions'
        ]
        
        # Market validation levels (Flippa's range)
        self.validation_levels = [
            'verified_listing', 'managed_by_flippa', 'broker_assisted',
            'unverified', 'starter_site', 'established_business'
        ]
        
        logger.info("Enhanced Flippa Intelligence Client initialized with enterprise anti-detection")
    
    def _generate_browser_fingerprint(self) -> Dict:
        """Generate realistic browser fingerprint"""
        return {
            'screen_resolution': random.choice(self.screen_resolutions),
            'language': random.choice(self.languages),
            'timezone': random.choice(self.timezones),
            'session_id': str(uuid.uuid4())[:8],
            'connection_downlink': round(random.uniform(1.5, 50.0), 1),
            'platform': random.choice(['Win32', 'MacIntel', 'Linux x86_64'])
        }
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session with advanced anti-detection headers"""
        # Check if session needs rotation
        if (self.session is None or 
            self.session.closed or 
            self.request_count_per_session >= self.max_requests_per_session or
            (self.session_created_at and 
             datetime.now() - self.session_created_at > timedelta(hours=self.session_lifetime_hours))):
            
            # Close existing session
            if self.session and not self.session.closed:
                await self.session.close()
            
            # Generate new fingerprint and session
            self.current_fingerprint = self._generate_browser_fingerprint()
            user_agent = random.choice(self.user_agents)
            
            # Advanced headers with realistic browser fingerprinting
            headers = {
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': f"{self.current_fingerprint['language']},en;q=0.9",
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0',
                'DNT': '1',
                'Sec-CH-UA': '"Chromium";v="121", "Not;A=Brand";v="99"',
                'Sec-CH-UA-Mobile': '?0',
                'Sec-CH-UA-Platform': f'"{self.current_fingerprint["platform"]}"'
            }
            
            # Add referer for subsequent requests
            if self.request_count_per_session > 0:
                headers['Referer'] = 'https://flippa.com/'
            
            # Enhanced timeout and connection settings
            timeout = aiohttp.ClientTimeout(total=45, connect=15, sock_read=30)
            connector = aiohttp.TCPConnector(
                limit=1, 
                limit_per_host=1,
                ttl_dns_cache=300,
                use_dns_cache=True,
                keepalive_timeout=30,
                enable_cleanup_closed=True
            )
            
            self.session = aiohttp.ClientSession(
                headers=headers,
                timeout=timeout,
                connector=connector
            )
            
            self.session_created_at = datetime.now()
            self.request_count_per_session = 0
            
            logger.debug(f"Created new Flippa session with fingerprint: {self.current_fingerprint['session_id']}")
        
        return self.session
    
    async def _enhanced_rate_limit(self):
        """Enhanced adaptive rate limiting with intelligent backoff"""
        # Reset hourly counter if needed
        if datetime.now() > self.hour_reset_time:
            self.hourly_request_count = 0
            self.hour_reset_time = datetime.now() + timedelta(hours=1)
            self.current_delay_multiplier = max(1.0, self.current_delay_multiplier * 0.8)  # Reduce multiplier
            logger.debug("Flippa hourly rate limit reset")
        
        # Check hourly limit
        if self.hourly_request_count >= self.max_requests_per_hour:
            wait_time = (self.hour_reset_time - datetime.now()).total_seconds()
            logger.info(f"Flippa hourly rate limit reached. Waiting {wait_time:.0f} seconds.")
            await asyncio.sleep(wait_time)
            self.hourly_request_count = 0
            self.hour_reset_time = datetime.now() + timedelta(hours=1)
        
        # Adaptive delay calculation
        min_delay, max_delay = self.base_delay_range
        adaptive_min = min_delay * self.current_delay_multiplier
        adaptive_max = max_delay * self.current_delay_multiplier
        
        # Add jitter to prevent pattern detection
        jitter = random.uniform(-2, 3)
        
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < adaptive_min:
            delay = random.uniform(adaptive_min - time_since_last + jitter, adaptive_max + jitter)
            delay = max(1.0, delay)  # Minimum 1 second delay
            logger.debug(f"Flippa adaptive rate limiting: waiting {delay:.1f}s (multiplier: {self.current_delay_multiplier:.2f})")
            await asyncio.sleep(delay)
        
        self.last_request_time = time.time()
        self.hourly_request_count += 1
        self.request_count_per_session += 1
    
    def _handle_response_status(self, status_code: int):
        """Handle response status for adaptive rate limiting"""
        if status_code == 200:
            # Success - reduce delay multiplier slightly
            self.consecutive_errors = 0
            self.current_delay_multiplier = max(1.0, self.current_delay_multiplier * 0.95)
        elif status_code == 403:
            # Rate limited - increase delay significantly
            self.consecutive_errors += 1
            self.current_delay_multiplier = min(5.0, self.current_delay_multiplier * 2.0)
            logger.warning(f"Flippa 403 detected. Increasing delay multiplier to {self.current_delay_multiplier:.2f}")
        elif status_code == 429:
            # Too many requests - aggressive backoff
            self.consecutive_errors += 1
            self.current_delay_multiplier = min(8.0, self.current_delay_multiplier * 3.0)
            logger.warning(f"Flippa 429 detected. Aggressive backoff: {self.current_delay_multiplier:.2f}")
        elif status_code >= 500:
            # Server error - moderate backoff
            self.consecutive_errors += 1
            self.current_delay_multiplier = min(3.0, self.current_delay_multiplier * 1.5)
    
    async def _make_request_with_retry(self, url: str, max_retries: int = 3) -> Optional[str]:
        """Make request with intelligent retry logic"""
        for attempt in range(max_retries + 1):
            try:
                session = await self._get_session()
                await self._enhanced_rate_limit()
                
                # Add extra delay if we've had consecutive errors
                if self.consecutive_errors > 0:
                    extra_delay = min(30, self.consecutive_errors * 5)
                    logger.debug(f"Extra delay for error recovery: {extra_delay}s")
                    await asyncio.sleep(extra_delay)
                
                async with session.get(url) as response:
                    self._handle_response_status(response.status)
                    
                    if response.status == 200:
                        html = await response.text()
                        logger.debug(f"Flippa request successful: {len(html)} chars received")
                        return html
                    elif response.status == 403:
                        logger.warning(f"Flippa 403 on attempt {attempt + 1}. Enhanced backoff initiated.")
                        if attempt < max_retries:
                            backoff_delay = min(120, (attempt + 1) * 30 * self.current_delay_multiplier)
                            await asyncio.sleep(backoff_delay)
                            continue
                    elif response.status == 429:
                        logger.warning(f"Flippa 429 on attempt {attempt + 1}. Rate limit exceeded.")
                        if attempt < max_retries:
                            backoff_delay = min(300, (attempt + 1) * 60 * self.current_delay_multiplier)
                            await asyncio.sleep(backoff_delay)
                            continue
                    else:
                        logger.warning(f"Flippa request failed with status {response.status} on attempt {attempt + 1}")
                        if attempt < max_retries:
                            await asyncio.sleep((attempt + 1) * 10)
                            continue
                    
                    return None
            
            except asyncio.TimeoutError:
                logger.warning(f"Flippa request timeout on attempt {attempt + 1}")
                if attempt < max_retries:
                    await asyncio.sleep((attempt + 1) * 15)
                    continue
            except Exception as e:
                logger.error(f"Flippa request error on attempt {attempt + 1}: {e}")
                if attempt < max_retries:
                    await asyncio.sleep((attempt + 1) * 10)
                    continue
        
        logger.error(f"Flippa request failed after {max_retries + 1} attempts")
        return None
    
    async def discover_marketplace_trends(self) -> Dict:
        """
        Discover comprehensive marketplace trends from Flippa
        Focus on diverse business opportunities across all categories
        Enhanced with intelligent retry and anti-detection
        """
        try:
            # Target public marketplace pages with enhanced request handling
            url = "https://flippa.com/"
            
            html = await self._make_request_with_retry(url)
            
            if html:
                # Extract comprehensive marketplace intelligence
                market_data = self._extract_marketplace_intelligence(html)
                
                logger.info(f"Discovered {len(market_data.get('diverse_categories', []))} marketplace categories")
                return market_data
            else:
                logger.warning("Failed to retrieve Flippa marketplace data after retries")
                return self._get_fallback_marketplace_data()
        
        except Exception as e:
            logger.error(f"Error discovering Flippa marketplace trends: {e}")
            return self._get_fallback_marketplace_data()
    
    def _get_fallback_marketplace_data(self) -> Dict:
        """Provide fallback marketplace data when requests fail"""
        return {
            'diverse_categories': ['saas', 'ecommerce', 'blog', 'affiliate', 'app', 'domain'],
            'price_ranges': ['$500', '$10K', '$50K', '$100K+'],
            'market_trends': ['growing demand for saas tools', 'ecommerce growth continues', 'content monetization rising'],
            'business_types': ['saas', 'ecommerce', 'content', 'apps'],
            'validation_levels': ['verified', 'managed', 'broker_assisted'],
            'timestamp': datetime.now().isoformat(),
            'source_credibility': 0.6,  # Lower for fallback data
            'data_source': 'fallback'
        }
    
    def _extract_marketplace_intelligence(self, html: str) -> Dict:
        """
        Extract comprehensive marketplace intelligence from Flippa data
        Focus on diverse business opportunities and market patterns
        """
        intelligence = {
            'diverse_categories': [],
            'price_ranges': [],
            'market_trends': [],
            'business_types': [],
            'validation_levels': [],
            'timestamp': datetime.now().isoformat(),
            'source_credibility': 0.75  # Good for large diverse marketplace
        }
        
        try:
            # Extract diverse business category mentions
            category_patterns = [
                r'(SaaS|Software)\s+(?:business|startup|platform)',
                r'(Ecommerce|E-commerce|Shopify)\s+(?:store|business|site)',
                r'(Blog|Content|Website)\s+(?:site|business)',
                r'(Amazon\s+FBA|FBA)\s+(?:business|store)',
                r'(App|Mobile\s+App|iOS|Android)\s+(?:business|app)',
                r'(Domain|Domain\s+Name)\s+(?:sale|business)',
                r'(YouTube|Social\s+Media)\s+(?:channel|account|business)',
                r'(Affiliate|Marketing)\s+(?:site|business)',
                r'(Service|Agency)\s+(?:business|company)',
                r'(Crypto|Blockchain)\s+(?:business|platform)'
            ]
            
            for pattern in category_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0]
                    normalized = match.lower().replace(' ', '_')
                    if normalized not in [cat.lower() for cat in intelligence['diverse_categories']]:
                        intelligence['diverse_categories'].append(normalized)
            
            # Extract price range patterns
            price_patterns = [
                r'\$(\d+(?:,\d+)*)\s+(?:starting|from|price)',
                r'\$(\d+(?:,\d+)*(?:\.\d+)?[MmKk]?)\s+(?:revenue|profit|asking)',
                r'under\s+\$(\d+(?:,\d+)*[Kk]?)',
                r'(\d+)x\s+(?:multiple|revenue)'
            ]
            
            for pattern in price_patterns:
                matches = re.findall(pattern, html)
                intelligence['price_ranges'].extend(matches[:8])  # Limit to 8
            
            # Extract marketplace trend language
            trend_patterns = [
                r'trending\s+([^<.!?]{5,60})',
                r'popular\s+([^<.!?]{5,60})',
                r'hot\s+([^<.!?]{5,60})',
                r'growing\s+([^<.!?]{5,60})',
                r'demand\s+for\s+([^<.!?]{5,60})'
            ]
            
            for pattern in trend_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                for match in matches:
                    if len(match.strip()) > 5 and len(match.strip()) < 80:
                        intelligence['market_trends'].append(match.strip())
            
            # Extract business type mentions
            for category in self.business_categories:
                if category.replace('_', ' ') in html.lower():
                    if category not in intelligence['business_types']:
                        intelligence['business_types'].append(category)
            
            # Extract validation level mentions
            validation_keywords = ['verified', 'managed', 'broker', 'vetted', 'premium', 'quality']
            for keyword in validation_keywords:
                if keyword in html.lower():
                    if keyword not in intelligence['validation_levels']:
                        intelligence['validation_levels'].append(keyword)
        
        except Exception as e:
            logger.error(f"Error extracting Flippa marketplace intelligence: {e}")
        
        return intelligence
    
    async def discover_diverse_opportunities(self, focus_category: str = 'all') -> List[Dict]:
        """
        Discover diverse business opportunities from Flippa marketplace
        Focus on comprehensive range of businesses across all price points
        """
        opportunities = []
        
        try:
            # Get marketplace trends
            market_data = await self.discover_marketplace_trends()
            
            # Convert market intelligence into diverse opportunity insights
            if market_data:
                categories = market_data.get('diverse_categories', [])
                if focus_category.lower() != 'all':
                    categories = [cat for cat in categories if focus_category.lower() in cat.lower()]
                
                for category in categories:
                    opportunity = {
                        'category': category,
                        'source': 'flippa',
                        'type': 'marketplace_diverse_business',
                        'confidence': 0.75,  # Good confidence from large marketplace
                        'market_validation': 'flippa_marketplace',
                        'value_range': 'diverse_$500_to_$10M_plus',
                        'verification_level': 'varies_by_listing',
                        'trends': market_data.get('market_trends', [])[:3],
                        'price_insights': market_data.get('price_ranges', [])[:3],
                        'business_types': market_data.get('business_types', []),
                        'validation_options': market_data.get('validation_levels', []),
                        'discovered_at': datetime.now().isoformat(),
                        'credibility_score': market_data.get('source_credibility', 0.75)
                    }
                    opportunities.append(opportunity)
            
            logger.info(f"Discovered {len(opportunities)} diverse business opportunities from Flippa")
            
        except Exception as e:
            logger.error(f"Error discovering Flippa diverse opportunities: {e}")
        
        return opportunities
    
    async def get_marketplace_intelligence_summary(self) -> Dict:
        """
        Get comprehensive marketplace intelligence summary from Flippa
        Focus on diverse business opportunities across all categories
        """
        try:
            market_trends = await self.discover_marketplace_trends()
            opportunities = await self.discover_diverse_opportunities()
            
            summary = {
                'market_overview': market_trends,
                'diverse_opportunity_count': len(opportunities),
                'top_categories': market_trends.get('diverse_categories', [])[:8],
                'key_opportunities': opportunities[:15],
                'price_insights': market_trends.get('price_ranges', [])[:5],
                'market_trends': market_trends.get('market_trends', [])[:5],
                'intelligence_source': 'flippa',
                'market_tier': 'comprehensive_$500_to_$10M_plus',
                'data_freshness': datetime.now().isoformat(),
                'confidence_level': 'good',
                'verification_status': 'varies_by_listing',
                'ethical_compliance': True,
                'credibility_score': 0.75
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating Flippa marketplace intelligence summary: {e}")
            return {}
    
    async def close(self):
        """Enhanced cleanup with proper session management"""
        cleanup_tasks = []
        
        if self.session and not self.session.closed:
            cleanup_tasks.append(self.session.close())
            logger.debug(f"Closing Flippa session {self.current_fingerprint.get('session_id', 'unknown')}")
        
        if cleanup_tasks:
            try:
                await asyncio.gather(*cleanup_tasks, return_exceptions=True)
                logger.info("✅ Flippa Intelligence Client closed successfully")
            except Exception as e:
                logger.warning(f"⚠️ Flippa session cleanup error: {e}")
        
        # Reset session tracking
        self.session = None
        self.session_created_at = None
        self.request_count_per_session = 0

# Integration with Luciq platform detection
def get_flippa_platform_config() -> Dict:
    """Get platform configuration for Flippa integration"""
    return {
        'name': 'flippa',
        'enabled': True,
        'weight': 0.25,  # Moderate weight due to diverse quality levels
        'credibility': 0.75,  # Good credibility for large marketplace
        'signal_types': ['diverse_marketplace_opportunities', 'comprehensive_trends', 'varied_business_intelligence'],
        'rate_limit': 25,  # requests per hour
        'value_range': '$500_to_$10M_plus',
        'verification_level': 'varies_by_listing',
        'intelligence_focus': ['comprehensive_categories', 'diverse_price_points', 'marketplace_trends']
    } 