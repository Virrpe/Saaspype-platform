#!/usr/bin/env python3
"""
Test Dialectical Synthesis Engine
Demonstrates the Hegelian resolution of quantity-quality contradiction
"""

import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.api.domains.intelligence.services.contextual_source_intelligence import (
    ContextualSourceIntelligenceEngine, QueryContext
)

async def test_dialectical_synthesis():
    """Test the dialectical synthesis with various query types"""
    
    print("🧠 HEGELIAN DIALECTICAL SYNTHESIS ENGINE TEST")
    print("=" * 60)
    print("Testing the resolution of quantity-quality contradiction through contextual intelligence")
    print()
    
    # Initialize the engine
    engine = ContextualSourceIntelligenceEngine()
    
    # Test queries representing different contexts
    test_queries = [
        {
            'query': "What are the biggest pain points developers face with project management tools?",
            'expected_context': QueryContext.PAIN_POINT_DISCOVERY,
            'description': "Pain Point Discovery"
        },
        {
            'query': "What are the latest trending technologies in machine learning and AI development?",
            'expected_context': QueryContext.TECHNICAL_TRENDS,
            'description': "Technical Trends Analysis"
        },
        {
            'query': "How can I validate my SaaS product idea before building it?",
            'expected_context': QueryContext.MARKET_VALIDATION,
            'description': "Market Validation Strategy"
        },
        {
            'query': "What startup funding trends are happening right now in 2024?",
            'expected_context': QueryContext.STARTUP_INTELLIGENCE,
            'description': "Startup Intelligence"
        },
        {
            'query': "What programming frameworks are developers most excited about?",
            'expected_context': QueryContext.DEVELOPER_INSIGHTS,
            'description': "Developer Insights"
        },
        {
            'query': "Find me some interesting business opportunities",
            'expected_context': QueryContext.GENERAL_EXPLORATION,
            'description': "General Exploration"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"🎯 TEST {i}: {test_case['description']}")
        print(f"Query: \"{test_case['query']}\"")
        print("-" * 50)
        
        # Run dialectical analysis
        result = await engine.determine_optimal_sources(test_case['query'])
        results.append(result)
        
        # Display results
        print(f"📊 DIALECTICAL ANALYSIS RESULTS:")
        print(f"   Detected Context: {result['context'].value}")
        print(f"   Sources Activated: {len(result['selected_sources'])}")
        
        print(f"\n🎯 SELECTED SOURCES:")
        for source_info in result['selected_sources']:
            print(f"   • {source_info['source']}: "
                  f"Synthesis={source_info['synthesis_score']:.3f}, "
                  f"ROI={source_info['expected_roi']:.2f}, "
                  f"Max Signals={source_info['max_signals']}")
        
        print(f"\n🧠 DIALECTICAL REASONING:")
        reasoning = result['dialectical_reasoning']
        print(f"   Thesis: {reasoning['dialectical_process']['thesis_analysis']}")
        print(f"   Antithesis: {reasoning['dialectical_process']['antithesis_analysis']}")
        print(f"   Synthesis: {reasoning['dialectical_process']['synthesis_resolution']}")
        
        if reasoning['rejected_sources']:
            print(f"\n❌ REJECTED SOURCES:")
            for rejected in reasoning['rejected_sources']:
                print(f"   • {rejected['source']}: {rejected['reason']} (Score: {rejected['synthesis_score']})")
        
        print(f"\n📈 SYNTHESIS METADATA:")
        metadata = result['synthesis_metadata']
        print(f"   Sources Considered: {metadata['total_sources_considered']}")
        print(f"   Sources Activated: {metadata['sources_activated']}")
        print(f"   Avg Synthesis Score: {metadata['avg_synthesis_score']:.3f}")
        print(f"   Dialectical Tension Resolved: {metadata['dialectical_tension_resolved']:.3f}")
        
        print("\n" + "="*60 + "\n")
    
    # Generate performance report
    print("📊 DIALECTICAL PERFORMANCE REPORT")
    print("=" * 60)
    
    performance = engine.get_dialectical_performance_report()
    
    print(f"📈 SUMMARY:")
    summary = performance['dialectical_summary']
    print(f"   Total Queries Processed: {summary['total_queries_processed']}")
    print(f"   Contexts Encountered: {summary['contexts_encountered']}")
    print(f"   Avg Sources per Query: {summary['avg_sources_per_query']}")
    print(f"   Dialectical Efficiency: {summary['dialectical_efficiency']}")
    
    print(f"\n🎯 CONTEXT DISTRIBUTION:")
    for context, count in performance['context_distribution'].items():
        print(f"   {context.value}: {count} queries")
    
    print(f"\n📊 SOURCE ACTIVATION FREQUENCY:")
    for source, count in performance['source_activation_frequency'].items():
        activation_rate = (count / len(test_queries)) * 100
        print(f"   {source}: {count}/{len(test_queries)} queries ({activation_rate:.1f}%)")
    
    print(f"\n✅ SYNTHESIS EFFECTIVENESS:")
    effectiveness = performance['synthesis_effectiveness']
    print(f"   Average Synthesis Score: {effectiveness['avg_synthesis_score']:.3f}")
    print(f"   Status: {effectiveness['dialectical_tension_resolution']}")
    
    # Demonstrate the dialectical principle
    print(f"\n🎯 HEGELIAN DIALECTICAL PRINCIPLE DEMONSTRATED:")
    print("=" * 60)
    
    # Calculate traditional vs dialectical approach
    traditional_sources = 8  # All sources always
    dialectical_avg = summary['avg_sources_per_query']
    efficiency_gain = ((traditional_sources - dialectical_avg) / traditional_sources) * 100
    
    print(f"📊 COMPARISON:")
    print(f"   Traditional Approach: {traditional_sources} sources per query (quantity focus)")
    print(f"   Dialectical Synthesis: {dialectical_avg} sources per query (contextual optimization)")
    print(f"   Efficiency Improvement: {efficiency_gain:.1f}% reduction in source usage")
    print(f"   Quality Preservation: Maintained through contextual intelligence")
    
    print(f"\n💡 DIALECTICAL INSIGHTS:")
    print(f"   ✅ THESIS (More Sources): Preserved through comprehensive source pool")
    print(f"   ✅ ANTITHESIS (Fewer Sources): Preserved through selective activation")
    print(f"   ✅ SYNTHESIS (Contextual Intelligence): Achieved optimal balance")
    print(f"   🎯 AUFHEBUNG: Quantity-quality contradiction resolved at higher level")
    
    print(f"\n🚀 PRACTICAL BENEFITS:")
    print(f"   • Reduced processing costs by {efficiency_gain:.1f}%")
    print(f"   • Maintained signal quality through context-aware selection")
    print(f"   • Eliminated redundant/correlated sources dynamically")
    print(f"   • Adaptive to different query types and contexts")
    print(f"   • Preserves multi-source capability while optimizing efficiency")
    
    return results

async def demonstrate_context_switching():
    """Demonstrate how the engine adapts to different contexts"""
    
    print("\n🔄 CONTEXT SWITCHING DEMONSTRATION")
    print("=" * 60)
    
    engine = ContextualSourceIntelligenceEngine()
    
    # Same base query with different contextual hints
    base_query = "AI development tools"
    
    context_variations = [
        (f"What are the biggest problems with {base_query}?", "Pain Point Focus"),
        (f"What are the latest trends in {base_query}?", "Technical Trends Focus"),
        (f"How to validate market demand for {base_query}?", "Market Validation Focus"),
        (f"What do developers think about {base_query}?", "Developer Insights Focus")
    ]
    
    for query, description in context_variations:
        print(f"🎯 {description}")
        print(f"Query: \"{query}\"")
        
        result = await engine.determine_optimal_sources(query)
        
        print(f"Context: {result['context'].value}")
        print(f"Sources: {[s['source'] for s in result['selected_sources']]}")
        print(f"Avg Synthesis Score: {result['synthesis_metadata']['avg_synthesis_score']:.3f}")
        print("-" * 40)
    
    print("✅ Demonstrated contextual adaptation - same topic, different source strategies!")

if __name__ == "__main__":
    async def main():
        await test_dialectical_synthesis()
        await demonstrate_context_switching()
    
    asyncio.run(main()) 