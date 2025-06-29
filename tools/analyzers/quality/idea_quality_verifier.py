#!/usr/bin/env python3
"""
IDEA QUALITY VERIFIER
Deep analysis and validation of business ideas from discovery intelligence
Verifies market potential, competition, feasibility, and revenue potential
"""

import json
import sys
import re
from datetime import datetime
from collections import defaultdict

class IdeaQualityVerifier:
    """Comprehensive business idea quality verification system"""
    
    def __init__(self):
        self.quality_criteria = {
            'market_size': {
                'weight': 0.25,
                'indicators': {
                    'large': ['billion', 'million users', 'enterprise', 'saas', 'b2b'],
                    'medium': ['thousand', 'small business', 'niche', 'specialized'],
                    'small': ['personal', 'hobby', 'side project']
                }
            },
            'revenue_potential': {
                'weight': 0.25,
                'indicators': {
                    'high': ['arr', 'mrr', 'subscription', 'recurring', 'enterprise', 'b2b'],
                    'medium': ['one-time', 'service', 'consulting', 'freelance'],
                    'low': ['free', 'ad-supported', 'donation']
                }
            },
            'technical_feasibility': {
                'weight': 0.20,
                'indicators': {
                    'easy': ['api', 'wrapper', 'dashboard', 'simple tool', 'automation'],
                    'medium': ['platform', 'app', 'integration', 'ai tool'],
                    'hard': ['infrastructure', 'hardware', 'complex ai', 'blockchain']
                }
            },
            'market_validation': {
                'weight': 0.15,
                'indicators': {
                    'validated': ['show hn', 'launched', 'users', 'customers', 'revenue'],
                    'partial': ['prototype', 'beta', 'testing', 'feedback'],
                    'unvalidated': ['idea', 'concept', 'planning']
                }
            },
            'competition': {
                'weight': 0.10,
                'indicators': {
                    'low': ['alternative', 'open source', 'new approach', 'niche'],
                    'medium': ['better', 'faster', 'cheaper', 'simpler'],
                    'high': ['dominated', 'saturated', 'giants']
                }
            },
            'time_to_market': {
                'weight': 0.05,
                'indicators': {
                    'fast': ['mvp', 'simple', 'api', 'tool', 'automation'],
                    'medium': ['app', 'platform', 'service'],
                    'slow': ['infrastructure', 'complex', 'enterprise']
                }
            }
        }
    
    def verify_idea_quality(self, opportunities_file):
        """Verify the quality of discovered business ideas"""
        
        print("🔍 IDEA QUALITY VERIFIER")
        print("=" * 60)
        print("🎯 Deep analysis of business idea quality and potential")
        print("📊 Analyzing market size, revenue potential, feasibility")
        print()
        
        # Load opportunities
        try:
            with open(opportunities_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return
        
        opportunities = data.get('business_opportunities', [])
        
        if not opportunities:
            print("❌ No business opportunities found in file!")
            return
        
        print(f"📊 Analyzing {len(opportunities)} business opportunities...")
        print()
        
        verified_ideas = []
        
        for i, opp in enumerate(opportunities, 1):
            print(f"🔍 ANALYZING IDEA #{i}")
            print("=" * 40)
            
            title = opp.get('title', '')
            url = opp.get('url', '')
            source = opp.get('source', '')
            business_score = opp.get('business_score', 0)
            
            print(f"💡 IDEA: {title[:80]}...")
            print(f"🌐 SOURCE: {source}")
            print(f"📊 INITIAL SCORE: {business_score}")
            print()
            
            # Analyze each quality criterion
            quality_scores = {}
            analysis_details = {}
            
            for criterion, config in self.quality_criteria.items():
                score, details = self._analyze_criterion(title, criterion, config)
                quality_scores[criterion] = score
                analysis_details[criterion] = details
                
                print(f"   📈 {criterion.replace('_', ' ').title()}: {score:.1f}/10 - {details}")
            
            # Calculate weighted quality score
            weighted_score = sum(
                quality_scores[criterion] * config['weight'] 
                for criterion, config in self.quality_criteria.items()
            )
            
            # Additional analysis based on source credibility
            source_multiplier = self._get_source_credibility_multiplier(source)
            final_score = weighted_score * source_multiplier
            
            # Determine idea grade
            grade = self._get_idea_grade(final_score)
            
            print(f"\n   🎯 WEIGHTED QUALITY SCORE: {weighted_score:.1f}/10")
            print(f"   ⭐ SOURCE CREDIBILITY MULTIPLIER: {source_multiplier:.1f}x")
            print(f"   🏆 FINAL SCORE: {final_score:.1f}/10")
            print(f"   📊 GRADE: {grade}")
            
            # Specific recommendations
            recommendations = self._generate_recommendations(title, quality_scores, source)
            print(f"\n   💡 RECOMMENDATIONS:")
            for rec in recommendations:
                print(f"      • {rec}")
            
            verified_ideas.append({
                'rank': i,
                'title': title,
                'url': url,
                'source': source,
                'original_score': business_score,
                'quality_scores': quality_scores,
                'weighted_score': weighted_score,
                'source_multiplier': source_multiplier,
                'final_score': final_score,
                'grade': grade,
                'recommendations': recommendations,
                'analysis_details': analysis_details
            })
            
            print("\n" + "="*60 + "\n")
        
        # Overall analysis and ranking
        print("🏆 OVERALL IDEA QUALITY ANALYSIS")
        print("=" * 50)
        
        # Sort by final score
        verified_ideas.sort(key=lambda x: x['final_score'], reverse=True)
        
        print("🥇 TOP-RANKED IDEAS:")
        for i, idea in enumerate(verified_ideas[:5], 1):
            grade = idea['grade']
            score = idea['final_score']
            title = idea['title'][:50]
            print(f"   #{i} {title}... (Grade: {grade}, Score: {score:.1f})")
        
        # Grade distribution
        grade_distribution = defaultdict(int)
        for idea in verified_ideas:
            grade_distribution[idea['grade']] += 1
        
        print(f"\n📊 GRADE DISTRIBUTION:")
        for grade in ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F']:
            count = grade_distribution.get(grade, 0)
            if count > 0:
                percentage = (count / len(verified_ideas)) * 100
                print(f"   {grade}: {count} ideas ({percentage:.1f}%)")
        
        # Category analysis
        print(f"\n🎯 CATEGORY ANALYSIS:")
        categories = self._categorize_ideas(verified_ideas)
        for category, ideas in categories.items():
            avg_score = sum(idea['final_score'] for idea in ideas) / len(ideas)
            print(f"   📈 {category}: {len(ideas)} ideas (Avg: {avg_score:.1f})")
        
        # Investment recommendations
        print(f"\n💰 INVESTMENT RECOMMENDATIONS:")
        
        excellent_ideas = [idea for idea in verified_ideas if idea['final_score'] >= 8.0]
        good_ideas = [idea for idea in verified_ideas if 6.0 <= idea['final_score'] < 8.0]
        risky_ideas = [idea for idea in verified_ideas if idea['final_score'] < 6.0]
        
        print(f"   🚀 IMMEDIATE PURSUIT ({len(excellent_ideas)} ideas):")
        for idea in excellent_ideas[:3]:
            title = idea['title'][:45]
            score = idea['final_score']
            print(f"      ⚡ {title}... (Score: {score:.1f})")
        
        print(f"   🎯 FURTHER RESEARCH ({len(good_ideas)} ideas):")
        for idea in good_ideas[:3]:
            title = idea['title'][:45]
            score = idea['final_score']
            print(f"      🔍 {title}... (Score: {score:.1f})")
        
        print(f"   ⚠️ HIGH RISK ({len(risky_ideas)} ideas):")
        for idea in risky_ideas[:2]:
            title = idea['title'][:45]
            score = idea['final_score']
            print(f"      ❌ {title}... (Score: {score:.1f})")
        
        # Save detailed analysis
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_file = f"idea_quality_verification_{timestamp}.json"
        
        verification_results = {
            'timestamp': timestamp,
            'source_file': opportunities_file,
            'total_ideas_analyzed': len(verified_ideas),
            'verification_criteria': self.quality_criteria,
            'verified_ideas': verified_ideas,
            'grade_distribution': dict(grade_distribution),
            'categories': {cat: len(ideas) for cat, ideas in categories.items()},
            'recommendations': {
                'immediate_pursuit': len(excellent_ideas),
                'further_research': len(good_ideas),
                'high_risk': len(risky_ideas)
            }
        }
        
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(verification_results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n🎉 IDEA QUALITY VERIFICATION COMPLETE!")
        print("=" * 50)
        print(f"📊 {len(verified_ideas)} ideas analyzed and ranked")
        print(f"🏆 {len(excellent_ideas)} excellent ideas for immediate pursuit")
        print(f"🎯 {len(good_ideas)} good ideas for further research")
        print(f"💾 Detailed analysis saved to: {analysis_file}")
        
        return verification_results
    
    def _analyze_criterion(self, title, criterion, config):
        """Analyze a specific quality criterion"""
        title_lower = title.lower()
        
        # Check indicators for each level
        for level in ['high', 'large', 'easy', 'validated', 'low', 'fast']:
            if level in config['indicators']:
                for indicator in config['indicators'][level]:
                    if indicator in title_lower:
                        if level in ['high', 'large', 'easy', 'validated', 'low', 'fast']:
                            return 8.5, f"Strong {level} indicator: '{indicator}'"
        
        for level in ['medium', 'partial']:
            if level in config['indicators']:
                for indicator in config['indicators'][level]:
                    if indicator in title_lower:
                        return 6.0, f"Medium indicator: '{indicator}'"
        
        for level in ['small', 'low', 'hard', 'unvalidated', 'high', 'slow']:
            if level in config['indicators']:
                for indicator in config['indicators'][level]:
                    if indicator in title_lower:
                        if level in ['small', 'hard', 'unvalidated', 'high', 'slow']:
                            return 3.5, f"Challenging {level} indicator: '{indicator}'"
        
        # Default score if no indicators found
        return 5.0, "No clear indicators found"
    
    def _get_source_credibility_multiplier(self, source):
        """Get credibility multiplier based on source"""
        multipliers = {
            'ycombinator_show': 1.3,  # Highest credibility
            'hacker_news': 1.2,
            'indie_hackers': 1.2,
            'github_trending': 1.1,
            'reddit_entrepreneur': 1.0,
            'launching_next': 0.9,
            'maker_log': 0.9,
            'dev_to': 0.8,
            'medium_startup': 0.8
        }
        return multipliers.get(source, 1.0)
    
    def _get_idea_grade(self, score):
        """Convert score to letter grade"""
        if score >= 9.0:
            return 'A+'
        elif score >= 8.5:
            return 'A'
        elif score >= 8.0:
            return 'B+'
        elif score >= 7.0:
            return 'B'
        elif score >= 6.0:
            return 'C+'
        elif score >= 5.0:
            return 'C'
        elif score >= 4.0:
            return 'D'
        else:
            return 'F'
    
    def _generate_recommendations(self, title, quality_scores, source):
        """Generate specific recommendations for idea improvement"""
        recommendations = []
        
        # Market size recommendations
        if quality_scores['market_size'] < 6.0:
            recommendations.append("Research market size - consider enterprise/B2B angle")
        
        # Revenue potential recommendations
        if quality_scores['revenue_potential'] < 6.0:
            recommendations.append("Explore subscription/recurring revenue models")
        
        # Technical feasibility recommendations
        if quality_scores['technical_feasibility'] < 6.0:
            recommendations.append("Start with MVP - focus on core functionality first")
        
        # Market validation recommendations
        if quality_scores['market_validation'] < 6.0:
            recommendations.append("Validate with potential customers before building")
        
        # Source-specific recommendations
        if source in ['ycombinator_show', 'hacker_news']:
            recommendations.append("High-quality source - consider immediate prototyping")
        elif source in ['reddit_entrepreneur']:
            recommendations.append("Community-validated - gather more user feedback")
        
        # Title-specific recommendations
        title_lower = title.lower()
        if 'show hn' in title_lower:
            recommendations.append("Already launched - analyze user feedback and traction")
        if 'arr' in title_lower or 'revenue' in title_lower:
            recommendations.append("Proven revenue model - study their approach")
        if 'open source' in title_lower:
            recommendations.append("Consider commercial/enterprise version")
        
        return recommendations[:4]  # Limit to top 4 recommendations
    
    def _categorize_ideas(self, verified_ideas):
        """Categorize ideas by type"""
        categories = defaultdict(list)
        
        for idea in verified_ideas:
            title = idea['title'].lower()
            
            if any(word in title for word in ['api', 'tool', 'developer', 'framework']):
                categories['Developer Tools'].append(idea)
            elif any(word in title for word in ['design', 'ui', 'color', 'palette']):
                categories['Design Tools'].append(idea)
            elif any(word in title for word in ['arr', 'revenue', 'business', 'startup']):
                categories['Business/Revenue'].append(idea)
            elif any(word in title for word in ['ai', 'llm', 'machine learning']):
                categories['AI/ML Tools'].append(idea)
            elif any(word in title for word in ['open source', 'alternative']):
                categories['Open Source'].append(idea)
            else:
                categories['Other'].append(idea)
        
        return categories

def main():
    """Run the idea quality verifier"""
    if len(sys.argv) < 2:
        print("Usage: python idea_quality_verifier.py <opportunities_file.json>")
        return
    
    verifier = IdeaQualityVerifier()
    verifier.verify_idea_quality(sys.argv[1])

if __name__ == "__main__":
    main() 