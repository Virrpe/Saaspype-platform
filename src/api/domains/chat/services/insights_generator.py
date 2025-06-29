#!/usr/bin/env python3
"""
Insights Generator - Advanced Analytics and Visualization for User Ideas
Generates trends, patterns, charts, and actionable insights from idea collections
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter
import math

from .idea_manager import IdeaManager

logger = logging.getLogger(__name__)

class InsightsGenerator:
    """
    Generates intelligent insights and visualizations from user idea data
    """
    
    def __init__(self):
        self.idea_manager = IdeaManager()
        
    async def generate_insights(
        self,
        user_id: str,
        analysis_type: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive insights based on analysis type
        """
        try:
            # Get user's ideas and analytics
            ideas = await self.idea_manager.get_user_ideas(user_id, limit=1000)
            analytics = await self.idea_manager.get_idea_analytics(user_id)
            
            if analysis_type == "trends":
                return await self._analyze_trends(ideas, analytics, filters)
            elif analysis_type == "categories":
                return await self._analyze_categories(ideas, analytics, filters)
            elif analysis_type == "ratings":
                return await self._analyze_ratings(ideas, analytics, filters)
            elif analysis_type == "recommendations":
                return await self._generate_recommendations(ideas, analytics, filters)
            elif analysis_type == "comprehensive":
                return await self._comprehensive_analysis(ideas, analytics, filters)
            else:
                raise ValueError(f"Unknown analysis type: {analysis_type}")
                
        except Exception as e:
            logger.error(f"Generate insights error: {e}")
            raise
    
    async def _analyze_trends(
        self,
        ideas: List[Dict[str, Any]],
        analytics: Dict[str, Any],
        filters: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze trends in user's idea collection"""
        
        # Time-based analysis
        idea_timeline = self._create_timeline_analysis(ideas)
        
        # Category trends
        category_trends = self._analyze_category_trends(ideas)
        
        # Rating trends over time
        rating_trends = self._analyze_rating_trends(ideas)
        
        # Keyword/theme analysis
        theme_analysis = self._analyze_themes(ideas)
        
        # Velocity analysis (ideas per week/month)
        velocity_analysis = self._analyze_idea_velocity(ideas)
        
        return {
            'analysis_type': 'trends',
            'timeline': idea_timeline,
            'category_trends': category_trends,
            'rating_trends': rating_trends,
            'themes': theme_analysis,
            'velocity': velocity_analysis,
            'insights': self._generate_trend_insights(
                idea_timeline, category_trends, rating_trends, velocity_analysis
            )
        }
    
    async def _analyze_categories(
        self,
        ideas: List[Dict[str, Any]],
        analytics: Dict[str, Any],
        filters: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze category distribution and patterns"""
        
        # Category distribution
        category_dist = Counter(idea['category'] for idea in ideas)
        
        # Category performance (average ratings)
        category_performance = {}
        for category in category_dist.keys():
            category_ideas = [idea for idea in ideas if idea['category'] == category]
            rated_ideas = [idea for idea in category_ideas if idea['rating']]
            if rated_ideas:
                avg_rating = sum(idea['rating'] for idea in rated_ideas) / len(rated_ideas)
                category_performance[category] = {
                    'avg_rating': round(avg_rating, 2),
                    'total_ideas': len(category_ideas),
                    'rated_ideas': len(rated_ideas)
                }
        
        # Category growth over time
        category_growth = self._analyze_category_growth(ideas)
        
        # Suggested new categories
        suggested_categories = self._suggest_categories(ideas)
        
        return {
            'analysis_type': 'categories',
            'distribution': dict(category_dist),
            'performance': category_performance,
            'growth': category_growth,
            'suggestions': suggested_categories,
            'insights': self._generate_category_insights(
                category_dist, category_performance, category_growth
            )
        }
    
    async def _analyze_ratings(
        self,
        ideas: List[Dict[str, Any]],
        analytics: Dict[str, Any],
        filters: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze rating patterns and quality metrics"""
        
        rated_ideas = [idea for idea in ideas if idea['rating']]
        
        if not rated_ideas:
            return {
                'analysis_type': 'ratings',
                'message': 'No rated ideas found. Start rating your ideas to see insights!',
                'suggestions': ['Rate your existing ideas', 'Focus on quality over quantity']
            }
        
        # Rating distribution
        rating_dist = Counter(idea['rating'] for idea in rated_ideas)
        
        # Quality metrics
        avg_rating = sum(idea['rating'] for idea in rated_ideas) / len(rated_ideas)
        high_quality_ideas = [idea for idea in rated_ideas if idea['rating'] >= 4]
        low_quality_ideas = [idea for idea in rated_ideas if idea['rating'] <= 2]
        
        # Rating by category
        rating_by_category = {}
        for idea in rated_ideas:
            category = idea['category']
            if category not in rating_by_category:
                rating_by_category[category] = []
            rating_by_category[category].append(idea['rating'])
        
        # Calculate category averages
        category_avg_ratings = {}
        for category, ratings in rating_by_category.items():
            category_avg_ratings[category] = round(sum(ratings) / len(ratings), 2)
        
        # Rating improvement over time
        rating_improvement = self._analyze_rating_improvement(rated_ideas)
        
        return {
            'analysis_type': 'ratings',
            'distribution': dict(rating_dist),
            'average_rating': round(avg_rating, 2),
            'quality_metrics': {
                'high_quality_count': len(high_quality_ideas),
                'low_quality_count': len(low_quality_ideas),
                'quality_ratio': len(high_quality_ideas) / len(rated_ideas) if rated_ideas else 0
            },
            'category_ratings': category_avg_ratings,
            'improvement_trend': rating_improvement,
            'insights': self._generate_rating_insights(
                rating_dist, avg_rating, category_avg_ratings, rating_improvement
            )
        }
    
    async def _generate_recommendations(
        self,
        ideas: List[Dict[str, Any]],
        analytics: Dict[str, Any],
        filters: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate actionable recommendations for the user"""
        
        recommendations = []
        
        # Analyze current state
        total_ideas = len(ideas)
        rated_ideas = [idea for idea in ideas if idea['rating']]
        categories = set(idea['category'] for idea in ideas)
        
        # Recommendation 1: Rating completion
        if len(rated_ideas) < total_ideas * 0.5:
            recommendations.append({
                'type': 'rating_completion',
                'priority': 'high',
                'title': 'Rate Your Ideas',
                'description': f'You have {total_ideas - len(rated_ideas)} unrated ideas. Rating helps prioritize and track quality.',
                'action': 'Rate unrated ideas',
                'impact': 'Better insights and prioritization'
            })
        
        # Recommendation 2: Category diversification
        if len(categories) < 3 and total_ideas > 5:
            recommendations.append({
                'type': 'diversification',
                'priority': 'medium',
                'title': 'Explore New Categories',
                'description': 'Consider exploring ideas in different domains to broaden your innovation scope.',
                'action': 'Brainstorm ideas in new categories',
                'impact': 'Increased innovation potential'
            })
        
        # Recommendation 3: Quality improvement
        if rated_ideas:
            avg_rating = sum(idea['rating'] for idea in rated_ideas) / len(rated_ideas)
            if avg_rating < 3.5:
                recommendations.append({
                    'type': 'quality_improvement',
                    'priority': 'high',
                    'title': 'Focus on Quality',
                    'description': 'Your average idea rating is below 3.5. Consider refining existing ideas or being more selective.',
                    'action': 'Refine low-rated ideas or generate higher-quality concepts',
                    'impact': 'Higher success potential'
                })
        
        # Recommendation 4: Idea development
        high_rated_ideas = [idea for idea in rated_ideas if idea['rating'] >= 4]
        if high_rated_ideas:
            recommendations.append({
                'type': 'development',
                'priority': 'high',
                'title': 'Develop High-Rated Ideas',
                'description': f'You have {len(high_rated_ideas)} high-quality ideas ready for development.',
                'action': 'Create detailed plans for top-rated ideas',
                'impact': 'Turn ideas into reality'
            })
        
        # Recommendation 5: Consistency
        if total_ideas > 0:
            recent_ideas = [
                idea for idea in ideas 
                if datetime.fromisoformat(idea['created_at'].replace('Z', '+00:00')) > 
                   datetime.now() - timedelta(days=7)
            ]
            if len(recent_ideas) == 0:
                recommendations.append({
                    'type': 'consistency',
                    'priority': 'medium',
                    'title': 'Stay Consistent',
                    'description': 'No new ideas in the past week. Regular ideation builds creative momentum.',
                    'action': 'Set a goal to generate 1-2 ideas per week',
                    'impact': 'Sustained innovation flow'
                })
        
        # Generate personalized insights
        personalized_insights = self._generate_personalized_insights(ideas, analytics)
        
        return {
            'analysis_type': 'recommendations',
            'recommendations': recommendations,
            'personalized_insights': personalized_insights,
            'next_actions': self._suggest_next_actions(ideas, recommendations)
        }
    
    async def _comprehensive_analysis(
        self,
        ideas: List[Dict[str, Any]],
        analytics: Dict[str, Any],
        filters: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate comprehensive analysis combining all insight types"""
        
        trends = await self._analyze_trends(ideas, analytics, filters)
        categories = await self._analyze_categories(ideas, analytics, filters)
        ratings = await self._analyze_ratings(ideas, analytics, filters)
        recommendations = await self._generate_recommendations(ideas, analytics, filters)
        
        # Generate executive summary
        executive_summary = self._generate_executive_summary(
            ideas, trends, categories, ratings, recommendations
        )
        
        return {
            'analysis_type': 'comprehensive',
            'executive_summary': executive_summary,
            'trends': trends,
            'categories': categories,
            'ratings': ratings,
            'recommendations': recommendations,
            'generated_at': datetime.now().isoformat()
        }
    
    async def generate_chart_data(self, user_id: str, chart_type: str) -> Dict[str, Any]:
        """Generate specific chart data for visualization"""
        
        ideas = await self.idea_manager.get_user_ideas(user_id, limit=1000)
        
        if chart_type == "category_pie":
            return self._generate_category_pie_chart(ideas)
        elif chart_type == "rating_bar":
            return self._generate_rating_bar_chart(ideas)
        elif chart_type == "timeline":
            return self._generate_timeline_chart(ideas)
        elif chart_type == "quality_trend":
            return self._generate_quality_trend_chart(ideas)
        elif chart_type == "category_performance":
            return self._generate_category_performance_chart(ideas)
        else:
            raise ValueError(f"Unknown chart type: {chart_type}")
    
    def _create_timeline_analysis(self, ideas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create timeline analysis of idea creation"""
        
        timeline = defaultdict(int)
        
        for idea in ideas:
            # Parse creation date
            created_date = datetime.fromisoformat(idea['created_at'].replace('Z', '+00:00'))
            week_key = created_date.strftime('%Y-W%U')  # Year-Week format
            timeline[week_key] += 1
        
        # Convert to sorted list
        sorted_timeline = sorted(timeline.items())
        
        return {
            'weekly_counts': dict(sorted_timeline),
            'total_weeks': len(sorted_timeline),
            'peak_week': max(timeline.items(), key=lambda x: x[1]) if timeline else None,
            'average_per_week': sum(timeline.values()) / len(timeline) if timeline else 0
        }
    
    def _analyze_category_trends(self, ideas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze how categories have evolved over time"""
        
        category_timeline = defaultdict(lambda: defaultdict(int))
        
        for idea in ideas:
            created_date = datetime.fromisoformat(idea['created_at'].replace('Z', '+00:00'))
            month_key = created_date.strftime('%Y-%m')
            category_timeline[idea['category']][month_key] += 1
        
        return dict(category_timeline)
    
    def _analyze_themes(self, ideas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze common themes and keywords in ideas"""
        
        # Simple keyword extraction from titles and descriptions
        all_text = []
        for idea in ideas:
            all_text.append(idea['title'].lower())
            if idea['description']:
                all_text.append(idea['description'].lower())
        
        # Count common words (simple approach)
        words = []
        for text in all_text:
            # Simple word extraction (could be enhanced with NLP)
            text_words = [word.strip('.,!?()[]{}') for word in text.split()]
            words.extend([word for word in text_words if len(word) > 3])
        
        # Filter out common stop words
        stop_words = {'this', 'that', 'with', 'have', 'will', 'from', 'they', 'been', 'were', 'said', 'each', 'which', 'their', 'time', 'about'}
        filtered_words = [word for word in words if word not in stop_words]
        
        word_counts = Counter(filtered_words)
        
        return {
            'top_keywords': dict(word_counts.most_common(10)),
            'total_unique_words': len(word_counts),
            'vocabulary_richness': len(word_counts) / len(words) if words else 0
        }
    
    def _analyze_idea_velocity(self, ideas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the rate of idea generation over time"""
        
        if not ideas:
            return {'message': 'No ideas to analyze'}
        
        # Sort ideas by creation date
        sorted_ideas = sorted(ideas, key=lambda x: x['created_at'])
        
        first_idea = datetime.fromisoformat(sorted_ideas[0]['created_at'].replace('Z', '+00:00'))
        last_idea = datetime.fromisoformat(sorted_ideas[-1]['created_at'].replace('Z', '+00:00'))
        
        total_days = (last_idea - first_idea).days + 1
        total_weeks = total_days / 7
        total_months = total_days / 30
        
        return {
            'total_days': total_days,
            'ideas_per_day': len(ideas) / total_days if total_days > 0 else len(ideas),
            'ideas_per_week': len(ideas) / total_weeks if total_weeks > 0 else len(ideas),
            'ideas_per_month': len(ideas) / total_months if total_months > 0 else len(ideas),
            'first_idea_date': first_idea.isoformat(),
            'last_idea_date': last_idea.isoformat()
        }
    
    def _generate_category_pie_chart(self, ideas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate pie chart data for category distribution"""
        
        category_counts = Counter(idea['category'] for idea in ideas)
        
        return {
            'chart_type': 'pie',
            'title': 'Ideas by Category',
            'data': [
                {'label': category, 'value': count, 'percentage': round(count/len(ideas)*100, 1)}
                for category, count in category_counts.most_common()
            ]
        }
    
    def _generate_rating_bar_chart(self, ideas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate bar chart data for rating distribution"""
        
        rated_ideas = [idea for idea in ideas if idea['rating']]
        rating_counts = Counter(idea['rating'] for idea in rated_ideas)
        
        return {
            'chart_type': 'bar',
            'title': 'Rating Distribution',
            'data': [
                {'label': f'{rating} stars', 'value': count}
                for rating in range(1, 6)
                for count in [rating_counts.get(rating, 0)]
            ]
        }
    
    def _generate_timeline_chart(self, ideas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate timeline chart data"""
        
        timeline = self._create_timeline_analysis(ideas)
        
        return {
            'chart_type': 'line',
            'title': 'Ideas Created Over Time',
            'data': [
                {'label': week, 'value': count}
                for week, count in timeline['weekly_counts'].items()
            ]
        }
    
    def _generate_trend_insights(self, timeline, category_trends, rating_trends, velocity) -> List[str]:
        """Generate textual insights from trend analysis"""
        
        insights = []
        
        # Velocity insights
        if velocity.get('ideas_per_week', 0) > 2:
            insights.append("🚀 You're highly productive with 2+ ideas per week!")
        elif velocity.get('ideas_per_week', 0) > 1:
            insights.append("📈 Good momentum with 1+ ideas per week")
        else:
            insights.append("💡 Consider setting a goal of 1-2 ideas per week")
        
        # Timeline insights
        if timeline.get('peak_week'):
            peak_week, peak_count = timeline['peak_week']
            insights.append(f"🏆 Your most productive week was {peak_week} with {peak_count} ideas")
        
        return insights
    
    def _generate_category_insights(self, distribution, performance, growth) -> List[str]:
        """Generate insights from category analysis"""
        
        insights = []
        
        # Most popular category
        if distribution:
            top_category = max(distribution.items(), key=lambda x: x[1])
            insights.append(f"🎯 Your focus area is '{top_category[0]}' with {top_category[1]} ideas")
        
        # Best performing category
        if performance:
            best_category = max(performance.items(), key=lambda x: x[1]['avg_rating'])
            insights.append(f"⭐ '{best_category[0]}' has your highest average rating: {best_category[1]['avg_rating']}")
        
        # Diversification
        if len(distribution) < 3:
            insights.append("🌟 Consider exploring new categories to diversify your innovation")
        
        return insights
    
    def _generate_rating_insights(self, distribution, avg_rating, category_ratings, improvement) -> List[str]:
        """Generate insights from rating analysis"""
        
        insights = []
        
        # Overall quality
        if avg_rating >= 4:
            insights.append("🌟 Excellent! Your ideas average 4+ stars")
        elif avg_rating >= 3:
            insights.append("👍 Good quality ideas with room for improvement")
        else:
            insights.append("💡 Focus on quality - consider refining your ideation process")
        
        # Best category
        if category_ratings:
            best_category = max(category_ratings.items(), key=lambda x: x[1])
            insights.append(f"🏆 '{best_category[0]}' is your strongest category ({best_category[1]} avg)")
        
        return insights
    
    def _generate_personalized_insights(self, ideas, analytics) -> List[str]:
        """Generate personalized insights based on user patterns"""
        
        insights = []
        
        total_ideas = len(ideas)
        
        if total_ideas == 0:
            insights.append("🌱 Start your innovation journey by saving your first idea!")
        elif total_ideas < 5:
            insights.append("🚀 You're building momentum! Try to reach 10 ideas for better insights.")
        elif total_ideas < 20:
            insights.append("📈 Great progress! You're developing a solid idea collection.")
        else:
            insights.append("🎯 Impressive collection! You're a prolific innovator.")
        
        return insights
    
    def _suggest_next_actions(self, ideas, recommendations) -> List[str]:
        """Suggest specific next actions for the user"""
        
        actions = []
        
        # Extract high-priority recommendations
        high_priority = [rec for rec in recommendations if rec.get('priority') == 'high']
        
        for rec in high_priority[:3]:  # Top 3 high-priority actions
            actions.append(rec['action'])
        
        # Add general actions if needed
        if len(actions) < 3:
            if len(ideas) < 10:
                actions.append("Generate 2-3 new ideas this week")
            actions.append("Explore a new category or domain")
            actions.append("Review and refine your top-rated ideas")
        
        return actions[:3]  # Return max 3 actions
    
    def _generate_executive_summary(self, ideas, trends, categories, ratings, recommendations) -> Dict[str, Any]:
        """Generate an executive summary of all analyses"""
        
        total_ideas = len(ideas)
        rated_ideas = len([idea for idea in ideas if idea['rating']])
        avg_rating = ratings.get('average_rating', 0)
        top_category = max(categories['distribution'].items(), key=lambda x: x[1])[0] if categories['distribution'] else 'None'
        
        return {
            'overview': {
                'total_ideas': total_ideas,
                'rated_ideas': rated_ideas,
                'average_rating': avg_rating,
                'top_category': top_category,
                'categories_explored': len(categories['distribution'])
            },
            'key_insights': [
                f"You have {total_ideas} ideas with {rated_ideas} rated",
                f"Your focus area is '{top_category}'",
                f"Average idea quality: {avg_rating}/5 stars",
                f"You've explored {len(categories['distribution'])} different categories"
            ],
            'status': self._determine_user_status(total_ideas, avg_rating, len(categories['distribution'])),
            'priority_actions': [rec['action'] for rec in recommendations['recommendations'][:2]]
        }
    
    def _determine_user_status(self, total_ideas, avg_rating, categories_count) -> str:
        """Determine user's innovation status"""
        
        if total_ideas >= 20 and avg_rating >= 4 and categories_count >= 4:
            return "Innovation Expert"
        elif total_ideas >= 10 and avg_rating >= 3.5:
            return "Active Innovator"
        elif total_ideas >= 5:
            return "Emerging Innovator"
        else:
            return "Getting Started" 