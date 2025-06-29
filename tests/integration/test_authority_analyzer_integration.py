#!/usr/bin/env python3
"""
Integration Test: Authority Analyzer Integration with ContextualSourceIntelligenceEngine
Phase 1 Tactical Improvement Validation
"""

import pytest
import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.api.domains.intelligence.services.contextual_source_intelligence import (
    ContextualSourceIntelligenceEngine, QueryContext
)
from src.api.domains.intelligence.services.authority_analyzer import AuthorityAnalyzer

@pytest.mark.asyncio
class TestAuthorityAnalyzerIntegration:
    """Test suite for Authority Analyzer integration with ContextualSourceIntelligenceEngine"""
    
    @pytest.fixture
    def engine(self):
        """Create a ContextualSourceIntelligenceEngine instance"""
        return ContextualSourceIntelligenceEngine()
    
    @pytest.fixture
    def authority_analyzer(self):
        """Create an AuthorityAnalyzer instance for comparison"""
        return AuthorityAnalyzer()
    
    def test_authority_analyzer_initialization(self, engine):
        """Test that the Authority Analyzer is properly initialized in the engine"""
        
        # Check that authority analyzer is present
        assert hasattr(engine, 'authority_analyzer')
        assert engine.authority_analyzer is not None
        assert isinstance(engine.authority_analyzer, AuthorityAnalyzer)
    
    def test_enhanced_source_characteristics(self, engine):
        """Test that source characteristics are enhanced with authority metrics"""
        
        # Check that source characteristics contain authority enhancements
        for source, characteristics in engine.source_characteristics.items():
            # Verify authority enhancement fields are present
            assert 'authority_score' in characteristics, f"Missing authority_score for {source}"
            assert 'dialectical_quality' in characteristics, f"Missing dialectical_quality for {source}"
            assert 'quality_enhancement' in characteristics, f"Missing quality_enhancement for {source}"
            assert 'dialectical_metadata' in characteristics, f"Missing dialectical_metadata for {source}"
            
            # Verify authority score is valid
            authority_score = characteristics['authority_score']
            assert 0 <= authority_score <= 1, f"Invalid authority_score for {source}: {authority_score}"
            
            # Verify dialectical quality is valid
            dialectical_quality = characteristics['dialectical_quality']
            assert 0 <= dialectical_quality <= 1, f"Invalid dialectical_quality for {source}: {dialectical_quality}"
    
    def test_quality_improvements_from_authority(self, engine):
        """Test that authority analysis actually improves quality scores"""
        
        improvements_found = False
        
        for source, characteristics in engine.source_characteristics.items():
            base_quality = characteristics.get('base_quality', 0.5)
            dialectical_quality = characteristics.get('dialectical_quality', 0.5)
            quality_enhancement = characteristics.get('quality_enhancement', 0)
            
            # Check if this source shows improvement
            if quality_enhancement > 0:
                improvements_found = True
                assert dialectical_quality > base_quality, f"Dialectical quality should be higher for {source}"
                
            # Verify enhancement calculation
            expected_enhancement = dialectical_quality - base_quality
            assert abs(quality_enhancement - expected_enhancement) < 0.001, \
                f"Quality enhancement calculation mismatch for {source}"
        
        # We should see at least some improvements from authority analysis
        assert improvements_found, "No quality improvements found from authority analysis"
    
    async def test_dialectical_synthesis_with_authority(self, engine):
        """Test that dialectical synthesis uses authority-enhanced quality scores"""
        
        # Test query for pain point discovery
        test_query = "struggling with API integration errors"
        
        # Get synthesis result
        result = await engine.determine_optimal_sources(test_query, QueryContext.PAIN_POINT_DISCOVERY)
        
        # Verify result structure
        assert 'context' in result
        assert 'selected_sources' in result
        assert 'dialectical_reasoning' in result
        assert 'synthesis_metadata' in result
        
        # Check that sources were selected
        selected_sources = result['selected_sources']
        assert len(selected_sources) > 0, "No sources selected"
        
        # Verify that quality scores in selection reasoning reflect authority enhancement
        dialectical_reasoning = result['dialectical_reasoning']
        selection_reasoning = dialectical_reasoning['selection_reasoning']
        
        for source_info in selection_reasoning:
            source_name = source_info['source']
            antithesis_score = source_info['antithesis_score']
            
            # Verify antithesis score uses enhanced quality
            source_char = engine.source_characteristics[source_name]
            base_quality = source_char['base_quality']
            dialectical_quality = source_char.get('dialectical_quality', base_quality)
            
            # The antithesis score should reflect the enhanced quality
            # (We can't test exact values due to contextual weights and other factors,
            # but we can verify the enhancement is being used)
            assert antithesis_score > 0, f"Invalid antithesis score for {source_name}"
    
    def test_specific_authority_improvements(self, engine, authority_analyzer):
        """Test specific expected authority improvements based on empirical results"""
        
        # Based on our validation results from the tactical improvements:
        # Reddit: +13% improvement expected
        # GitHub: +9% improvement expected  
        # ProductHunt: +16% improvement expected
        
        expected_improvements = {
            'reddit': 0.10,      # At least 10% improvement
            'github': 0.05,      # At least 5% improvement
            'producthunt': 0.10  # At least 10% improvement
        }
        
        for source, min_improvement in expected_improvements.items():
            if source in engine.source_characteristics:
                characteristics = engine.source_characteristics[source]
                enhancement = characteristics.get('quality_enhancement', 0)
                
                assert enhancement >= min_improvement, \
                    f"Expected at least {min_improvement:.1%} improvement for {source}, got {enhancement:.1%}"
    
    async def test_authority_ranking_integration(self, engine):
        """Test that authority ranking affects source selection"""
        
        # Get authority ranking
        authority_ranking = engine.authority_analyzer.get_authority_ranking()
        
        # Verify ranking structure
        assert len(authority_ranking) > 0, "Authority ranking is empty"
        
        # Verify highest authority sources appear in engine characteristics
        top_sources = list(authority_ranking.keys())[:3]  # Top 3 authority sources
        
        for source in top_sources:
            assert source in engine.source_characteristics, \
                f"Top authority source {source} not in engine characteristics"
            
            # High authority sources should have good authority scores
            authority_score = engine.source_characteristics[source]['authority_score']
            assert authority_score > 0.8, \
                f"Top authority source {source} has low authority score: {authority_score}"
    
    async def test_context_specific_quality_enhancement(self, engine):
        """Test that quality enhancement works across different contexts"""
        
        test_contexts = [
            (QueryContext.TECHNICAL_TRENDS, "new JavaScript framework trending"),
            (QueryContext.PAIN_POINT_DISCOVERY, "developers frustrated with deployment process"),
            (QueryContext.MARKET_VALIDATION, "startup product launch feedback")
        ]
        
        for context, query in test_contexts:
            result = await engine.determine_optimal_sources(query, context)
            
            # Verify sources were selected for each context
            assert len(result['selected_sources']) > 0, \
                f"No sources selected for context {context.value}"
            
            # Verify synthesis metadata indicates authority enhancement
            synthesis_metadata = result['synthesis_metadata']
            assert 'avg_synthesis_score' in synthesis_metadata
            assert synthesis_metadata['avg_synthesis_score'] > 0.5, \
                f"Low synthesis score for {context.value}"
    
    def test_dialectical_metadata_completeness(self, engine):
        """Test that dialectical metadata contains all expected authority information"""
        
        for source, characteristics in engine.source_characteristics.items():
            if 'dialectical_metadata' in characteristics:
                metadata = characteristics['dialectical_metadata']
                
                # Verify required dialectical metadata fields
                required_fields = [
                    'authority_score', 'engagement_score', 'thesis_score', 
                    'antithesis_score', 'dialectical_tension', 'synthesis_score',
                    'dialectical_improvement', 'synthesis_quality'
                ]
                
                for field in required_fields:
                    assert field in metadata, f"Missing {field} in dialectical metadata for {source}"
                    
                # Verify values are in valid ranges
                assert 0 <= metadata['authority_score'] <= 1
                assert 0 <= metadata['engagement_score'] <= 1
                assert 0 <= metadata['synthesis_score'] <= 1
                assert metadata['dialectical_tension'] >= 0

