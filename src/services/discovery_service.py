"""
Luciq Discovery Service
Extracted from master_luciq_api.py - Phase 3 Performance & Scalability Optimization

Advanced business opportunity discovery and pain point analysis
"""

import logging
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class MasterDiscoveryService:
    """
    Master discovery service for business opportunity identification
    
    Capabilities:
    - Reddit-based pain point discovery
    - Business context analysis
    - Market opportunity scoring
    - Validation signal extraction
    """
    
    def __init__(self, db_service=None, reddit_client=None):
        self.db_service = db_service
        self.reddit_client = reddit_client
        
        # Pain point indicators for business analysis
        self.pain_indicators = [
            'problem', 'issue', 'challenge', 'difficult', 'frustrating', 'annoying',
            'broken', 'doesn\'t work', 'need help', 'struggling', 'pain point',
            'wish there was', 'if only', 'why isn\'t there', 'someone should build',
            'hate that', 'terrible', 'awful', 'sucks', 'waste of time'
        ]
        
        # Business opportunity keywords
        self.business_keywords = [
            'startup', 'business', 'entrepreneur', 'saas', 'revenue', 'customers',
            'market', 'product', 'service', 'solution', 'opportunity', 'idea',
            'launch', 'funding', 'investment', 'growth', 'scale', 'monetize'
        ]
        
        # Market size indicators
        self.market_size_keywords = {
            'large': ['enterprise', 'corporate', 'industry', 'global', 'worldwide'],
            'medium': ['business', 'company', 'startup', 'small business'],
            'small': ['personal', 'individual', 'hobby', 'side project']
        }
        
        # Urgency indicators
        self.urgency_keywords = [
            'urgent', 'asap', 'immediately', 'critical', 'emergency', 'deadline',
            'time sensitive', 'right now', 'quickly', 'fast'
        ]
        
        # Solution gap indicators
        self.solution_gap_keywords = [
            'no solution', 'nothing works', 'tried everything', 'no options',
            'doesn\'t exist', 'wish there was', 'someone should build',
            'why isn\'t there', 'missing', 'gap in market'
        ]
        
        # Monetization indicators
        self.monetization_keywords = [
            'pay for', 'would buy', 'subscription', 'pricing', 'cost',
            'expensive', 'cheap', 'affordable', 'budget', 'worth it'
        ]
    
    async def discover_pain_points(self, subreddit: str = 'startups', limit: int = 5) -> Dict:
        """
        Discover pain points and business opportunities from Reddit
        
        Args:
            subreddit: Target subreddit for discovery
            limit: Number of posts to analyze
            
        Returns:
            Discovery results with pain points and opportunities
        """
        session_id = str(uuid.uuid4())
        logger.info(f"Starting discovery session {session_id} on r/{subreddit}")
        
        try:
            # Get posts from Reddit (if client available)
            posts = []
            if self.reddit_client:
                posts = await self.reddit_client.get_subreddit_posts(
                    subreddit=subreddit,
                    sort='new',
                    limit=limit * 2,  # Get more posts to filter
                    time_filter='day'
                )
            
            if not posts:
                logger.warning(f"No posts found in r/{subreddit}")
                return self._create_empty_result(session_id, subreddit)
            
            # Analyze posts for pain points
            pain_points = []
            posts_analyzed = 0
            
            for post in posts:
                if posts_analyzed >= limit:
                    break
                
                pain_point = await self._analyze_post_for_pain_points(post)
                if pain_point:
                    pain_points.append(pain_point)
                    # Save to database if available
                    if self.db_service:
                        await self.db_service.save_pain_point(session_id, pain_point)
                
                posts_analyzed += 1
            
            # Save discovery session if database available
            if self.db_service:
                await self.db_service.save_discovery_session(
                    session_id=session_id,
                    user_id=1,  # Default user for now
                    subreddit=subreddit,
                    posts_analyzed=posts_analyzed,
                    pain_points_found=len(pain_points)
                )
            
            # Sort pain points by total score
            pain_points.sort(key=lambda x: x.get('total_score', 0), reverse=True)
            
            result = {
                'success': True,
                'session_id': session_id,
                'subreddit': subreddit,
                'posts_analyzed': posts_analyzed,
                'pain_points_found': len(pain_points),
                'pain_points': pain_points,
                'timestamp': datetime.now().isoformat(),
                'discovery_metadata': {
                    'source': 'reddit',
                    'analysis_method': 'rule_based_with_scoring',
                    'filters_applied': ['business_relevance', 'spam_detection'],
                    'scoring_components': ['market_size', 'urgency', 'solution_gap', 'monetization']
                }
            }
            
            logger.info(f"Discovery session {session_id} completed: {len(pain_points)} pain points found")
            return result
            
        except Exception as e:
            logger.error(f"Discovery session {session_id} failed: {e}")
            return self._create_error_result(session_id, subreddit, str(e))
    
    async def _analyze_post_for_pain_points(self, post: Dict) -> Optional[Dict]:
        """Analyze a single post for pain points and business opportunities"""
        try:
            title = post.get('title', '')
            body = post.get('body', '')
            text = f"{title} {body}".lower()
            
            # Check if post has pain indicators
            if not self._has_pain_indicators(text):
                return None
            
            # Perform rule-based analysis
            analysis = self._rule_based_pain_analysis(post, text)
            
            # Calculate confidence score
            confidence = self._calculate_confidence(post, text, analysis['total_score'])
            
            # Only return if confidence is above threshold
            if confidence < 0.3:
                return None
            
            # Extract additional business context
            pain_point = {
                'post_id': post.get('id'),
                'title': title,
                'description': self._extract_pain_point_description(text),
                'url': post.get('url'),
                'author': post.get('author'),
                'upvotes': post.get('upvotes', 0),
                'comments': post.get('comments', 0),
                'created_datetime': post.get('created_datetime'),
                'domain': self._classify_domain(text),
                'market_size_score': analysis['market_size_score'],
                'urgency_score': analysis['urgency_score'],
                'solution_gap_score': analysis['solution_gap_score'],
                'monetization_score': analysis['monetization_score'],
                'total_score': analysis['total_score'],
                'confidence_score': confidence,
                'target_market': self._determine_target_market(text, analysis['domain']),
                'opportunity_description': self._generate_opportunity_description(
                    analysis['pain_point'], analysis['domain']
                ),
                'validation_signals': self._extract_validation_signals(post, text)
            }
            
            return pain_point
            
        except Exception as e:
            logger.error(f"Failed to analyze post {post.get('id', 'unknown')}: {e}")
            return None
    
    def _has_pain_indicators(self, text: str) -> bool:
        """Check if text contains pain point indicators"""
        return any(indicator in text for indicator in self.pain_indicators)
    
    def _rule_based_pain_analysis(self, post: Dict, text: str) -> Dict:
        """Perform rule-based pain point analysis"""
        # Score different aspects
        market_size_score = self._score_market_size(text)
        urgency_score = self._score_urgency(text)
        solution_gap_score = self._score_solution_gap(text)
        monetization_score = self._score_monetization(text)
        
        # Calculate total score
        total_score = market_size_score + urgency_score + solution_gap_score + monetization_score
        
        # Extract pain point description
        pain_point = self._extract_pain_point_description(text)
        
        # Classify domain
        domain = self._classify_domain(text)
        
        return {
            'pain_point': pain_point,
            'domain': domain,
            'market_size_score': market_size_score,
            'urgency_score': urgency_score,
            'solution_gap_score': solution_gap_score,
            'monetization_score': monetization_score,
            'total_score': total_score
        }
    
    def _score_market_size(self, text: str) -> int:
        """Score market size potential (0-3)"""
        score = 0
        
        # Check for market size indicators
        for size, keywords in self.market_size_keywords.items():
            if any(keyword in text for keyword in keywords):
                if size == 'large':
                    score = 3
                elif size == 'medium':
                    score = 2
                elif size == 'small':
                    score = 1
                break
        
        # Boost score for business-related content
        if any(keyword in text for keyword in self.business_keywords):
            score += 1
        
        return min(score, 3)
    
    def _score_urgency(self, text: str) -> int:
        """Score urgency level (0-3)"""
        score = 0
        
        # Count urgency indicators
        urgency_count = sum(1 for keyword in self.urgency_keywords if keyword in text)
        
        if urgency_count >= 3:
            score = 3
        elif urgency_count >= 2:
            score = 2
        elif urgency_count >= 1:
            score = 1
        
        return score
    
    def _score_solution_gap(self, text: str) -> int:
        """Score solution gap (0-3)"""
        score = 0
        
        # Count solution gap indicators
        gap_count = sum(1 for keyword in self.solution_gap_keywords if keyword in text)
        
        if gap_count >= 2:
            score = 3
        elif gap_count >= 1:
            score = 2
        
        # Additional scoring for specific phrases
        if 'no good solution' in text or 'nothing available' in text:
            score += 1
        
        return min(score, 3)
    
    def _score_monetization(self, text: str) -> int:
        """Score monetization potential (0-3)"""
        score = 0
        
        # Count monetization indicators
        monetization_count = sum(1 for keyword in self.monetization_keywords if keyword in text)
        
        if monetization_count >= 3:
            score = 3
        elif monetization_count >= 2:
            score = 2
        elif monetization_count >= 1:
            score = 1
        
        return score
    
    def _calculate_confidence(self, post: Dict, text: str, total_score: int) -> float:
        """Calculate confidence score for the analysis"""
        confidence = 0.0
        
        # Base confidence from total score
        confidence += min(total_score / 12.0, 0.4)  # Max 0.4 from scoring
        
        # Engagement indicators
        upvotes = post.get('upvotes', 0)
        comments = post.get('comments', 0)
        
        if upvotes > 10:
            confidence += 0.1
        if comments > 5:
            confidence += 0.1
        
        # Content quality indicators
        if len(text) > 100:  # Substantial content
            confidence += 0.1
        if len(text) > 300:  # Detailed content
            confidence += 0.1
        
        # Business relevance
        business_score = sum(1 for keyword in self.business_keywords if keyword in text)
        confidence += min(business_score / 10.0, 0.2)  # Max 0.2 from business relevance
        
        return min(confidence, 1.0)
    
    def _extract_pain_point_description(self, text: str) -> str:
        """Extract a concise pain point description"""
        # Look for sentences containing pain indicators
        sentences = text.split('.')
        
        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in self.pain_indicators):
                # Clean and return the sentence
                clean_sentence = sentence.strip()
                if len(clean_sentence) > 20 and len(clean_sentence) < 200:
                    return clean_sentence
        
        # Fallback: return first part of text
        return text[:150] + "..." if len(text) > 150 else text
    
    def _classify_domain(self, text: str) -> str:
        """Classify the business domain"""
        domains = {
            'saas': ['software', 'app', 'platform', 'tool', 'service', 'api'],
            'ecommerce': ['shop', 'store', 'buy', 'sell', 'product', 'marketplace'],
            'fintech': ['payment', 'money', 'finance', 'bank', 'crypto', 'investment'],
            'healthtech': ['health', 'medical', 'doctor', 'patient', 'healthcare'],
            'edtech': ['education', 'learning', 'course', 'student', 'teach'],
            'productivity': ['productivity', 'workflow', 'automation', 'efficiency'],
            'marketing': ['marketing', 'advertising', 'social media', 'content'],
            'hr': ['hiring', 'recruitment', 'employee', 'hr', 'human resources']
        }
        
        for domain, keywords in domains.items():
            if any(keyword in text for keyword in keywords):
                return domain
        
        return 'general'
    
    def _generate_opportunity_description(self, pain_point: str, domain: str) -> str:
        """Generate opportunity description based on pain point and domain"""
        templates = {
            'saas': f"Software solution opportunity to address: {pain_point}",
            'ecommerce': f"E-commerce platform opportunity for: {pain_point}",
            'fintech': f"Financial technology solution for: {pain_point}",
            'healthtech': f"Healthcare technology opportunity: {pain_point}",
            'edtech': f"Educational technology solution: {pain_point}",
            'productivity': f"Productivity enhancement opportunity: {pain_point}",
            'marketing': f"Marketing technology solution: {pain_point}",
            'hr': f"HR technology opportunity: {pain_point}",
            'general': f"Business opportunity identified: {pain_point}"
        }
        
        return templates.get(domain, templates['general'])
    
    def _determine_target_market(self, text: str, domain: str) -> str:
        """Determine target market for the opportunity"""
        if 'enterprise' in text or 'corporate' in text:
            return 'Enterprise'
        elif 'small business' in text or 'startup' in text:
            return 'SMB/Startups'
        elif 'consumer' in text or 'personal' in text:
            return 'Consumer'
        else:
            return 'Business' if domain != 'general' else 'General'
    
    def _extract_validation_signals(self, post: Dict, text: str) -> List[str]:
        """Extract validation signals from the post"""
        signals = []
        
        # Engagement signals
        upvotes = post.get('upvotes', 0)
        comments = post.get('comments', 0)
        
        if upvotes > 20:
            signals.append(f"High engagement: {upvotes} upvotes")
        if comments > 10:
            signals.append(f"Active discussion: {comments} comments")
        
        # Content signals
        if 'would pay' in text or 'pay for' in text:
            signals.append("Willingness to pay mentioned")
        if 'tried everything' in text or 'no solution' in text:
            signals.append("Solution gap confirmed")
        if 'many people' in text or 'everyone' in text:
            signals.append("Market size indicated")
        
        # Authority signals
        if post.get('gilded', 0) > 0:
            signals.append("Post received awards")
        if post.get('author') and 'founder' in text:
            signals.append("Founder/entrepreneur perspective")
        
        return signals
    
    def _create_empty_result(self, session_id: str, subreddit: str) -> Dict:
        """Create empty result when no posts found"""
        return {
            'success': True,
            'session_id': session_id,
            'subreddit': subreddit,
            'posts_analyzed': 0,
            'pain_points_found': 0,
            'pain_points': [],
            'timestamp': datetime.now().isoformat(),
            'message': f"No posts found in r/{subreddit}"
        }
    
    def _create_error_result(self, session_id: str, subreddit: str, error: str) -> Dict:
        """Create error result"""
        return {
            'success': False,
            'session_id': session_id,
            'subreddit': subreddit,
            'posts_analyzed': 0,
            'pain_points_found': 0,
            'pain_points': [],
            'timestamp': datetime.now().isoformat(),
            'error': error
        } 