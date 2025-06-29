#!/usr/bin/env python3
"""
Business Problem Analyzer for Luciq
Extracts and analyzes actual business problems from Reddit posts instead of just keywords
"""

import json
import re
from datetime import datetime
from collections import defaultdict

def load_pain_points_database():
    """Load the pain points database"""
    try:
        with open("luciq/memory/pain-points-database.json", 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading pain points database: {e}")
        return {}

def extract_business_problems(post_text, title):
    """Extract actual business problems from post content"""
    problems = []
    
    # Combine title and text for analysis
    full_text = f"{title}. {post_text}"
    
    # More comprehensive problem extraction
    # 1. Extract complete sentences that contain problem indicators
    sentences = re.split(r'[.!?]+', full_text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 20 or len(sentence) > 300:  # Skip too short/long sentences
            continue
            
        sentence_lower = sentence.lower()
        
        # Check if sentence contains problem indicators
        problem_indicators = [
            'problem', 'issue', 'challenge', 'struggle', 'difficulty', 'pain', 'frustration',
            'bottleneck', 'obstacle', 'hard to', 'difficult to', 'impossible to',
            'can\'t', 'cannot', 'unable to', 'failing to', 'struggling with',
            'having trouble', 'finding it hard', 'wasting money', 'wasting time',
            'takes too long', 'time-consuming', 'manually', 'tedious',
            'no good solution', 'lack of', 'missing', 'need help', 'how do i',
            'any advice', 'looking for help', 'not sure how', 'don\'t know how'
        ]
        
        if any(indicator in sentence_lower for indicator in problem_indicators):
            # Clean and add the problem
            cleaned_problem = clean_problem_sentence(sentence)
            if cleaned_problem and len(cleaned_problem) > 15:
                problems.append(cleaned_problem)
    
    # 2. Also extract specific problem patterns (more targeted)
    problem_patterns = [
        # Direct statements
        r"(?:the (?:main |biggest |real )?(?:problem|issue|challenge) (?:is|with|here))\s+([^.!?]{10,150})",
        r"(?:my (?:main |biggest )?(?:concern|problem|issue) is)\s+([^.!?]{10,150})",
        
        # Capability gaps
        r"(?:i (?:can't|cannot|don't know how to|am not sure how to|struggle to))\s+([^.!?]{10,150})",
        r"(?:it's (?:hard|difficult|impossible|challenging) to)\s+([^.!?]{10,150})",
        
        # Resource waste
        r"(?:(?:wasting|spending too much|losing) (?:money|time|resources) on)\s+([^.!?]{10,150})",
        
        # Process inefficiencies
        r"(?:takes (?:too long|forever) to)\s+([^.!?]{10,150})",
        r"(?:manually (?:doing|handling|managing))\s+([^.!?]{10,150})",
        
        # Solution gaps
        r"(?:no (?:good )?(?:solution|tool|way) (?:for|to))\s+([^.!?]{10,150})",
        r"(?:lacking|missing) (?:a |the )?([^.!?]{10,150})",
        
        # Help seeking
        r"(?:need help (?:with|finding))\s+([^.!?]{10,150})",
        r"(?:how (?:do i|can i|should i))\s+([^.!?]{10,150})",
        r"(?:any advice on)\s+([^.!?]{10,150})"
    ]
    
    for pattern in problem_patterns:
        matches = re.finditer(pattern, full_text, re.IGNORECASE)
        for match in matches:
            problem_text = match.group(1).strip()
            cleaned_problem = clean_problem_text(problem_text)
            if cleaned_problem and len(cleaned_problem) > 10:
                problems.append(cleaned_problem)
    
    return list(set(problems))  # Remove duplicates

def clean_problem_sentence(sentence):
    """Clean a full sentence that represents a problem"""
    # Remove extra whitespace
    sentence = re.sub(r'\s+', ' ', sentence).strip()
    
    # Remove common prefixes that don't add value
    prefixes_to_remove = [
        r'^(?:but |and |so |also |however |though |although |while )',
        r'^(?:i think |i believe |i feel |in my opinion )',
        r'^(?:the thing is |the problem is |the issue is )'
    ]
    
    for prefix in prefixes_to_remove:
        sentence = re.sub(prefix, '', sentence, flags=re.IGNORECASE).strip()
    
    # Capitalize first letter
    if sentence:
        sentence = sentence[0].upper() + sentence[1:]
    
    return sentence

def clean_problem_text(text):
    """Clean and normalize problem text"""
    # Remove common filler words and clean up
    text = re.sub(r'\b(?:the|a|an|and|or|but|in|on|at|to|for|of|with|by)\b', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Capitalize first letter
    if text:
        text = text[0].upper() + text[1:]
    
    return text

def categorize_business_problem(problem_text):
    """Categorize business problems into domains"""
    problem_lower = problem_text.lower()
    
    # Marketing & Sales
    if any(word in problem_lower for word in ['marketing', 'ads', 'advertising', 'leads', 'customers', 'sales', 'conversion', 'traffic', 'seo', 'social media']):
        return 'marketing_sales'
    
    # Operations & Productivity
    elif any(word in problem_lower for word in ['productivity', 'workflow', 'process', 'automation', 'efficiency', 'time management', 'organization']):
        return 'operations_productivity'
    
    # Finance & Accounting
    elif any(word in problem_lower for word in ['money', 'finance', 'accounting', 'invoicing', 'payment', 'revenue', 'expenses', 'budget']):
        return 'finance_accounting'
    
    # Customer Service
    elif any(word in problem_lower for word in ['customer service', 'support', 'tickets', 'complaints', 'feedback', 'communication']):
        return 'customer_service'
    
    # Technology & Development
    elif any(word in problem_lower for word in ['development', 'coding', 'technical', 'software', 'app', 'website', 'platform', 'integration']):
        return 'technology_development'
    
    # HR & Team Management
    elif any(word in problem_lower for word in ['team', 'employees', 'hiring', 'management', 'collaboration', 'remote work']):
        return 'hr_team_management'
    
    else:
        return 'general_business'

def analyze_business_problems():
    """Analyze actual business problems from the database"""
    print("[ANALYSIS] REAL BUSINESS PROBLEMS ANALYSIS")
    print("=" * 60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    data = load_pain_points_database()
    if not data or 'pain_points' not in data:
        print("No pain points data available.")
        return
    
    all_problems = []
    problem_frequency = defaultdict(int)
    problem_categories = defaultdict(list)
    subreddit_problems = defaultdict(list)
    
    # Extract problems from each post
    for post in data['pain_points']:
        title = post.get('title', '')
        content = post.get('selftext', '')
        subreddit = post.get('subreddit', 'unknown')
        business_potential = post.get('business_potential', 'low')
        post_age = post.get('post_age_days', 0)
        
        problems = extract_business_problems(content, title)
        
        for problem in problems:
            problem_info = {
                'problem': problem,
                'subreddit': subreddit,
                'business_potential': business_potential,
                'post_age_days': post_age,
                'category': categorize_business_problem(problem),
                'source_title': title
            }
            
            all_problems.append(problem_info)
            problem_frequency[problem] += 1
            problem_categories[categorize_business_problem(problem)].append(problem)
            subreddit_problems[subreddit].append(problem)
    
    print(f"[DATA] EXTRACTED {len(all_problems)} REAL BUSINESS PROBLEMS")
    print(f"[DATA] FROM {len(data['pain_points'])} POSTS ANALYZED")
    print()
    
    # Top recurring problems
    print("[TOP] TOP RECURRING BUSINESS PROBLEMS")
    print("-" * 45)
    sorted_problems = sorted(problem_frequency.items(), key=lambda x: x[1], reverse=True)
    
    for i, (problem, count) in enumerate(sorted_problems[:10], 1):
        if count > 1:  # Only show problems that appear multiple times
            print(f"{i}. \"{problem}\" - {count} occurrences")
            
            # Show which subreddits this appears in
            subreddits = set()
            for p in all_problems:
                if p['problem'] == problem:
                    subreddits.add(p['subreddit'])
            print(f"   Communities: {', '.join(subreddits)}")
            
            # Show business potential
            high_potential_count = sum(1 for p in all_problems if p['problem'] == problem and p['business_potential'] == 'high')
            print(f"   High Business Potential: {high_potential_count}/{count} cases")
            print()
    
    print()
    
    # Problems by category
    print("[CATEGORY] PROBLEMS BY BUSINESS CATEGORY")
    print("-" * 40)
    for category, problems in problem_categories.items():
        unique_problems = len(set(problems))
        total_problems = len(problems)
        print(f"{category.replace('_', ' ').title()}: {unique_problems} unique problems ({total_problems} total)")
        
        # Show top problems in this category
        category_freq = defaultdict(int)
        for problem in problems:
            category_freq[problem] += 1
        
        top_category_problems = sorted(category_freq.items(), key=lambda x: x[1], reverse=True)[:3]
        for problem, count in top_category_problems:
            if count > 1:
                print(f"  * \"{problem}\" ({count}x)")
        print()
    
    # High business potential problems
    print("[POTENTIAL] HIGH BUSINESS POTENTIAL PROBLEMS")
    print("-" * 40)
    high_potential_problems = [p for p in all_problems if p['business_potential'] == 'high']
    
    if high_potential_problems:
        # Group by problem text
        high_potential_freq = defaultdict(int)
        for p in high_potential_problems:
            high_potential_freq[p['problem']] += 1
        
        sorted_high_potential = sorted(high_potential_freq.items(), key=lambda x: x[1], reverse=True)
        
        for i, (problem, count) in enumerate(sorted_high_potential[:5], 1):
            print(f"{i}. \"{problem}\" - {count} high-potential occurrences")
            
            # Show source posts
            sources = [p['source_title'] for p in high_potential_problems if p['problem'] == problem]
            print(f"   From posts: {', '.join(set(sources[:2]))}...")
            print()
    else:
        print("No high business potential problems identified yet.")
    
    print()
    print("[INSIGHTS] ACTIONABLE INSIGHTS")
    print("-" * 25)
    
    if sorted_problems:
        most_common = sorted_problems[0]
        print(f"* Most common problem: \"{most_common[0]}\" ({most_common[1]} occurrences)")
    
    if high_potential_problems:
        print(f"* {len(high_potential_problems)} problems marked as high business potential")
        
        # Most validated high-potential problem
        if sorted_high_potential:
            top_validated = sorted_high_potential[0]
            print(f"* Most validated opportunity: \"{top_validated[0]}\" ({top_validated[1]} validations)")
    
    # Category with most problems
    if problem_categories:
        top_category = max(problem_categories.items(), key=lambda x: len(x[1]))
        print(f"* Biggest problem area: {top_category[0].replace('_', ' ').title()} ({len(top_category[1])} problems)")

if __name__ == "__main__":
    analyze_business_problems() 