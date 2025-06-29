#!/usr/bin/env python3
"""
Business Idea Generation Blitz
Rapid-fire scraping of multiple subreddits to generate tons of real SaaS ideas
"""

import sys
import os
sys.path.append('src')

import asyncio
import json
from datetime import datetime
from collections import defaultdict

from api.domains.discovery.services.discovery_service import DiscoveryService

async def idea_generation_blitz():
    """Generate a shitload of business ideas by hitting multiple subreddits rapidly"""
    
    print("🚀 BUSINESS IDEA GENERATION BLITZ")
    print("=" * 60)
    print("🎯 MISSION: Generate maximum business ideas in minimum time!")
    
    # Target subreddits for rapid idea generation
    target_subreddits = [
        'entrepreneur',      # Main entrepreneurship discussions
        'startups',         # Startup-specific problems  
        'smallbusiness',    # Small business pain points
        'freelance',        # Freelancer problems
        'SaaS',            # SaaS business challenges
        'business',        # General business issues
        'marketing',       # Marketing pain points
        'webdev',          # Developer problems
        'productivity',    # Productivity challenges
        'indiehackers',    # Indie hacker challenges
        'Entrepreneur',    # Alternative entrepreneur sub
        'sales',           # Sales challenges
        'ecommerce',       # E-commerce problems
        'consulting',      # Consulting pain points
        'remotework'       # Remote work issues
    ]
    
    # Initialize discovery service
    service = DiscoveryService()
    
    # Storage for all results
    all_pain_points = []
    all_opportunities = []
    all_concepts = []
    business_ideas = []
    subreddit_stats = {}
    
    print(f"🎯 Target Subreddits: {len(target_subreddits)}")
    print(f"📊 Posts per subreddit: 5 (for speed)")
    print(f"🔍 Total posts to analyze: {len(target_subreddits) * 5}")
    print(f"⚡ Rapid-fire mode: Minimal delays")
    print("\n" + "="*60)
    
    start_time = datetime.now()
    
    # Rapid-fire scraping
    for i, subreddit in enumerate(target_subreddits, 1):
        print(f"\n🔥 [{i}/{len(target_subreddits)}] BLITZING r/{subreddit}")
        print("-" * 40)
        
        try:
            # Run discovery on this subreddit (reduced posts for speed)
            result = await service.discover_pain_points(
                subreddit=subreddit,
                limit=5  # Reduced for speed
            )
            
            # Extract results
            posts_analyzed = result.get('posts_analyzed', 0)
            pain_points = result.get('pain_points', [])
            opportunities = result.get('ranked_opportunities', [])
            concepts = result.get('concepts', [])
            
            # Store stats
            subreddit_stats[subreddit] = {
                'posts_analyzed': posts_analyzed,
                'pain_points_found': len(pain_points),
                'opportunities_generated': len(opportunities),
                'concepts_generated': len(concepts)
            }
            
            # Process pain points into business ideas
            for pain_point in pain_points:
                title = pain_point.get('title', 'Unknown')
                
                # Generate specific business idea from pain point
                business_idea = generate_business_idea_from_pain_point(pain_point, subreddit)
                if business_idea:
                    business_ideas.append(business_idea)
                
                pain_point['source_subreddit'] = subreddit
                all_pain_points.append(pain_point)
            
            # Process opportunities
            for opportunity in opportunities:
                # Extract specific business idea from opportunity title
                opp_title = opportunity.get('title', '')
                if 'SaaS Solution for:' in opp_title:
                    problem = opp_title.replace('SaaS Solution for:', '').strip()
                    business_idea = {
                        'idea_title': f"Solution for: {problem[:50]}...",
                        'problem_statement': problem,
                        'business_model': 'SaaS',
                        'target_market': opportunity.get('domain', 'General'),
                        'revenue_potential': opportunity.get('business_potential', 'Medium'),
                        'source_subreddit': subreddit,
                        'confidence_score': opportunity.get('score', 0),
                        'discovery_method': 'opportunity_extraction'
                    }
                    business_ideas.append(business_idea)
                
                opportunity['source_subreddit'] = subreddit
                all_opportunities.append(opportunity)
            
            # Add concepts
            for concept in concepts:
                concept['source_subreddit'] = subreddit
                all_concepts.append(concept)
            
            # Show immediate results
            print(f"   📊 Posts: {posts_analyzed}")
            print(f"   ⚠️ Pain Points: {len(pain_points)}")
            print(f"   🌟 Opportunities: {len(opportunities)}")
            print(f"   💡 Business Ideas Generated: {len([p for p in pain_points]) + len([o for o in opportunities])}")
            
            # Show top business idea from this subreddit
            subreddit_ideas = [idea for idea in business_ideas if idea.get('source_subreddit') == subreddit]
            if subreddit_ideas:
                top_idea = subreddit_ideas[-1]  # Latest idea
                print(f"   🏆 Latest Idea: {top_idea.get('idea_title', 'Unknown')[:50]}...")
            
            # Minimal delay for rapid-fire mode
            await asyncio.sleep(0.5)  # Very short delay
            
        except Exception as e:
            print(f"   ❌ Error scraping r/{subreddit}: {str(e)}")
            subreddit_stats[subreddit] = {
                'posts_analyzed': 0,
                'pain_points_found': 0,
                'opportunities_generated': 0,
                'concepts_generated': 0,
                'error': str(e)
            }
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Comprehensive analysis
    print(f"\n🎉 IDEA GENERATION BLITZ COMPLETE!")
    print("=" * 60)
    
    # Overall stats
    total_posts = sum(stats['posts_analyzed'] for stats in subreddit_stats.values())
    total_pain_points = len(all_pain_points)
    total_opportunities = len(all_opportunities)
    total_business_ideas = len(business_ideas)
    
    print(f"📊 BLITZ STATISTICS:")
    print(f"   ⏱️ Total Duration: {duration:.1f} seconds")
    print(f"   📝 Total Posts Analyzed: {total_posts}")
    print(f"   ⚠️ Total Pain Points Found: {total_pain_points}")
    print(f"   🌟 Total Opportunities Generated: {total_opportunities}")
    print(f"   💡 Total Business Ideas: {total_business_ideas}")
    print(f"   🚀 Ideas per Second: {total_business_ideas/duration:.1f}")
    print(f"   📈 Success Rate: {(total_business_ideas/total_posts*100):.1f}% (ideas per post)")
    
    # Show all business ideas
    print(f"\n💡 ALL BUSINESS IDEAS GENERATED:")
    print("=" * 60)
    
    for i, idea in enumerate(business_ideas, 1):
        print(f"\n#{i} 🚀 {idea.get('idea_title', 'Untitled Idea')}")
        print(f"   📝 Problem: {idea.get('problem_statement', 'Unknown')[:80]}...")
        print(f"   🏭 Target Market: {idea.get('target_market', 'Unknown')}")
        print(f"   💰 Revenue Model: {idea.get('business_model', 'Unknown')}")
        print(f"   📊 Confidence: {idea.get('confidence_score', 0)}/10")
        print(f"   📍 Source: r/{idea.get('source_subreddit', 'unknown')}")
        print(f"   🔍 Method: {idea.get('discovery_method', 'unknown')}")
    
    # Business idea categories
    print(f"\n🏷️ BUSINESS IDEA CATEGORIES:")
    categories = defaultdict(int)
    for idea in business_ideas:
        category = idea.get('target_market', 'Unknown')
        categories[category] += 1
    
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"   🎯 {category}: {count} ideas")
    
    # Top performing subreddits
    print(f"\n🏆 TOP PERFORMING SUBREDDITS:")
    sorted_subreddits = sorted(
        subreddit_stats.items(), 
        key=lambda x: x[1]['pain_points_found'] + x[1]['opportunities_generated'], 
        reverse=True
    )
    
    for i, (subreddit, stats) in enumerate(sorted_subreddits[:10], 1):
        if 'error' not in stats:
            total_ideas = stats['pain_points_found'] + stats['opportunities_generated']
            print(f"   #{i} r/{subreddit}: {total_ideas} ideas from {stats['posts_analyzed']} posts")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"business_ideas_blitz_{timestamp}.json"
    
    blitz_results = {
        'timestamp': timestamp,
        'duration_seconds': duration,
        'subreddits_analyzed': target_subreddits,
        'total_stats': {
            'posts_analyzed': total_posts,
            'pain_points_found': total_pain_points,
            'opportunities_generated': total_opportunities,
            'business_ideas_generated': total_business_ideas,
            'ideas_per_second': total_business_ideas/duration,
            'success_rate': total_business_ideas/total_posts if total_posts > 0 else 0
        },
        'subreddit_stats': subreddit_stats,
        'business_ideas': business_ideas,
        'pain_points': all_pain_points,
        'opportunities': all_opportunities,
        'idea_categories': dict(categories)
    }
    
    with open(results_file, 'w') as f:
        json.dump(blitz_results, f, indent=2, default=str)
    
    print(f"\n💾 RESULTS SAVED TO: {results_file}")
    print(f"🎯 Business idea generation blitz complete!")
    
    return blitz_results

