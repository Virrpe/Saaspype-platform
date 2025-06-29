"""
Luciq Reddit Client Service
Extracted from master_luciq_api.py - Phase 2 Core Architecture Refactoring

Handles Reddit API integration with OAuth and fallback mechanisms
"""

import aiohttp
import asyncio
import logging
import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta

from config import settings

logger = logging.getLogger(__name__)

class MasterRedditClient:
    """Enhanced Reddit client with OAuth and fallback mechanisms"""
    
    def __init__(self):
        self.client_id = settings.REDDIT_CLIENT_ID
        self.client_secret = settings.REDDIT_CLIENT_SECRET
        self.user_agent = settings.REDDIT_USER_AGENT
        self.access_token = None
        self.token_expires_at = None
        
        # Business intelligence keywords for filtering
        self.business_keywords = [
            'startup', 'business', 'entrepreneur', 'saas', 'revenue', 'customers',
            'market', 'product', 'service', 'problem', 'solution', 'pain point',
            'opportunity', 'idea', 'launch', 'funding', 'investment', 'growth',
            'scale', 'monetize', 'profit', 'competition', 'industry', 'niche',
            'target audience', 'user acquisition', 'marketing', 'sales'
        ]
        
        # Spam indicators
        self.spam_indicators = [
            'buy now', 'click here', 'limited time', 'act fast', 'guaranteed',
            'make money fast', 'work from home', 'get rich', 'no experience',
            'free money', 'easy money', 'passive income scam'
        ]
    
    async def get_access_token(self) -> Optional[str]:
        """Get Reddit OAuth access token"""
        if not self.client_id or not self.client_secret:
            logger.warning("Reddit API credentials not configured")
            return None
            
        if self.access_token and self.token_expires_at and datetime.now() < self.token_expires_at:
            return self.access_token
        
        try:
            auth = aiohttp.BasicAuth(self.client_id, self.client_secret)
            headers = {'User-Agent': self.user_agent}
            data = {'grant_type': 'client_credentials'}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://www.reddit.com/api/v1/access_token',
                    auth=auth,
                    headers=headers,
                    data=data
                ) as response:
                    if response.status == 200:
                        token_data = await response.json()
                        self.access_token = token_data['access_token']
                        expires_in = token_data.get('expires_in', 3600)
                        self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
                        logger.info("Reddit OAuth token obtained successfully")
                        return self.access_token
                    else:
                        logger.error(f"Failed to get Reddit token: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error getting Reddit access token: {e}")
            return None
    
    async def get_subreddit_posts(self, subreddit: str, sort: str = 'new', limit: int = 25, time_filter: str = 'day') -> List[Dict]:
        """Get posts from subreddit with OAuth or fallback"""
        token = await self.get_access_token()
        
        if token:
            try:
                return await self._get_posts_oauth(subreddit, sort, limit, time_filter, token)
            except Exception as e:
                logger.warning(f"OAuth request failed, falling back to public API: {e}")
        
        # Fallback to public API
        return await self._get_posts_fallback(subreddit, sort, limit)
    
    async def _get_posts_oauth(self, subreddit: str, sort: str, limit: int, time_filter: str, token: str) -> List[Dict]:
        """Get posts using OAuth"""
        headers = {
            'Authorization': f'Bearer {token}',
            'User-Agent': self.user_agent
        }
        
        url = f'https://oauth.reddit.com/r/{subreddit}/{sort}'
        params = {'limit': limit, 't': time_filter}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    posts = []
                    for post in data['data']['children']:
                        post_data = post['data']
                        if not self.is_spam_content(post_data.get('title', ''), post_data.get('selftext', '')):
                            posts.append(self.extract_business_context(post_data))
                    return posts
                else:
                    raise Exception(f"OAuth API returned {response.status}")
    
    async def _get_posts_fallback(self, subreddit: str, sort: str, limit: int) -> List[Dict]:
        """Fallback to public JSON API"""
        url = f'https://www.reddit.com/r/{subreddit}/{sort}.json'
        params = {'limit': limit}
        headers = {'User-Agent': self.user_agent}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        posts = []
                        for post in data['data']['children']:
                            post_data = post['data']
                            if not self.is_spam_content(post_data.get('title', ''), post_data.get('selftext', '')):
                                posts.append(self.extract_business_context(post_data))
                        return posts
                    else:
                        logger.error(f"Fallback API returned {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Fallback API failed: {e}")
            return []
    
    def is_spam_content(self, title: str, body: str) -> bool:
        """Check if content appears to be spam"""
        content = f"{title} {body}".lower()
        
        # Check for spam indicators
        spam_count = sum(1 for indicator in self.spam_indicators if indicator in content)
        if spam_count >= 2:
            return True
        
        # Check for excessive capitalization
        if len(title) > 10 and sum(1 for c in title if c.isupper()) / len(title) > 0.5:
            return True
        
        # Check for excessive punctuation
        if title.count('!') > 3 or title.count('?') > 3:
            return True
        
        return False
    
    def extract_business_context(self, post: Dict) -> Dict:
        """Extract business-relevant context from Reddit post"""
        title = post.get('title', '')
        body = post.get('selftext', '')
        content = f"{title} {body}".lower()
        
        # Calculate business relevance score
        business_score = sum(1 for keyword in self.business_keywords if keyword in content)
        business_relevance = min(business_score / 5.0, 1.0)  # Normalize to 0-1
        
        # Extract metrics
        upvotes = post.get('ups', 0)
        comments = post.get('num_comments', 0)
        created_utc = post.get('created_utc', 0)
        
        # Calculate engagement score
        engagement_score = min((upvotes + comments * 2) / 100.0, 1.0)
        
        return {
            'id': post.get('id'),
            'title': title,
            'body': body,
            'author': post.get('author'),
            'subreddit': post.get('subreddit'),
            'url': f"https://reddit.com{post.get('permalink', '')}",
            'upvotes': upvotes,
            'comments': comments,
            'created_utc': created_utc,
            'created_datetime': datetime.fromtimestamp(created_utc) if created_utc else None,
            'business_relevance': business_relevance,
            'engagement_score': engagement_score,
            'total_score': (business_relevance + engagement_score) / 2,
            'flair': post.get('link_flair_text'),
            'is_self': post.get('is_self', False),
            'domain': post.get('domain'),
            'gilded': post.get('gilded', 0),
            'distinguished': post.get('distinguished'),
            'stickied': post.get('stickied', False)
        } 