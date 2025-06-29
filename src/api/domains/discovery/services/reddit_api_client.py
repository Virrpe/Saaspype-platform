"""
Reddit API Client Service
Real Reddit API integration with OAuth2, rate limiting, and error handling
"""

import os
import time
import logging
import asyncio
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from collections import defaultdict
import json

logger = logging.getLogger(__name__)

@dataclass
class RateLimitInfo:
    """Rate limit tracking information"""
    requests_made: int = 0
    requests_remaining: int = 60
    reset_time: datetime = None
    last_request_time: datetime = None

class RedditAPIClient:
    """Production Reddit API client with OAuth2 and rate limiting"""
    
    def __init__(self):
        # Reddit API credentials (from environment or config)
        self.client_id = os.getenv('REDDIT_CLIENT_ID', 'your_client_id')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET', 'your_client_secret')
        self.user_agent = os.getenv('REDDIT_USER_AGENT', 'Luciq:trend-discovery:v2.1 (by /u/luciq_bot)')
        
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
        
        logger.info("Reddit API Client initialized")
    
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
            # Ensure authentication
            if not await self._ensure_authenticated():
                logger.error("Failed to authenticate with Reddit API")
                return None
            
            # Apply rate limiting
            self._wait_for_rate_limit()
            
            # Make request
            url = f"{self.base_url}{endpoint}"
            response = self.session.get(url, params=params or {}, timeout=10)
            
            # Handle rate limit headers if present
            if 'x-ratelimit-remaining' in response.headers:
                self.rate_limit.requests_remaining = int(response.headers['x-ratelimit-remaining'])
            
            if 'x-ratelimit-reset' in response.headers:
                reset_timestamp = int(response.headers['x-ratelimit-reset'])
                self.rate_limit.reset_time = datetime.fromtimestamp(reset_timestamp)
            
            # Handle response
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                logger.warning("Reddit API authentication expired, re-authenticating...")
                self.access_token = None
                if await self.authenticate():
                    # Retry once with new token
                    self._wait_for_rate_limit()
                    response = self.session.get(url, params=params or {}, timeout=10)
                    if response.status_code == 200:
                        return response.json()
                logger.error("Re-authentication failed")
                return None
            elif response.status_code == 429:
                logger.warning("Reddit API rate limit exceeded")
                # Wait and retry once
                time.sleep(60)
                return await self._make_api_request(endpoint, params)
            else:
                logger.error(f"Reddit API request failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Reddit API request error: {e}")
            return None
    
    async def get_subreddit_posts(self, subreddit: str, sort: str = 'new', limit: int = 25, time_filter: str = 'day') -> List[Dict]:
        """
        Get posts from a subreddit using authenticated Reddit API
        
        Args:
            subreddit: Subreddit name (without r/)
            sort: Sort method ('new', 'hot', 'top', 'rising')
            limit: Number of posts to fetch (max 100)
            time_filter: Time filter for 'top' sort ('hour', 'day', 'week', 'month', 'year', 'all')
        
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
            
            # Extract posts
            posts = []
            children = data.get('data', {}).get('children', [])
            
            for child in children:
                post_data = child.get('data', {})
                
                # Filter out non-text posts if needed
                if not post_data.get('selftext') and not post_data.get('title'):
                    continue
                
                # Extract relevant post information
                post = {
                    'id': post_data.get('id'),
                    'title': post_data.get('title', ''),
                    'selftext': post_data.get('selftext', ''),
                    'author': post_data.get('author', '[deleted]'),
                    'score': post_data.get('score', 0),
                    'upvote_ratio': post_data.get('upvote_ratio', 0.5),
                    'num_comments': post_data.get('num_comments', 0),
                    'created_utc': post_data.get('created_utc', 0),
                    'subreddit': post_data.get('subreddit', subreddit),
                    'permalink': post_data.get('permalink', ''),
                    'url': post_data.get('url', ''),
                    'is_self': post_data.get('is_self', True),
                    'link_flair_text': post_data.get('link_flair_text', ''),
                    'distinguished': post_data.get('distinguished'),
                    'stickied': post_data.get('stickied', False),
                    'over_18': post_data.get('over_18', False),
                    'spoiler': post_data.get('spoiler', False),
                    'locked': post_data.get('locked', False),
                    'retrieved_at': datetime.now().isoformat()
                }
                
                posts.append(post)
            
            logger.info(f"Retrieved {len(posts)} posts from r/{subreddit} using Reddit API")
            return posts
            
        except Exception as e:
            logger.error(f"Error fetching posts from r/{subreddit}: {e}")
            return []
    
    async def get_post_comments(self, subreddit: str, post_id: str, limit: int = 10) -> List[Dict]:
        """
        Get comments for a specific post
        
        Args:
            subreddit: Subreddit name
            post_id: Post ID
            limit: Number of top-level comments to fetch
        
        Returns:
            List of comment dictionaries
        """
        try:
            endpoint = f"/r/{subreddit}/comments/{post_id}"
            params = {
                'limit': limit,
                'depth': 2,  # Get replies to top-level comments
                'raw_json': 1
            }
            
            data = await self._make_api_request(endpoint, params)
            
            if not data or len(data) < 2:
                return []
            
            # Comments are in the second element of the response array
            comments_data = data[1].get('data', {}).get('children', [])
            
            comments = []
            for comment_child in comments_data:
                comment_data = comment_child.get('data', {})
                
                if comment_data.get('body') in ['[deleted]', '[removed]', '']:
                    continue
                
                comment = {
                    'id': comment_data.get('id'),
                    'body': comment_data.get('body', ''),
                    'author': comment_data.get('author', '[deleted]'),
                    'score': comment_data.get('score', 0),
                    'created_utc': comment_data.get('created_utc', 0),
                    'parent_id': comment_data.get('parent_id', ''),
                    'depth': comment_data.get('depth', 0),
                    'retrieved_at': datetime.now().isoformat()
                }
                
                comments.append(comment)
            
            return comments
            
        except Exception as e:
            logger.error(f"Error fetching comments for post {post_id}: {e}")
            return []
    
    def get_rate_limit_status(self) -> Dict[str, Any]:
        """Get current rate limit status"""
        return {
            'requests_made': self.rate_limit.requests_made,
            'requests_remaining': self.rate_limit.requests_remaining,
            'reset_time': self.rate_limit.reset_time.isoformat() if self.rate_limit.reset_time else None,
            'last_request_time': self.rate_limit.last_request_time.isoformat() if self.rate_limit.last_request_time else None,
            'authenticated': self._is_token_valid()
        }

# Global instance
reddit_api_client = RedditAPIClient() 