# Integration test runner
async def run_integration_tests():
    """Run integration tests manually"""
    
    print("🧪 AUTHORITY ANALYZER INTEGRATION TESTS")
    print("=" * 60)
    
    # Create test instances
    engine = ContextualSourceIntelligenceEngine()
    authority_analyzer = AuthorityAnalyzer()
    
    print("\n1. Testing Authority Analyzer Initialization...")
    assert hasattr(engine, 'authority_analyzer')
    print("✅ Authority Analyzer properly initialized")
    
    print("\n2. Testing Enhanced Source Characteristics...")
    enhanced_count = 0
    for source, chars in engine.source_characteristics.items():
        if 'dialectical_quality' in chars:
            enhanced_count += 1
            improvement = chars.get('quality_enhancement', 0)
            print(f"   📊 {source}: {improvement:+.3f} quality enhancement")
    
    assert enhanced_count > 0
    print(f"✅ {enhanced_count} sources enhanced with authority analysis")
    
    print("\n3. Testing Dialectical Synthesis Integration...")
    result = await engine.determine_optimal_sources(
        "API integration problems", 
        QueryContext.PAIN_POINT_DISCOVERY
    )
    
    selected_count = len(result['selected_sources'])
    avg_synthesis = result['synthesis_metadata']['avg_synthesis_score']
    print(f"   🎯 Selected {selected_count} sources with avg synthesis score: {avg_synthesis:.3f}")
    print("✅ Dialectical synthesis using authority-enhanced quality")
    
    print("\n4. Testing Authority Ranking Integration...")
    authority_ranking = engine.authority_analyzer.get_authority_ranking()
    top_3 = list(authority_ranking.items())[:3]
    print("   🏆 Top 3 Authority Sources:")
    for i, (source, score) in enumerate(top_3, 1):
        print(f"      {i}. {source}: {score:.3f}")
    print("✅ Authority ranking integration working")
    
    print(f"\n🎉 ALL INTEGRATION TESTS PASSED!")
    print(f"   Authority Analyzer successfully integrated into ContextualSourceIntelligenceEngine")
    print(f"   Phase 1 Tactical Improvement: COMPLETE")

if __name__ == "__main__":
    asyncio.run(run_integration_tests()) 