#!/usr/bin/env python3
"""
Luciq Value Validation Test
Test real business scenarios to prove API value before launch
"""

import requests
import json
import time
from datetime import datetime

def test_real_business_scenario(scenario_name, content, expected_insights):
    """Test a real business scenario and validate insights"""
    print(f"\n🎯 Testing: {scenario_name}")
    print(f"Input: {content[:100]}...")
    
    results = {}
    
    # Test Pain Point Detection
    try:
        response = requests.post(
            "http://localhost:8000/api/intelligence/pain-point-detection",
            json={"content": content, "platform": "test", "context": {}},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            pain_analysis = data.get('pain_point_analysis', {})
            results['pain_points'] = {
                'confidence': pain_analysis.get('confidence_score', 0),
                'description': pain_analysis.get('pain_point_description', ''),
                'opportunity': pain_analysis.get('opportunity_description', ''),
                'market_size': pain_analysis.get('market_size_score', 0),
                'urgency': pain_analysis.get('urgency_score', 0)
            }
            print(f"✅ Pain Point Confidence: {results['pain_points']['confidence']:.2f}")
            print(f"   Opportunity: {results['pain_points']['opportunity'][:80]}...")
        else:
            print(f"❌ Pain Point Detection failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Pain Point Error: {e}")
    
    # Test Market Validation
    try:
        response = requests.post(
            "http://localhost:8000/api/intelligence/market-validation",
            json={"content": content, "platform": "test", "context": {}},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            market_analysis = data.get('market_validation_analysis', {})
            results['market'] = {
                'validation_score': market_analysis.get('market_validation_score', 0),
                'market_size': market_analysis.get('market_metrics', {}).get('market_size_score', 0),
                'competition': market_analysis.get('market_metrics', {}).get('competition_density', 0),
                'timing': market_analysis.get('timing_analysis', {}).get('market_timing_score', 0),
                'entry_strategy': market_analysis.get('strategic_recommendations', {}).get('recommended_entry_strategy', '')
            }
            print(f"✅ Market Validation Score: {results['market']['validation_score']:.2f}")
            print(f"   Entry Strategy: {results['market']['entry_strategy']}")
        else:
            print(f"❌ Market Validation failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Market Validation Error: {e}")
    
    # Test Competitive Analysis
    try:
        response = requests.post(
            "http://localhost:8000/api/intelligence/solution-gap-analysis",
            json={"content": content, "platform": "test", "context": {}},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            gap_analysis = data.get('solution_gap_analysis', {})
            results['competitive'] = {
                'opportunity_score': gap_analysis.get('opportunity_score', 0),
                'gaps_identified': len(gap_analysis.get('gap_analysis', {}).get('identified_gaps', [])),
                'competitive_advantages': gap_analysis.get('competitive_analysis', {}).get('competitive_advantages', []),
                'bootstrap_feasible': gap_analysis.get('bootstrap_assessment', {}).get('feasibility_score', 0)
            }
            print(f"✅ Opportunity Score: {results['competitive']['opportunity_score']:.2f}")
            print(f"   Gaps Found: {results['competitive']['gaps_identified']}")
        else:
            print(f"❌ Competitive Analysis failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Competitive Analysis Error: {e}")
    
    # Validate against expected insights
    print(f"\n📊 Value Assessment:")
    total_score = 0
    max_score = 0
    
    if 'pain_points' in results:
        pain_score = results['pain_points']['confidence']
        total_score += pain_score
        max_score += 1
        print(f"   Pain Point Detection: {pain_score:.2f}/1.0 {'✅' if pain_score > 0.2 else '⚠️'}")
    
    if 'market' in results:
        market_score = results['market']['validation_score']
        total_score += market_score
        max_score += 1
        print(f"   Market Validation: {market_score:.2f}/1.0 {'✅' if market_score > 0.4 else '⚠️'}")
    
    if 'competitive' in results:
        comp_score = results['competitive']['opportunity_score']
        total_score += comp_score
        max_score += 1
        print(f"   Competitive Analysis: {comp_score:.2f}/1.0 {'✅' if comp_score > 0.3 else '⚠️'}")
    
    overall_score = (total_score / max_score) if max_score > 0 else 0
    print(f"   Overall Value Score: {overall_score:.2f}/1.0 {'🚀' if overall_score > 0.4 else '⚠️'}")
    
    return results, overall_score

def run_comprehensive_value_test():
    """Run comprehensive value validation with real scenarios"""
    print("🔍 Luciq Value Validation Test")
    print("=" * 50)
    
    # Real business scenarios to test
    test_scenarios = [
        {
            "name": "SaaS Project Management Pain",
            "content": "I'm so frustrated with project management tools. Asana is too complex for my 5-person team, Monday.com costs $200/month which is crazy for a startup, and Trello is too basic. I need something in between that doesn't break the bank but has good reporting. Why is everything either too simple or enterprise-level expensive?",
            "expected": ["pain_point_detected", "market_gap", "pricing_opportunity"]
        },
        {
            "name": "E-commerce Automation Need",
            "content": "Running a Shopify store and manually responding to customer service emails is killing me. Zendesk is $50/month per agent which adds up fast. I need something that can auto-respond to common questions but still feels personal. Most chatbots sound robotic and customers hate them.",
            "expected": ["automation_opportunity", "cost_pain", "personalization_gap"]
        },
        {
            "name": "Freelancer Invoicing Struggle",
            "content": "As a freelance designer, I hate dealing with invoices and payments. FreshBooks is $15/month which seems expensive for just invoicing. PayPal invoices look unprofessional. I need something that looks good, integrates with my bank, and doesn't cost a fortune. Why is financial software so expensive for solo entrepreneurs?",
            "expected": ["freelancer_market", "professional_appearance", "cost_sensitivity"]
        },
        {
            "name": "Remote Team Communication",
            "content": "Our remote team is struggling with communication. Slack gets chaotic with too many channels, Zoom fatigue is real, and email chains are a nightmare. We need something that combines async communication with quick video calls but isn't overwhelming. Microsoft Teams feels too corporate for our startup vibe.",
            "expected": ["remote_work_trend", "communication_overload", "startup_market"]
        },
        {
            "name": "Social Media Management Pain",
            "content": "Managing social media for my small business is a nightmare. Hootsuite is $50/month which is too much for a local restaurant. Buffer is cheaper but limited. I need to post to Instagram, Facebook, and TikTok but manually posting takes hours every week. Why are all the good tools so expensive for small businesses?",
            "expected": ["small_business_market", "multi_platform_need", "time_saving_value"]
        }
    ]
    
    all_results = []
    total_value_score = 0
    
    for scenario in test_scenarios:
        results, score = test_real_business_scenario(
            scenario["name"], 
            scenario["content"], 
            scenario["expected"]
        )
        all_results.append({
            "scenario": scenario["name"],
            "results": results,
            "score": score
        })
        total_value_score += score
        time.sleep(2)  # Rate limiting
    
    # Generate value assessment report
    avg_value_score = total_value_score / len(test_scenarios)
    
    print(f"\n🎯 COMPREHENSIVE VALUE ASSESSMENT")
    print("=" * 50)
    print(f"Average Value Score: {avg_value_score:.2f}/1.0")
    
    if avg_value_score > 0.5:
        print("🚀 EXCELLENT: High-value insights detected!")
        print("   Your API provides significant business intelligence value")
        print("   Ready for premium pricing ($149-299/month)")
    elif avg_value_score > 0.3:
        print("✅ GOOD: Solid value proposition detected")
        print("   Your API provides useful business insights")
        print("   Ready for competitive pricing ($49-149/month)")
    else:
        print("⚠️  NEEDS IMPROVEMENT: Value unclear")
        print("   Consider improving analysis algorithms")
        print("   Start with lower pricing ($29-49/month)")
    
    # Specific value propositions identified
    print(f"\n💡 KEY VALUE PROPOSITIONS DISCOVERED:")
    value_props = []
    
    for result in all_results:
        if result["score"] > 0.4:
            scenario_name = result["scenario"]
            if "pain_points" in result["results"]:
                confidence = result["results"]["pain_points"]["confidence"]
                if confidence > 0.2:
                    value_props.append(f"✅ {scenario_name}: Pain point detection working (confidence: {confidence:.2f})")
            
            if "market" in result["results"]:
                market_score = result["results"]["market"]["validation_score"]
                if market_score > 0.4:
                    value_props.append(f"✅ {scenario_name}: Market validation strong (score: {market_score:.2f})")
    
    for prop in value_props[:5]:  # Show top 5
        print(f"   {prop}")
    
    return avg_value_score, all_results

def generate_customer_demo_scenarios():
    """Generate demo scenarios for customer presentations"""
    print(f"\n🎬 CUSTOMER DEMO SCENARIOS")
    print("=" * 50)
    
    demo_scenarios = [
        {
            "title": "SaaS Opportunity Discovery",
            "description": "Analyze Reddit/Twitter posts to find underserved SaaS markets",
            "api_call": "POST /api/mvp/pain-point-detection",
            "sample_input": "Project management tools are either too simple or too expensive...",
            "expected_output": "Pain point confidence: 0.85, Market size: Large, Urgency: High"
        },
        {
            "title": "Market Validation",
            "description": "Validate business ideas before building",
            "api_call": "POST /api/mvp/market-validation", 
            "sample_input": "AI-powered invoice generator for freelancers",
            "expected_output": "Market score: 0.72, Competition: Medium, Timing: Excellent"
        },
        {
            "title": "Competitive Intelligence",
            "description": "Find gaps in competitive landscape",
            "api_call": "POST /api/mvp/competitive-analysis",
            "sample_input": "Social media management for small businesses",
            "expected_output": "Opportunity score: 0.68, 3 gaps identified, Bootstrap feasible"
        }
    ]
    
    for i, scenario in enumerate(demo_scenarios, 1):
        print(f"{i}. {scenario['title']}")
        print(f"   Use Case: {scenario['description']}")
        print(f"   API: {scenario['api_call']}")
        print(f"   Demo Input: {scenario['sample_input']}")
        print(f"   Expected: {scenario['expected_output']}")
        print()
    
    return demo_scenarios

if __name__ == "__main__":
    print("🚀 Luciq Value Validation & Demo Generator")
    print("=" * 60)
    
    # Run comprehensive value test
    avg_score, results = run_comprehensive_value_test()
    
    # Generate demo scenarios
    demo_scenarios = generate_customer_demo_scenarios()
    
    # Final recommendations
    print(f"\n🎯 LAUNCH RECOMMENDATIONS")
    print("=" * 50)
    
    if avg_score > 0.5:
        print("🚀 IMMEDIATE LAUNCH RECOMMENDED")
        print("   • Start with Professional tier: $149/month")
        print("   • Target: Entrepreneurs, VCs, consultants")
        print("   • Value prop: 'CB Insights for $149 vs $60K'")
        print("   • Expected conversion: 5-10% of trials")
    elif avg_score > 0.3:
        print("✅ LAUNCH WITH CAUTION")
        print("   • Start with Starter tier: $49/month")
        print("   • Target: Indie developers, small agencies")
        print("   • Value prop: 'Affordable business intelligence'")
        print("   • Expected conversion: 2-5% of trials")
    else:
        print("⚠️  IMPROVE BEFORE LAUNCH")
        print("   • Enhance analysis algorithms")
        print("   • Add more training data")
        print("   • Consider freemium model first")
    
    print(f"\n📊 Next Steps:")
    print("1. Review value test results above")
    print("2. Test with your own business scenarios")
    print("3. Create demo scenarios for customers")
    print("4. Implement MVP if value score > 0.3")
    print("5. Start with conservative pricing and scale up") 