def generate_business_idea_from_pain_point(pain_point, subreddit):
    """Generate a specific business idea from a pain point"""
    title = pain_point.get('title', '')
    
    # Extract business context
    business_context = pain_point.get('business_context', {})
    industry = business_context.get('industry', 'General')
    
    # Generate business idea based on pain point
    if 'marketing' in title.lower():
        return {
            'idea_title': f"Marketing Solution: {title[:40]}...",
            'problem_statement': title,
            'business_model': 'SaaS',
            'target_market': 'Marketing',
            'revenue_potential': 'Medium',
            'source_subreddit': subreddit,
            'confidence_score': pain_point.get('score', 0),
            'discovery_method': 'pain_point_analysis'
        }
    elif 'freelance' in title.lower() or 'client' in title.lower():
        return {
            'idea_title': f"Freelancer Tool: {title[:40]}...",
            'problem_statement': title,
            'business_model': 'SaaS',
            'target_market': 'Freelancers',
            'revenue_potential': 'Medium',
            'source_subreddit': subreddit,
            'confidence_score': pain_point.get('score', 0),
            'discovery_method': 'pain_point_analysis'
        }
    elif 'startup' in title.lower() or 'business' in title.lower():
        return {
            'idea_title': f"Business Tool: {title[:40]}...",
            'problem_statement': title,
            'business_model': 'SaaS',
            'target_market': 'Startups',
            'revenue_potential': 'Medium',
            'source_subreddit': subreddit,
            'confidence_score': pain_point.get('score', 0),
            'discovery_method': 'pain_point_analysis'
        }
    else:
        return {
            'idea_title': f"Solution: {title[:40]}...",
            'problem_statement': title,
            'business_model': 'SaaS',
            'target_market': industry,
            'revenue_potential': 'Medium',
            'source_subreddit': subreddit,
            'confidence_score': pain_point.get('score', 0),
            'discovery_method': 'pain_point_analysis'
        }

if __name__ == "__main__":
    results = asyncio.run(idea_generation_blitz())
    
    print(f"\n🚀 IDEA GENERATION BLITZ ACCOMPLISHED!")
    print(f"   ⏱️ Duration: {results['duration_seconds']:.1f}s")
    print(f"   💡 Business Ideas: {results['total_stats']['business_ideas_generated']}")
    print(f"   🚀 Ideas/Second: {results['total_stats']['ideas_per_second']:.1f}")
    print(f"   📈 Success Rate: {results['total_stats']['success_rate']:.1%}")
    print(f"   📊 Subreddits: {len(results['subreddits_analyzed'])}") 