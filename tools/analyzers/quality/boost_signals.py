#!/usr/bin/env python3
"""
Signal Boost Script - Get to 10,000+ signals immediately
Expand data collection to industry standards
"""

import asyncio
import sys
import os
sys.path.append('src/api')

from services.trend_detection_service import CrossPlatformTrendDetector, TrendSignal
from datetime import datetime, timedelta
import aiohttp
import json

class SignalBooster:
    """Boost signal collection to industry standards"""
    
    def __init__(self):
        self.session = None
        
        # Massive subreddit list (100+ subreddits)
        self.massive_subreddits = [
            # Tier 1: Core Business (High Value)
            'startups', 'entrepreneur', 'SaaS', 'indiehackers', 'smallbusiness',
            'freelance', 'business', 'investing', 'stocks', 'venturecapital',
            'ycombinator', 'growmybusiness', 'EntrepreneurRideAlong',
            
            # Tier 1: Technology (High Value)
            'technology', 'programming', 'webdev', 'MachineLearning', 'artificial',
            'datascience', 'cybersecurity', 'cloudcomputing', 'devops', 'kubernetes',
            'docker', 'aws', 'azure', 'googlecloud', 'serverless',
            
            # Tier 2: Industry Specific
            'fintech', 'healthtech', 'edtech', 'proptech', 'insurtech',
            'legaltech', 'martech', 'hrtech', 'retailtech', 'agtech',
            'cleantech', 'biotech', 'medtech', 'regtech', 'govtech',
            
            # Tier 2: Emerging Tech
            'blockchain', 'cryptocurrency', 'NFTs', 'web3', 'metaverse',
            'VirtualReality', 'AugmentedReality', 'IoT', 'robotics', 'quantum',
            'artificialintelligence', 'deeplearning', 'computervision',
            
            # Tier 2: E-commerce & Marketing
            'ecommerce', 'dropshipping', 'shopify', 'amazon', 'etsy',
            'marketing', 'sales', 'digital_marketing', 'SEO', 'PPC',
            'socialmedia', 'content_marketing', 'email_marketing',
            
            # Tier 3: Pain Points & Problems (Gold Mine)
            'mildlyinfuriating', 'assholedesign', 'crappydesign', 'softwaregore',
            'techsupport', 'sysadmin', 'ITCareerQuestions', 'cscareerquestions',
            'programmerhumor', 'badcode', 'programminghorror',
            
            # Tier 3: Productivity & Tools
            'productivity', 'getmotivated', 'lifehacks', 'organization',
            'timemanagement', 'workflow', 'automation', 'zapier',
            'notion', 'obsidian', 'roamresearch', 'todoist',
            
            # Tier 3: Remote Work & Future
            'remotework', 'digitalnomad', 'workfromhome', 'freelancing',
            'gig_economy', 'future_of_work', 'jobs', 'careerguidance',
            'careerchange', 'findapath', 'cscareeradvice',
            
            # Tier 3: Creator Economy
            'youtube', 'twitch', 'tiktok', 'instagram', 'content_creation',
            'influencer', 'podcasting', 'blogging', 'writing', 'photography',
            'videography', 'streaming', 'onlyfans', 'patreon',
            
            # Tier 4: Niche Markets
            'personalfinance', 'investing', 'stocks', 'options', 'cryptocurrency',
            'realestate', 'landlord', 'flipping', 'passive_income',
            'sidehustle', 'beermoney', 'workonline', 'slavelabour'
        ]
    
    async def boost_signal_collection(self, hours_back: int = 24) -> dict:
        """Collect massive signals from expanded sources"""
        
        print(f"🚀 Starting MASSIVE signal collection...")
        print(f"📊 Target: 10,000+ signals from {len(self.massive_subreddits)} subreddits")
        print("=" * 60)
        
        self.session = aiohttp.ClientSession()
        
        try:
            # Collect from all subreddits in parallel batches
            batch_size = 10  # Process 10 subreddits at a time
            all_signals = []
            
            for i in range(0, len(self.massive_subreddits), batch_size):
                batch = self.massive_subreddits[i:i + batch_size]
                print(f"\n📱 Processing batch {i//batch_size + 1}: {batch}")
                
                # Collect from batch in parallel
                batch_tasks = [
                    self._collect_subreddit_signals(subreddit, hours_back)
                    for subreddit in batch
                ]
                
                batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
                
                batch_signals = 0
                for result in batch_results:
                    if isinstance(result, list):
                        all_signals.extend(result)
                        batch_signals += len(result)
                    elif isinstance(result, Exception):
                        print(f"   ❌ Error: {result}")
                
                print(f"   ✅ Batch collected: {batch_signals} signals")
                print(f"   📊 Total so far: {len(all_signals)} signals")
                
                # Rate limiting between batches
                await asyncio.sleep(2)
            
            # Additional sources
            print(f"\n🔥 Collecting from additional sources...")
            
            additional_tasks = [
                self._collect_github_expanded(hours_back),
                self._collect_stackoverflow_expanded(hours_back),
                self._collect_devto_expanded(hours_back),
                self._collect_hackernews_expanded(hours_back)
            ]
            
            additional_results = await asyncio.gather(*additional_tasks, return_exceptions=True)
            
            additional_signals = 0
            for result in additional_results:
                if isinstance(result, list):
                    all_signals.extend(result)
                    additional_signals += len(result)
            
            print(f"   ✅ Additional sources: {additional_signals} signals")
            
            # Final stats
            total_signals = len(all_signals)
            unique_sources = len(set(s.source for s in all_signals))
            
            print("\n" + "=" * 60)
            print(f"🎉 SIGNAL COLLECTION COMPLETE!")
            print(f"📊 Total Signals: {total_signals:,}")
            print(f"🔗 Unique Sources: {unique_sources}")
            print(f"⚡ Signals/Hour: {total_signals/hours_back:.1f}")
            
            if total_signals >= 10000:
                print("🏆 INDUSTRY STANDARD ACHIEVED! (10,000+ signals)")
            elif total_signals >= 5000:
                print("🥈 EXCELLENT! (5,000+ signals)")
            elif total_signals >= 1000:
                print("🥉 GOOD! (1,000+ signals)")
            else:
                print("⚠️  Need more signals for industry standards")
            
            # Analyze signal quality
            engagement_scores = [s.engagement_score for s in all_signals]
            avg_engagement = sum(engagement_scores) / len(engagement_scores) if engagement_scores else 0
            
            print(f"📈 Average Engagement: {avg_engagement:.1f}")
            print(f"🎯 High-Engagement Signals: {len([s for s in all_signals if s.engagement_score > 50])}")
            
            return {
                'total_signals': total_signals,
                'unique_sources': unique_sources,
                'signals': all_signals,
                'avg_engagement': avg_engagement,
                'industry_standard': total_signals >= 10000
            }
            
        finally:
            await self.session.close()
    
    async def _collect_subreddit_signals(self, subreddit: str, hours_back: int) -> list:
        """Collect signals from a single subreddit"""
        signals = []
        
        try:
            # Get both hot and new posts
            for sort_type in ['hot', 'new']:
                url = f"https://www.reddit.com/r/{subreddit}/{sort_type}.json?limit=100"
                
                async with self.session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        for post_data in data.get('data', {}).get('children', []):
                            post = post_data.get('data', {})
                            
                            # Filter by time
                            post_time = datetime.fromtimestamp(post.get('created_utc', 0))
                            if post_time < datetime.now() - timedelta(hours=hours_back):
                                continue
                            
                            # Extract content
                            title = post.get('title', '')
                            selftext = post.get('selftext', '')
                            content = f"{title} {selftext}"
                            
                            # Basic keyword filtering
                            keywords = self._extract_business_keywords(content)
                            
                            if keywords or len(content) > 50:  # Include if has keywords or substantial content
                                signal = TrendSignal(
                                    source='reddit',
                                    content=content[:500],  # Truncate for storage
                                    timestamp=post_time,
                                    engagement_score=post.get('score', 0) + post.get('num_comments', 0),
                                    sentiment_score=self._simple_sentiment(content),
                                    keywords=keywords,
                                    url=f"https://reddit.com{post.get('permalink', '')}",
                                    metadata={
                                        'subreddit': subreddit,
                                        'author': post.get('author', ''),
                                        'score': post.get('score', 0),
                                        'comments': post.get('num_comments', 0),
                                        'sort_type': sort_type
                                    }
                                )
                                signals.append(signal)
                
                # Rate limiting between requests
                await asyncio.sleep(0.5)
        
        except Exception as e:
            print(f"   ❌ Error collecting from r/{subreddit}: {e}")
        
        return signals
    
    def _extract_business_keywords(self, content: str) -> list:
        """Extract business-relevant keywords"""
        business_keywords = [
            # Core business
            'startup', 'business', 'saas', 'platform', 'tool', 'app', 'api',
            'revenue', 'profit', 'growth', 'scale', 'launch', 'mvp', 'product',
            
            # Technology
            'ai', 'artificial intelligence', 'machine learning', 'automation',
            'blockchain', 'crypto', 'web3', 'cloud', 'mobile', 'software',
            
            # Market indicators
            'problem', 'solution', 'need', 'pain point', 'opportunity',
            'market', 'customer', 'user', 'demand', 'trend', 'popular',
            
            # Business models
            'subscription', 'freemium', 'marketplace', 'ecommerce', 'b2b',
            'b2c', 'enterprise', 'small business', 'freelance', 'remote'
        ]
        
        content_lower = content.lower()
        found_keywords = []
        
        for keyword in business_keywords:
            if keyword in content_lower:
                found_keywords.append(keyword)
        
        return found_keywords[:10]  # Limit to top 10
    
    def _simple_sentiment(self, content: str) -> float:
        """Simple sentiment analysis"""
        positive_words = ['great', 'amazing', 'love', 'awesome', 'excellent', 'perfect', 'solution', 'helpful', 'useful', 'innovative']
        negative_words = ['problem', 'issue', 'broken', 'terrible', 'hate', 'difficult', 'struggle', 'frustrating', 'annoying', 'useless']
        
        content_lower = content.lower()
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        if positive_count + negative_count == 0:
            return 0.5
        
        return positive_count / (positive_count + negative_count)
    
    async def _collect_github_expanded(self, hours_back: int) -> list:
        """Expanded GitHub collection"""
        signals = []
        
        try:
            # Multiple GitHub searches
            search_queries = [
                'created:>=' + (datetime.now() - timedelta(hours=hours_back)).strftime('%Y-%m-%d'),
                'stars:>10 created:>=' + (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
                'language:python stars:>5',
                'language:javascript stars:>5',
                'topic:saas',
                'topic:startup',
                'topic:ai',
                'topic:automation'
            ]
            
            for query in search_queries:
                url = "https://api.github.com/search/repositories"
                params = {'q': query, 'sort': 'stars', 'order': 'desc', 'per_page': 50}
                
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        for repo in data.get('items', []):
                            content = f"{repo.get('name', '')} {repo.get('description', '')}"
                            keywords = self._extract_business_keywords(content)
                            
                            if keywords:
                                signal = TrendSignal(
                                    source='github',
                                    content=content,
                                    timestamp=datetime.now(),
                                    engagement_score=repo.get('stargazers_count', 0),
                                    sentiment_score=0.6,
                                    keywords=keywords,
                                    url=repo.get('html_url', ''),
                                    metadata={
                                        'language': repo.get('language', ''),
                                        'stars': repo.get('stargazers_count', 0),
                                        'forks': repo.get('forks_count', 0),
                                        'query': query
                                    }
                                )
                                signals.append(signal)
                
                await asyncio.sleep(1)  # Rate limiting
        
        except Exception as e:
            print(f"   ❌ GitHub error: {e}")
        
        return signals
    
    async def _collect_stackoverflow_expanded(self, hours_back: int) -> list:
        """Expanded Stack Overflow collection"""
        signals = []
        
        try:
            # Multiple SO searches
            tags = ['javascript', 'python', 'react', 'nodejs', 'api', 'automation', 'ai', 'saas']
            
            for tag in tags:
                url = "https://api.stackexchange.com/2.3/questions"
                params = {
                    'order': 'desc',
                    'sort': 'activity',
                    'tagged': tag,
                    'site': 'stackoverflow',
                    'pagesize': 50
                }
                
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        for question in data.get('items', []):
                            content = f"{question.get('title', '')} {' '.join(question.get('tags', []))}"
                            keywords = self._extract_business_keywords(content)
                            
                            if keywords:
                                signal = TrendSignal(
                                    source='stackoverflow',
                                    content=content,
                                    timestamp=datetime.fromtimestamp(question.get('creation_date', 0)),
                                    engagement_score=question.get('score', 0) + question.get('answer_count', 0),
                                    sentiment_score=0.5,
                                    keywords=keywords,
                                    url=question.get('link', ''),
                                    metadata={
                                        'tags': question.get('tags', []),
                                        'score': question.get('score', 0),
                                        'answers': question.get('answer_count', 0),
                                        'tag_search': tag
                                    }
                                )
                                signals.append(signal)
                
                await asyncio.sleep(1)
        
        except Exception as e:
            print(f"   ❌ Stack Overflow error: {e}")
        
        return signals
    
    async def _collect_devto_expanded(self, hours_back: int) -> list:
        """Expanded Dev.to collection"""
        signals = []
        
        try:
            # Multiple Dev.to searches
            tags = ['startup', 'saas', 'ai', 'automation', 'productivity', 'business', 'javascript', 'python']
            
            for tag in tags:
                url = "https://dev.to/api/articles"
                params = {'tag': tag, 'per_page': 30, 'top': 7}
                
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        articles = await response.json()
                        
                        for article in articles:
                            content = f"{article.get('title', '')} {article.get('description', '')}"
                            keywords = self._extract_business_keywords(content)
                            
                            if keywords:
                                signal = TrendSignal(
                                    source='dev_to',
                                    content=content,
                                    timestamp=datetime.now(),
                                    engagement_score=article.get('positive_reactions_count', 0) + article.get('comments_count', 0),
                                    sentiment_score=0.7,
                                    keywords=keywords,
                                    url=article.get('url', ''),
                                    metadata={
                                        'author': article.get('user', {}).get('name', ''),
                                        'reactions': article.get('positive_reactions_count', 0),
                                        'comments': article.get('comments_count', 0),
                                        'tag_search': tag
                                    }
                                )
                                signals.append(signal)
                
                await asyncio.sleep(1)
        
        except Exception as e:
            print(f"   ❌ Dev.to error: {e}")
        
        return signals
    
    async def _collect_hackernews_expanded(self, hours_back: int) -> list:
        """Expanded Hacker News collection"""
        signals = []
        
        try:
            # Get more HN stories
            story_types = ['topstories', 'newstories', 'beststories']
            
            for story_type in story_types:
                async with self.session.get(f'https://hacker-news.firebaseio.com/v0/{story_type}.json') as response:
                    if response.status == 200:
                        story_ids = await response.json()
                        
                        # Get details for top 50 stories
                        for story_id in story_ids[:50]:
                            try:
                                async with self.session.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json') as story_response:
                                    if story_response.status == 200:
                                        story = await story_response.json()
                                        
                                        content = f"{story.get('title', '')} {story.get('text', '')}"
                                        keywords = self._extract_business_keywords(content)
                                        
                                        if keywords:
                                            signal = TrendSignal(
                                                source='hacker_news',
                                                content=content,
                                                timestamp=datetime.fromtimestamp(story.get('time', 0)),
                                                engagement_score=story.get('score', 0),
                                                sentiment_score=self._simple_sentiment(content),
                                                keywords=keywords,
                                                url=story.get('url', ''),
                                                metadata={
                                                    'score': story.get('score', 0),
                                                    'descendants': story.get('descendants', 0),
                                                    'story_type': story_type
                                                }
                                            )
                                            signals.append(signal)
                            
                            except Exception as e:
                                continue
                            
                            await asyncio.sleep(0.1)
                
                await asyncio.sleep(1)
        
        except Exception as e:
            print(f"   ❌ Hacker News error: {e}")
        
        return signals

async def main():
    """Run the signal boost"""
    booster = SignalBooster()
    results = await booster.boost_signal_collection(hours_back=24)
    
    print(f"\n🎯 RESULTS SUMMARY:")
    print(f"Total Signals: {results['total_signals']:,}")
    print(f"Industry Standard: {'✅ YES' if results['industry_standard'] else '❌ NO'}")
    
    return results

if __name__ == "__main__":
    asyncio.run(main()) 