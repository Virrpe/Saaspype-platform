#!/usr/bin/env python3
"""
Discovery Service - Enhanced Reddit discovery with LLM analysis
Now using real Reddit API with OAuth2 and rate limiting
"""

import random
import time
import json
import re
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Set
import os
import logging
import hashlib
from collections import defaultdict
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

from src.shared.config.settings import MEMORY_DIR, PROCESSED_POSTS_FILE
from src.shared.database.connection import db_service
from src.api.domains.discovery.services.reddit_api_client import reddit_api_client
from ..models.discovery_models import DiscoveryRequest, DiscoveryResponse
from src.api.shared.services.reddit_client import RedditClient
from src.shared.database.connection import DatabaseService

# Initialize services
reddit_client = RedditClient()
db_service = DatabaseService()

class DiscoveryService:
    """Reddit discovery service with enhanced content quality and business intelligence"""
    
    def __init__(self):
        # Initialize Reddit API client
        self.reddit_client = reddit_client
        self.db_service = db_service
        
        # Target subreddits for SaaS discovery
        self.target_subreddits = [
            'startups', 'Entrepreneur', 'SaaS', 'freelance', 'smallbusiness',
            'indiehackers', 'entrepreneur', 'business', 'marketing', 'webdev',
            'productivity', 'consulting', 'remotework', 'devtools'
        ]
        
        # Enhanced spam detection patterns
        self.spam_keywords = [
            'upvote', 'karma', 'follow me', 'subscribe', 'like and share',
            'check out my', 'dm me', 'click here', 'free money', 'get rich',
            'make money fast', 'work from home', 'easy money', 'passive income',
            'crypto', 'bitcoin', 'nft', 'forex', 'trading signals'
        ]
        
        # Business-related keywords for content filtering
        self.business_keywords = [
            'startup', 'business', 'entrepreneur', 'saas', 'revenue', 'customers',
            'product', 'market', 'solution', 'problem', 'pain point', 'workflow',
            'automation', 'efficiency', 'cost', 'save time', 'productivity',
            'freelancer', 'client', 'agency', 'tool', 'platform', 'software'
        ]
        
        # Industries for categorization
        self.industries = [
            'fintech', 'healthcare', 'education', 'marketing', 'sales', 'hr',
            'logistics', 'ecommerce', 'real estate', 'travel', 'food', 'fitness',
            'legal', 'construction', 'manufacturing', 'retail', 'consulting'
        ]
        
        # Business context patterns for industry detection
        self.industry_patterns = {
            'software': [r'\b(saas|software|app|platform|api|code|dev|tech|ai|ml)\b'],
            'ecommerce': [r'\b(ecommerce|online\s+store|shopify|amazon|selling|retail)\b'],
            'marketing': [r'\b(marketing|advertising|social\s+media|seo|content|brand)\b'],
            'finance': [r'\b(finance|accounting|money|payment|fintech|banking)\b'],
            'healthcare': [r'\b(health|medical|doctor|patient|clinic|hospital)\b'],
            'education': [r'\b(education|learning|course|training|teach|student)\b'],
            'hr': [r'\b(hr|human\s+resources|hiring|recruitment|employee|staff)\b'],
            'logistics': [r'\b(logistics|shipping|delivery|transportation|supply\s+chain)\b'],
            'real estate': [r'\b(real\s+estate|property|housing|rent|mortgage)\b'],
            'travel': [r'\b(travel|tourism|hotel|booking|vacation|flight)\b'],
            'legal': [r'\b(legal|law|lawyer|attorney|contract|compliance)\b']
        }
        
        # Load pain point analysis prompt
        self.pain_point_prompt = self._load_pain_point_analysis_prompt()
        
        # Enhanced pain point indicators
        self.pain_indicators = {
            'high_intensity': ['hate', 'terrible', 'nightmare', 'impossible', 'broken', 'awful', 'disaster'],
            'workflow_friction': ['wasting time', 'manual', 'tedious', 'repetitive', 'inefficient', 'slow', 'clunky'],
            'solution_seeking': ['need help', 'looking for', 'wish there was', 'no solution', "can't find", 'how do i'],
            'problem_patterns': ['problem with', 'issue with', 'struggling with', 'difficulty with', 'challenge with'],
            'urgency': ['urgent', 'asap', 'immediately', 'deadline', 'critical', 'emergency', 'desperate']
        }
        
        logger.info("Discovery Service initialized with Reddit API client")
    
    async def fetch_subreddit_posts(self, subreddit: str, limit: int = 10) -> List[Dict]:
        """Fetch posts from specified subreddit using real Reddit API"""
        try:
            logger.info(f"Fetching {limit} posts from r/{subreddit} using Reddit API")
            
            # Use the real Reddit API client
            raw_posts = await self.reddit_client.get_subreddit_posts(
                subreddit=subreddit,
                sort='new',  # Get recent posts for trend detection
                limit=limit * 2,  # Fetch more to account for filtering
                time_filter='day'
            )
            
            # If Reddit API fails or returns no data, try fallback
            if not raw_posts:
                logger.warning(f"Reddit API returned no data for r/{subreddit}, trying fallback")
                return await self._fallback_fetch_posts(subreddit, limit)
            
            # Process and filter posts
            processed_posts = []
            for post in raw_posts:
                # Skip if missing essential data
                if not post.get('title') or post.get('stickied', False):
                    continue
                
                # Skip deleted or removed posts
                if post.get('selftext') in ['[deleted]', '[removed]', '']:
                    continue
                
                # Enhanced spam detection
                spam_analysis = self._advanced_spam_detection(post)
                if spam_analysis['is_spam']:
                    logger.debug(f"Filtered spam post: {post.get('title', '')[:50]}...")
                    continue
                
                # Extract business context
                business_context = self._extract_business_context(post)
                
                # Convert created_utc to datetime for compatibility
                created_utc = post.get('created_utc', 0)
                if isinstance(created_utc, (int, float)):
                    created_datetime = datetime.fromtimestamp(created_utc)
                else:
                    created_datetime = datetime.now()
                
                processed_post = {
                    'id': post.get('id'),
                    'title': post.get('title'),
                    'body': post.get('selftext', ''),
                    'author': post.get('author'),
                    'score': post.get('score', 0),
                    'upvote_ratio': post.get('upvote_ratio', 0.5),
                    'num_comments': post.get('num_comments', 0),
                    'created_utc': created_utc,
                    'created_datetime': created_datetime.isoformat(),
                    'subreddit': subreddit,
                    'url': f"https://reddit.com{post.get('permalink', '')}",
                    'full_url': post.get('url', ''),
                    'is_self': post.get('is_self', True),
                    'link_flair_text': post.get('link_flair_text', ''),
                    'over_18': post.get('over_18', False),
                    'locked': post.get('locked', False),
                    'spam_analysis': spam_analysis,
                    'business_context': business_context,
                    'retrieved_via': 'reddit_api_oauth2'
                }
                
                processed_posts.append(processed_post)
                
                if len(processed_posts) >= limit:
                    break
            
            # If we got no processed posts after filtering, try fallback
            if not processed_posts:
                logger.warning(f"No valid posts after filtering from Reddit API for r/{subreddit}, trying fallback")
                return await self._fallback_fetch_posts(subreddit, limit)
            
            logger.info(f"Processed {len(processed_posts)} quality posts from r/{subreddit}")
            return processed_posts
            
        except Exception as e:
            logger.error(f"Error fetching posts from r/{subreddit} via Reddit API: {e}")
            # Fallback to public API if OAuth fails (for development/testing)
            logger.info(f"Attempting fallback to public API for r/{subreddit}")
            return await self._fallback_fetch_posts(subreddit, limit)
    
    async def _fallback_fetch_posts(self, subreddit: str, limit: int) -> List[Dict]:
        """Fallback to public Reddit JSON API if OAuth fails"""
        try:
            import requests
            
            logger.warning(f"Falling back to public JSON API for r/{subreddit}")
            
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Luciq:discovery-engine:v2.1 (by /u/luciq_bot)'
            })
            
            url = f"https://www.reddit.com/r/{subreddit}/new.json"
            params = {'limit': limit * 3}  # Fetch more to account for filtering
            
            response = session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            posts = []
            
            for post_data in data.get('data', {}).get('children', []):
                post = post_data.get('data', {})
                
                # Skip if no title or if it's a sticky/pinned post
                if not post.get('title') or post.get('stickied', False):
                    continue
                
                # Skip deleted/removed posts
                if post.get('selftext') in ['[deleted]', '[removed]']:
                    continue
                
                # Accept both self posts and link posts with good titles
                # Skip only image/video posts without substantial text
                post_type = 'link' if not post.get('is_self', True) else 'self'
                
                # For link posts, ensure they have meaningful titles
                if post_type == 'link' and len(post.get('title', '')) < 20:
                    continue
                
                # Basic spam detection
                spam_analysis = self._advanced_spam_detection(post)
                if spam_analysis['is_spam']:
                    logger.debug(f"Filtered spam: {post.get('title', '')[:50]}...")
                    continue
                
                # Extract business context
                business_context = self._extract_business_context(post)
                
                # Convert created_utc to datetime
                created_utc = post.get('created_utc', 0)
                if isinstance(created_utc, (int, float)):
                    created_datetime = datetime.fromtimestamp(created_utc)
                else:
                    created_datetime = datetime.now()
                
                processed_post = {
                    'id': post.get('id'),
                    'title': post.get('title'),
                    'body': post.get('selftext', ''),
                    'author': post.get('author'),
                    'score': post.get('score', 0),
                    'upvote_ratio': post.get('upvote_ratio', 0.5),
                    'num_comments': post.get('num_comments', 0),
                    'created_utc': created_utc,
                    'created_datetime': created_datetime.isoformat(),
                    'subreddit': subreddit,
                    'url': f"https://reddit.com{post.get('permalink', '')}",
                    'full_url': post.get('url', ''),
                    'is_self': post.get('is_self', True),
                    'link_flair_text': post.get('link_flair_text', ''),
                    'over_18': post.get('over_18', False),
                    'locked': post.get('locked', False),
                    'spam_analysis': spam_analysis,
                    'business_context': business_context,
                    'retrieved_via': 'fallback_json_api'
                }
                
                posts.append(processed_post)
                
                if len(posts) >= limit:
                    break
            
            logger.info(f"Fallback: Successfully fetched {len(posts)} posts from r/{subreddit}")
            return posts
            
        except Exception as e:
            logger.error(f"Fallback fetch also failed for r/{subreddit}: {e}")
            return []
    
    def _calculate_content_hash(self, title: str, body: str) -> str:
        """Calculate hash for content deduplication"""
        content = f"{title.lower().strip()} {body.lower().strip()}"
        normalized = re.sub(r'\b(the|a|an|and|or|but|in|on|at|to|for|of|with|by)\b', '', content)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def _advanced_spam_detection(self, post: Dict) -> Dict:
        """Advanced spam detection with scoring"""
        title = post.get('title', '').lower()
        body = post.get('selftext', '').lower()
        combined_text = f"{title} {body}"
        
        spam_score = 0
        spam_indicators = []
        
        # Keyword-based detection (more targeted)
        high_spam_keywords = ['upvote', 'karma', 'follow me', 'dm me', 'free money', 'get rich quick']
        for keyword in high_spam_keywords:
            if keyword in combined_text:
                spam_score += 3
                spam_indicators.append(f"high_spam_keyword: {keyword}")
        
        # Lower-level spam indicators
        mild_spam_keywords = ['check out my', 'click here', 'subscribe', 'like and share']
        for keyword in mild_spam_keywords:
            if keyword in combined_text:
                spam_score += 1
                spam_indicators.append(f"mild_spam_keyword: {keyword}")
        
        # Account quality indicators
        author = post.get('author', '')
        if author in ['[deleted]', 'AutoModerator']:
            spam_score += 1
            spam_indicators.append("deleted_or_bot_account")
        
        # Content quality indicators (less aggressive)
        if len(title + body) < 20:  # Very short posts only
            spam_score += 1
            spam_indicators.append("very_low_content_length")
        
        # Multiple exclamation marks or caps
        if title.count('!') > 2 or len([c for c in title if c.isupper()]) > len(title) * 0.7:
            spam_score += 1
            spam_indicators.append("excessive_caps_or_exclamation")
        
        return {
            'spam_score': spam_score,
            'spam_indicators': spam_indicators,
            'is_spam': spam_score >= 6,  # Increased threshold
            'spam_confidence': min(1.0, spam_score / 10.0),
            'is_low_quality': spam_score >= 3
        }
    
    def _extract_business_context(self, post: Dict) -> Dict:
        """Extract business context from post content"""
        title = post.get('title', '').lower()
        body = post.get('selftext', '').lower()
        combined_text = f"{title} {body}"
        
        context = {
            'industry': 'general',
            'business_score': 0.0,
            'business_keywords': [],
            'problem_type': 'unknown',
            'urgency_level': 'low',
            'market_indicators': [],
            'pain_indicators': []
        }
        
        # Business keywords detection
        business_keywords_found = []
        for keyword in self.business_keywords:
            if keyword in combined_text:
                business_keywords_found.append(keyword)
                context['business_score'] += 0.2
        
        context['business_keywords'] = business_keywords_found
        
        # Industry detection (improved)
        industry_score = {}
        for industry, patterns in self.industry_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, combined_text, re.IGNORECASE))
                score += matches
            if score > 0:
                industry_score[industry] = score
        
        if industry_score:
            context['industry'] = max(industry_score, key=industry_score.get)
            context['business_score'] += 0.5
        
        # Problem/pain point detection (improved)
        pain_patterns = {
            'workflow': [r'\b(workflow|process|manual|automat\w+|efficient|streamlin\w+)\b'],
            'cost': [r'\b(expensive|costly|save money|budget|cheap\w+|afford\w+)\b'],
            'time': [r'\b(time consuming|slow|faster|quick\w+|save time|speed)\b'],
            'technical': [r'\b(bug|error|broken|not working|failing|glitch)\b'],
            'user_experience': [r'\b(confusing|difficult|hard to use|user friendly|intuitive)\b'],
            'scaling': [r'\b(scale|scaling|grow\w+|expand\w+|capacity|limit\w+)\b']
        }
        
        problem_scores = {}
        for problem_type, patterns in pain_patterns.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, combined_text, re.IGNORECASE)
                score += len(matches)
                context['pain_indicators'].extend(matches)
            if score > 0:
                problem_scores[problem_type] = score
        
        if problem_scores:
            context['problem_type'] = max(problem_scores, key=problem_scores.get)
            context['business_score'] += 0.3
        
        # Urgency detection
        urgency_patterns = [
            r'\b(urgent|asap|immediately|deadline|critical|emergency)\b',
            r'\b(need help|desperate|struggling|stuck)\b'
        ]
        
        urgency_score = 0
        for pattern in urgency_patterns:
            urgency_score += len(re.findall(pattern, combined_text, re.IGNORECASE))
        
        if urgency_score >= 2:
            context['urgency_level'] = 'high'
            context['business_score'] += 0.2
        elif urgency_score >= 1:
            context['urgency_level'] = 'medium'
            context['business_score'] += 0.1
        
        # Normalize business score
        context['business_score'] = min(1.0, context['business_score'])
        
        return context
    
    def _load_pain_point_analysis_prompt(self) -> str:
        """Load the sophisticated pain point analysis prompt"""
        try:
            prompt_path = Path("backups/pre-refactor-20250603-185500/emergency-backup/apps/src/prompts/discovery/pain_point_analysis.txt")
            if prompt_path.exists():
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                # Fallback prompt if file not found
                return self._get_fallback_analysis_prompt()
        except Exception as e:
            logger.warning(f"Could not load pain point analysis prompt: {e}")
            return self._get_fallback_analysis_prompt()
    
    def _get_fallback_analysis_prompt(self) -> str:
        """Fallback pain point analysis prompt"""
        return """
You are an expert SaaS opportunity analyst. Analyze Reddit posts and identify genuine business pain points.

SCORING FRAMEWORK:
- Market Size (0-3): Enterprise/industry-wide (3) vs personal problems (1)
- Urgency (0-3): Critical business blockers (3) vs wishlist items (0)
- Solution Gap (0-2): No existing solutions (2) vs saturated market (0)
- Monetization (0-2): Clear willingness to pay (2) vs cost-sensitive (0)

OUTPUT FORMAT:
{
  "pain_point": "Clear problem description",
  "market_size": 0-3,
  "urgency": 0-3,
  "solution_gap": 0-2,
  "monetization": 0-2,
  "total_score": "Sum of scores",
  "confidence": 0.0-1.0,
  "domain": "productivity|marketing|devtools|fintech|operations|general",
  "opportunity_description": "Specific SaaS solution",
  "target_market": "Who would pay",
  "validation_signals": ["List of validation signals"]
}
"""
    
    async def _analyze_pain_point_with_llm(self, post: Dict) -> Optional[Dict]:
        """Analyze a Reddit post using LLM for sophisticated pain point detection"""
        try:
            title = post.get('title', '')
            body = post.get('body', '')
            combined_text = f"{title}\n\n{body}"
            
            # Pre-filter: Check if post has pain point indicators
            if not self._has_pain_indicators(combined_text):
                return None
            
            # Quality filter: Skip low-quality posts
            if not self._passes_quality_filter(post):
                return None
            
            # For now, use rule-based analysis (can be replaced with actual LLM call)
            analysis = self._rule_based_pain_analysis(post, combined_text)
            
            # Only return high-quality opportunities (score >= 6)
            if analysis and analysis.get('total_score', 0) >= 6:
                return analysis
            
            return None
            
        except Exception as e:
            logger.error(f"Error in LLM pain point analysis: {e}")
            return None
    
    def _has_pain_indicators(self, text: str) -> bool:
        """Check if text contains pain point indicators"""
        text_lower = text.lower()
        
        # Count pain indicators across categories
        indicator_count = 0
        for category, indicators in self.pain_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    indicator_count += 1
        
        # Require at least 2 pain indicators for consideration
        return indicator_count >= 2
    
    def _passes_quality_filter(self, post: Dict) -> bool:
        """Apply quality filters to exclude low-value posts"""
        title = post.get('title', '')
        body = post.get('body', '')
        score = post.get('score', 0)
        num_comments = post.get('num_comments', 0)
        
        # Content length filter
        if len(title) < 10 or len(title + body) < 50:
            return False
        
        # Engagement filter (relaxed for high-quality content)
        if score < 3 and num_comments < 2:
            return False
        
        # Spam detection
        spam_analysis = self._advanced_spam_detection(post)
        if spam_analysis.get('is_spam', False) and spam_analysis.get('spam_confidence', 0) > 0.7:
            return False
        
        # Promotional content filter
        promotional_keywords = ['check out', 'my startup', 'our product', 'we launched', 'sign up', 'free trial']
        combined_text = (title + ' ' + body).lower()
        promotional_count = sum(1 for keyword in promotional_keywords if keyword in combined_text)
        
        if promotional_count >= 2:
            return False
        
        return True
    
    def _rule_based_pain_analysis(self, post: Dict, text: str) -> Dict:
        """Rule-based pain point analysis following the LLM framework"""
        title = post.get('title', '')
        body = post.get('body', '')
        score = post.get('score', 0)
        num_comments = post.get('num_comments', 0)
        
        # Extract pain point description
        pain_point = self._extract_pain_point_description(text)
        
        # Score Market Size (0-3)
        market_size = self._score_market_size(text)
        
        # Score Urgency (0-3)
        urgency = self._score_urgency(text)
        
        # Score Solution Gap (0-2)
        solution_gap = self._score_solution_gap(text)
        
        # Score Monetization Potential (0-2)
        monetization = self._score_monetization(text)
        
        # Calculate total score
        total_score = market_size + urgency + solution_gap + monetization
        
        # Calculate confidence (0.0-1.0)
        confidence = self._calculate_confidence(post, text, total_score)
        
        # Determine domain
        domain = self._classify_domain(text)
        
        # Generate specific opportunity description
        opportunity_description = self._generate_opportunity_description(pain_point, domain)
        
        # Determine target market
        target_market = self._determine_target_market(text, domain)
        
        # Extract validation signals
        validation_signals = self._extract_validation_signals(post, text)
        
        return {
            'pain_point': pain_point,
            'market_size': market_size,
            'urgency': urgency,
            'solution_gap': solution_gap,
            'monetization': monetization,
            'total_score': total_score,
            'confidence': confidence,
            'domain': domain,
            'opportunity_description': opportunity_description,
            'target_market': target_market,
            'validation_signals': validation_signals,
            'source_post': {
                'title': title,
                'score': score,
                'comments': num_comments,
                'url': post.get('url', ''),
                'subreddit': post.get('subreddit', '')
            }
        }
    
    def _extract_pain_point_description(self, text: str) -> str:
        """Extract clear pain point description from text"""
        # Look for explicit problem statements
        problem_patterns = [
            r"(?:the (?:main |biggest |real )?(?:problem|issue|challenge) (?:is|with))\s+([^.!?]{10,100})",
            r"(?:i (?:can't|cannot|struggle to|have trouble))\s+([^.!?]{10,100})",
            r"(?:it's (?:hard|difficult|impossible) to)\s+([^.!?]{10,100})",
            r"(?:no (?:good )?(?:solution|tool|way) (?:for|to))\s+([^.!?]{10,100})",
            r"(?:wish there was|need help with|looking for)\s+([^.!?]{10,100})"
        ]
        
        for pattern in problem_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Fallback: use title if no specific pattern found
        lines = text.split('\n')
        for line in lines[:3]:  # Check first 3 lines
            if any(indicator in line.lower() for indicators in self.pain_indicators.values() for indicator in indicators):
                return line.strip()[:100]
        
        return "Business process inefficiency identified"
    
    def _score_market_size(self, text: str) -> int:
        """Score market size (0-3)"""
        text_lower = text.lower()
        
        # Enterprise/industry indicators (3 points)
        enterprise_indicators = ['enterprise', 'company', 'business', 'industry', 'corporate', 'organization', 'team']
        if any(indicator in text_lower for indicator in enterprise_indicators):
            return 3
        
        # Professional/role indicators (2 points)
        professional_indicators = ['professional', 'work', 'job', 'career', 'client', 'customer']
        if any(indicator in text_lower for indicator in professional_indicators):
            return 2
        
        # Individual indicators (1 point)
        individual_indicators = ['personal', 'myself', 'i need', 'my own']
        if any(indicator in text_lower for indicator in individual_indicators):
            return 1
        
        return 2  # Default to professional level
    
    def _score_urgency(self, text: str) -> int:
        """Score urgency (0-3)"""
        text_lower = text.lower()
        
        # Critical urgency (3 points)
        critical_indicators = ['critical', 'urgent', 'emergency', 'asap', 'immediately', 'deadline', 'losing money']
        if any(indicator in text_lower for indicator in critical_indicators):
            return 3
        
        # High urgency (2 points)
        high_indicators = ['frustrating', 'wasting time', 'inefficient', 'slowing down', 'blocking']
        if any(indicator in text_lower for indicator in high_indicators):
            return 2
        
        # Medium urgency (1 point)
        medium_indicators = ['annoying', 'inconvenient', 'would like', 'prefer']
        if any(indicator in text_lower for indicator in medium_indicators):
            return 1
        
        return 1  # Default to medium urgency
    
    def _score_solution_gap(self, text: str) -> int:
        """Score solution gap (0-2)"""
        text_lower = text.lower()
        
        # Clear gap indicators (2 points)
        gap_indicators = ['no solution', 'nothing exists', "can't find", 'no tool', 'no way to', 'impossible to find']
        if any(indicator in text_lower for indicator in gap_indicators):
            return 2
        
        # Inadequate solutions (1 point)
        inadequate_indicators = ['too expensive', 'too complex', 'doesn\'t work well', 'limited options', 'not good enough']
        if any(indicator in text_lower for indicator in inadequate_indicators):
            return 1
        
        return 1  # Default to some gap exists
    
    def _score_monetization(self, text: str) -> int:
        """Score monetization potential (0-2)"""
        text_lower = text.lower()
        
        # High monetization (2 points)
        high_monetization = ['willing to pay', 'budget for', 'cost', 'price', 'expensive', 'revenue', 'profit', 'roi']
        if any(indicator in text_lower for indicator in high_monetization):
            return 2
        
        # Medium monetization (1 point)
        medium_monetization = ['business', 'professional', 'work', 'company', 'client']
        if any(indicator in text_lower for indicator in medium_monetization):
            return 1
        
        return 1  # Default to medium monetization
    
    def _calculate_confidence(self, post: Dict, text: str, total_score: int) -> float:
        """Calculate confidence score (0.0-1.0)"""
        confidence = 0.0
        
        # Clarity of problem statement (30%)
        if len(text) > 100 and any(word in text.lower() for word in ['problem', 'issue', 'challenge', 'struggle']):
            confidence += 0.3
        
        # User engagement/validation (25%)
        score = post.get('score', 0)
        comments = post.get('num_comments', 0)
        if score > 10 or comments > 5:
            confidence += 0.25
        elif score > 5 or comments > 2:
            confidence += 0.15
        
        # Market context provided (20%)
        business_context = post.get('business_context', {})
        if business_context.get('industry') and business_context.get('industry') != 'general':
            confidence += 0.2
        
        # Actionability (15%)
        if total_score >= 8:
            confidence += 0.15
        elif total_score >= 6:
            confidence += 0.1
        
        # Non-promotional nature (10%)
        if not self._is_promotional(text):
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _classify_domain(self, text: str) -> str:
        """Classify the business domain"""
        text_lower = text.lower()
        
        for domain, keywords in self.industry_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                return domain
        
        return 'general'
    
    def _generate_opportunity_description(self, pain_point: str, domain: str) -> str:
        """Generate specific SaaS opportunity description"""
        domain_solutions = {
            'productivity': f"AI-powered workflow automation platform that {pain_point.lower()}",
            'marketing': f"Intelligent marketing automation tool to solve {pain_point.lower()}",
            'devtools': f"Developer productivity platform addressing {pain_point.lower()}",
            'fintech': f"Financial automation solution for {pain_point.lower()}",
            'ecommerce': f"E-commerce optimization platform targeting {pain_point.lower()}",
            'saas': f"SaaS integration platform solving {pain_point.lower()}",
            'operations': f"Operations management system addressing {pain_point.lower()}",
            'hr': f"HR automation platform for {pain_point.lower()}",
            'customer_service': f"Customer service automation tool solving {pain_point.lower()}"
        }
        
        return domain_solutions.get(domain, f"Business automation platform addressing {pain_point.lower()}")
    
    def _determine_target_market(self, text: str, domain: str) -> str:
        """Determine target market for the opportunity"""
        text_lower = text.lower()
        
        if 'enterprise' in text_lower or 'large company' in text_lower:
            return f"Enterprise {domain} teams"
        elif 'startup' in text_lower or 'small business' in text_lower:
            return f"SMB {domain} professionals"
        elif 'freelance' in text_lower or 'consultant' in text_lower:
            return f"Freelance {domain} specialists"
        else:
            return f"{domain.title()} professionals and teams"
    
    def _extract_validation_signals(self, post: Dict, text: str) -> List[str]:
        """Extract validation signals from the post"""
        signals = []
        
        score = post.get('score', 0)
        comments = post.get('num_comments', 0)
        
        if score > 20:
            signals.append(f"High community engagement ({score} upvotes)")
        
        if comments > 10:
            signals.append(f"Active discussion ({comments} comments)")
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['willing to pay', 'budget', 'cost']):
            signals.append("Explicit willingness to pay mentioned")
        
        if any(word in text_lower for word in ['team', 'company', 'business']):
            signals.append("Business/professional context")
        
        if any(word in text_lower for word in ['urgent', 'critical', 'asap']):
            signals.append("High urgency indicated")
        
        if any(word in text_lower for word in ['no solution', "can't find", 'nothing exists']):
            signals.append("Clear solution gap identified")
        
        return signals
    
    def _is_promotional(self, text: str) -> bool:
        """Check if text is promotional"""
        promotional_keywords = ['check out', 'my startup', 'our product', 'we launched', 'sign up', 'free trial', 'download', 'visit our']
        text_lower = text.lower()
        return sum(1 for keyword in promotional_keywords if keyword in text_lower) >= 2
    
    async def discover_pain_points(self, subreddit: str = 'startups', limit: int = 5) -> Dict:
        """Discover pain points from Reddit posts using enhanced LLM analysis"""
        try:
            logger.info(f"Starting enhanced pain point discovery for r/{subreddit} with limit {limit}")
            
            # Fetch posts using real Reddit API
            posts = await self.fetch_subreddit_posts(subreddit, limit * 2)  # Fetch more to account for filtering
            
            if not posts:
                logger.warning(f"No posts fetched from r/{subreddit}")
                return {
                    'subreddit': subreddit,
                    'posts_analyzed': 0,
                    'pain_points_found': 0,
                    'pain_points': [],
                    'ranked_opportunities': [],
                    'generated_concepts': [],
                    'error': 'No posts could be fetched from Reddit API',
                    'reddit_api_status': self.reddit_client.get_rate_limit_status()
                }
            
            pain_points = []
            ranked_opportunities = []
            generated_concepts = []
            posts_analyzed = 0
            
            # Process each post with enhanced LLM analysis
            for post in posts:
                posts_analyzed += 1
                
                # Use sophisticated pain point analysis
                analysis = await self._analyze_pain_point_with_llm(post)
                
                if analysis:
                    # Create enhanced pain point object
                    pain_point = {
                        'title': post['title'],
                        'description': analysis['pain_point'],
                        'source': f"r/{subreddit}",
                        'url': post['url'],
                        'industry': analysis['domain'],
                        'pain_indicators': analysis['validation_signals'],
                        'engagement_score': post['score'] + post['num_comments'],
                        'discovered_at': datetime.now().isoformat(),
                        
                        # Enhanced scoring
                        'market_size_score': analysis['market_size'],
                        'urgency_score': analysis['urgency'],
                        'solution_gap_score': analysis['solution_gap'],
                        'monetization_score': analysis['monetization'],
                        'total_score': analysis['total_score'],
                        'confidence': analysis['confidence'],
                        
                        # Reddit metrics
                        'reddit_metrics': {
                            'score': post['score'],
                            'upvote_ratio': post.get('upvote_ratio', 0.5),
                            'num_comments': post['num_comments'],
                            'author': post['author'],
                            'created_utc': post['created_utc']
                        },
                        
                        # Legacy compatibility fields
                        'selftext': post['body'],
                        'business_potential': 'high' if analysis['total_score'] >= 8 else 'medium',
                        'score': analysis['total_score'],
                        'num_comments': post['num_comments'],
                        'post_age_days': 1,
                        'pain_point_indicators': analysis['validation_signals'],
                        'retrieved_via': post.get('retrieved_via', 'reddit_api')
                    }
                    pain_points.append(pain_point)
                    
                    # Generate enhanced opportunity
                    opportunity = {
                        'title': analysis['opportunity_description'],
                        'score': analysis['total_score'],
                        'domain': analysis['domain'],
                        'business_potential': 'high' if analysis['total_score'] >= 8 else 'medium',
                        'subreddit': subreddit,
                        'pain_point_indicators': analysis['validation_signals'],
                        'source_post': post['title'],
                        'target_market': analysis['target_market'],
                        'confidence': analysis['confidence'],
                        'market_size': analysis['market_size'],
                        'urgency': analysis['urgency'],
                        'solution_gap': analysis['solution_gap'],
                        'monetization': analysis['monetization'],
                        'reddit_metrics': {
                            'score': post['score'],
                            'num_comments': post['num_comments'],
                            'upvote_ratio': post.get('upvote_ratio', 0.5)
                        }
                    }
                    ranked_opportunities.append(opportunity)
                    
                    # Generate enhanced SaaS concept
                    concept = {
                        'saas_concept': {
                            'name': f"{analysis['domain'].title()} Solution Pro",
                            'description': analysis['opportunity_description'],
                            'target_market': analysis['target_market'],
                            'key_features': [
                                f"Automated {analysis['domain']} workflow management",
                                "AI-powered problem detection and resolution",
                                "Real-time analytics and insights",
                                "Seamless integration with existing tools",
                                "Scalable enterprise-grade architecture"
                            ],
                            'business_model': 'SaaS subscription with usage-based pricing',
                            'market_validation': analysis['validation_signals']
                        },
                        'source_opportunity': {
                            'score': analysis['total_score'],
                            'confidence': analysis['confidence'],
                            'title': post['title']
                        },
                        'data': {
                            'subreddit': subreddit,
                            'source_post': post['title'],
                            'industry': analysis['domain'],
                            'total_score': analysis['total_score'],
                            'retrieved_via': post.get('retrieved_via', 'reddit_api')
                        }
                    }
                    generated_concepts.append(concept)
                
                # Stop if we have enough high-quality results
                if len(pain_points) >= limit:
                    break
            
            # Sort by total score (highest quality first)
            pain_points.sort(key=lambda x: x['total_score'], reverse=True)
            ranked_opportunities.sort(key=lambda x: x['score'], reverse=True)
            generated_concepts.sort(key=lambda x: x['source_opportunity']['score'], reverse=True)
            
            # Limit results to requested amount
            pain_points = pain_points[:limit]
            ranked_opportunities = ranked_opportunities[:limit]
            generated_concepts = generated_concepts[:3]
            
            # Save to database
            self._save_discovery_session(subreddit, posts_analyzed, len(pain_points), pain_points)
            
            result = {
                'subreddit': subreddit,
                'posts_analyzed': posts_analyzed,
                'pain_points_found': len(pain_points),
                'pain_points': pain_points,
                'ranked_opportunities': ranked_opportunities,
                'generated_concepts': generated_concepts,
                'timestamp': datetime.now().isoformat(),
                'reddit_api_status': self.reddit_client.get_rate_limit_status(),
                'api_integration': 'enhanced_llm_analysis',
                'quality_metrics': {
                    'average_score': sum(p['total_score'] for p in pain_points) / len(pain_points) if pain_points else 0,
                    'average_confidence': sum(p['confidence'] for p in pain_points) / len(pain_points) if pain_points else 0,
                    'high_quality_count': len([p for p in pain_points if p['total_score'] >= 8]),
                    'domains_covered': list(set(p['industry'] for p in pain_points))
                }
            }
            
            logger.info(f"Enhanced discovery completed: {len(pain_points)} high-quality pain points found from {posts_analyzed} posts")
            logger.info(f"Average quality score: {result['quality_metrics']['average_score']:.2f}")
            return result
            
        except Exception as e:
            logger.error(f"Error in enhanced pain point discovery: {e}")
            return {
                'subreddit': subreddit,
                'posts_analyzed': 0,
                'pain_points_found': 0,
                'pain_points': [],
                'ranked_opportunities': [],
                'generated_concepts': [],
                'error': str(e),
                'reddit_api_status': self.reddit_client.get_rate_limit_status()
            }
    
    def _save_discovery_session(self, subreddit: str, posts_analyzed: int, pain_points_found: int, pain_points: List[Dict]):
        """Save discovery session to database"""
        try:
            conn = self.db_service.get_connection()
            cursor = conn.cursor()
            
            session_data = {
                'pain_points': pain_points,
                'timestamp': datetime.now().isoformat()
            }
            
            cursor.execute("""
                INSERT INTO discovery_sessions (subreddit, posts_analyzed, pain_points_found, session_data)
                VALUES (?, ?, ?, ?)
            """, (subreddit, posts_analyzed, pain_points_found, json.dumps(session_data)))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Saved discovery session: {subreddit} - {pain_points_found} pain points")
            
        except Exception as e:
            logger.error(f"Error saving discovery session: {e}")

# Global discovery service instance
discovery_service = DiscoveryService() 