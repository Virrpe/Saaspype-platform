"""
Reddit Client Service - Shared Reddit API Integration
Provides unified Reddit API access across all domains
"""

import os
import time
import logging
import asyncio
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class RateLimitInfo:
    """Rate limit tracking information"""
    requests_made: int = 0
    requests_remaining: int = 60
    reset_time: datetime = None
    last_request_time: datetime = None

class RedditClient:
    """Shared Reddit API client with OAuth2 and rate limiting"""
    
    def __init__(self):
        # Reddit API credentials (from environment or config)
        self.client_id = os.getenv('REDDIT_CLIENT_ID', 'your_client_id')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET', 'your_client_secret')
        self.user_agent = os.getenv('REDDIT_USER_AGENT', 'Luciq:discovery-engine:v2.1 (by /u/luciq_bot)')
        
        # API Configuration
        self.base_url = "https://oauth.reddit.com"
        self.auth_url = "https://www.reddit.com/api/v1/access_token"
        self.rate_limit = RateLimitInfo()
        
        # Session setup
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.user_agent
        })
        
        # Authentication
        self.access_token = None
        self.token_expires_at = None
        
        # Rate limiting (Reddit allows 60 requests per minute for OAuth)
        self.requests_per_minute = 60
        self.request_interval = 60.0 / self.requests_per_minute  # ~1 second between requests
        
        logger.info("Shared Reddit Client initialized")
    
    async def authenticate(self) -> bool:
        """Authenticate with Reddit API using OAuth2"""
        try:
            # Use application-only OAuth2 flow
            auth_data = {
                'grant_type': 'client_credentials',
                'scope': 'read'
            }
            
            response = requests.post(
                self.auth_url,
                auth=(self.client_id, self.client_secret),
                data=auth_data,
                headers={'User-Agent': self.user_agent}
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data['access_token']
                expires_in = token_data.get('expires_in', 3600)
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                
                # Update session headers
                self.session.headers.update({
                    'Authorization': f'Bearer {self.access_token}'
                })
                
                logger.info("Reddit API authentication successful")
                return True
            else:
                logger.error(f"Reddit API authentication failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Reddit API authentication error: {e}")
            return False
    
    def _is_token_valid(self) -> bool:
        """Check if current token is still valid"""
        if not self.access_token or not self.token_expires_at:
            return False
        return datetime.now() < self.token_expires_at
    
    async def _ensure_authenticated(self) -> bool:
        """Ensure we have a valid authentication token"""
        if not self._is_token_valid():
            return await self.authenticate()
        return True
    
    def _wait_for_rate_limit(self):
        """Implement rate limiting to respect Reddit's API limits"""
        now = datetime.now()
        
        if self.rate_limit.last_request_time:
            time_since_last_request = (now - self.rate_limit.last_request_time).total_seconds()
            if time_since_last_request < self.request_interval:
                wait_time = self.request_interval - time_since_last_request
                logger.debug(f"Rate limiting: waiting {wait_time:.2f}s")
                time.sleep(wait_time)
        
        self.rate_limit.last_request_time = datetime.now()
        self.rate_limit.requests_made += 1
    
    async def _make_api_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make authenticated API request with rate limiting and error handling"""
        try:
            # For development/testing, use public API if OAuth not configured
            if self.client_id == 'your_client_id':
                return await self._fallback_public_api(endpoint, params)
            
            # Ensure authentication
            if not await self._ensure_authenticated():
                logger.error("Failed to authenticate with Reddit API, falling back to public API")
                return await self._fallback_public_api(endpoint, params)
            
            # Apply rate limiting
            self._wait_for_rate_limit()
            
            # Make request
            url = f"{self.base_url}{endpoint}"
            response = self.session.get(url, params=params or {}, timeout=10)
            
            # Handle response
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                logger.warning("Reddit API authentication expired, falling back to public API")
                return await self._fallback_public_api(endpoint, params)
            elif response.status_code == 429:
                logger.warning("Reddit API rate limit exceeded, falling back to public API")
                return await self._fallback_public_api(endpoint, params)
            else:
                logger.error(f"Reddit API request failed: {response.status_code}, falling back to public API")
                return await self._fallback_public_api(endpoint, params)
                
        except Exception as e:
            logger.error(f"Reddit API request error: {e}, falling back to public API")
            return await self._fallback_public_api(endpoint, params)
    
    async def _fallback_public_api(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Fallback to public Reddit JSON API"""
        try:
            # Convert OAuth endpoint to public API endpoint
            if endpoint.startswith('/r/'):
                # Extract subreddit and sort from endpoint
                parts = endpoint.strip('/').split('/')
                if len(parts) >= 3:
                    subreddit = parts[1]
                    sort = parts[2]
                    public_url = f"https://www.reddit.com/r/{subreddit}/{sort}.json"
                else:
                    logger.error(f"Invalid endpoint format: {endpoint}")
                    return None
            else:
                logger.error(f"Unsupported endpoint for public API: {endpoint}")
                return None
            
            # Make public API request
            public_session = requests.Session()
            public_session.headers.update({
                'User-Agent': self.user_agent
            })
            
            response = public_session.get(public_url, params=params or {}, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Public Reddit API request failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Public Reddit API fallback error: {e}")
            return None
    
    async def get_subreddit_posts(self, subreddit: str, sort: str = 'new', limit: int = 25, time_filter: str = 'day') -> List[Dict]:
        """
        Get posts from a subreddit using Reddit API with fallback
        
        Args:
            subreddit: Subreddit name (without r/)
            sort: Sort method ('new', 'hot', 'top', 'rising')
            limit: Number of posts to fetch (max 100)
            time_filter: Time filter for 'top' sort
        
        Returns:
            List of post dictionaries
        """
        try:
            # Construct endpoint
            endpoint = f"/r/{subreddit}/{sort}"
            
            # Parameters
            params = {
                'limit': min(limit, 100),  # Reddit API max is 100
                'raw_json': 1  # Get JSON without HTML entities
            }
            
            if sort == 'top':
                params['t'] = time_filter
            
            # Make API request
            data = await self._make_api_request(endpoint, params)
            
            if not data:
                logger.warning(f"No data received from Reddit API for r/{subreddit}")
                return []
            
            # Extract posts from response
            posts = []
            children = data.get('data', {}).get('children', [])
            
            for child in children:
                post_data = child.get('data', {})
                if post_data:
                    posts.append(post_data)
            
            logger.info(f"Retrieved {len(posts)} posts from r/{subreddit}")
            return posts
            
        except Exception as e:
            logger.error(f"Error getting subreddit posts: {e}")
            return []
    
    def get_rate_limit_status(self) -> Dict[str, Any]:
        """Get current rate limit status"""
        return {
            'requests_made': self.rate_limit.requests_made,
            'requests_remaining': self.rate_limit.requests_remaining,
            'reset_time': self.rate_limit.reset_time.isoformat() if self.rate_limit.reset_time else None,
            'last_request_time': self.rate_limit.last_request_time.isoformat() if self.rate_limit.last_request_time else None
        } 