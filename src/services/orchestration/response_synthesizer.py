#!/usr/bin/env python3
"""
Response Synthesizer - Intelligent Result Combination
Combines results from multiple engines into coherent, comprehensive responses
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from .engine_coordinator import EngineResult

logger = logging.getLogger(__name__)

@dataclass
class SynthesisStrategy:
    """Strategy for combining engine results"""
    strategy_name: str
    primary_weight: float = 0.7
    supporting_weight: float = 0.3
    conflict_resolution: str = "weighted_average"  # weighted_average, primary_wins, consensus
    quality_threshold: float = 0.5

class ResponseSynthesizer:
    """
    Synthesizes results from multiple engines into coherent responses
    
    Features:
    - Intelligent result combination
    - Conflict resolution
    - Quality assessment
    - Context preservation
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Synthesis strategies for different request types
        self.synthesis_strategies = self._initialize_synthesis_strategies()
        
        # Performance tracking
        self.synthesis_stats = {
            'syntheses_performed': 0,
            'conflicts_resolved': 0,
            'quality_improvements': 0,
            'avg_synthesis_time_ms': 0.0
        }
    
    def _initialize_synthesis_strategies(self) -> Dict[str, SynthesisStrategy]:
        """Initialize synthesis strategies for different request types"""
        
        return {
            'cross_platform_analysis': SynthesisStrategy(
                strategy_name='cross_platform_synthesis',
                primary_weight=0.8,
                supporting_weight=0.2,
                conflict_resolution='primary_wins',
                quality_threshold=0.6
            ),
            
            'real_time_synthesis': SynthesisStrategy(
                strategy_name='real_time_synthesis',
                primary_weight=0.6,
                supporting_weight=0.4,
                conflict_resolution='consensus',
                quality_threshold=0.7
            ),
            
            'semantic_analysis': SynthesisStrategy(
                strategy_name='semantic_synthesis',
                primary_weight=0.9,
                supporting_weight=0.1,
                conflict_resolution='primary_wins',
                quality_threshold=0.5
            ),
            
            'fusion_analysis': SynthesisStrategy(
                strategy_name='fusion_synthesis',
                primary_weight=0.7,
                supporting_weight=0.3,
                conflict_resolution='weighted_average',
                quality_threshold=0.6
            ),
            
            'temporal_analysis': SynthesisStrategy(
                strategy_name='temporal_synthesis',
                primary_weight=0.8,
                supporting_weight=0.2,
                conflict_resolution='primary_wins',
                quality_threshold=0.6
            ),
            
            'full_intelligence': SynthesisStrategy(
                strategy_name='comprehensive_synthesis',
                primary_weight=0.5,
                supporting_weight=0.5,
                conflict_resolution='consensus',
                quality_threshold=0.8
            )
        }
    
    async def combine_results(self, engine_results: Dict[str, EngineResult], 
                            request_type: str) -> Dict[str, Any]:
        """
        Combine results from multiple engines into a coherent response
        
        Args:
            engine_results: Results from individual engines
            request_type: Type of analysis request
            
        Returns:
            Synthesized result combining all engine outputs
        """
        
        start_time = datetime.now()
        
        try:
            self.logger.info(f"🔄 Synthesizing results from {len(engine_results)} engines")
            
            # Filter successful results
            successful_results = {
                name: result for name, result in engine_results.items() 
                if result.success and result.result is not None
            }
            
            if not successful_results:
                return {
                    'synthesis_status': 'failed',
                    'error': 'No successful engine results to synthesize',
                    'engine_errors': {name: result.error for name, result in engine_results.items() if not result.success}
                }
            
            # Get synthesis strategy
            strategy = self.synthesis_strategies.get(request_type, self.synthesis_strategies['full_intelligence'])
            
            # Perform synthesis based on strategy
            synthesized_result = await self._synthesize_with_strategy(successful_results, strategy, request_type)
            
            # Add metadata
            synthesis_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            synthesized_result['synthesis_metadata'] = {
                'engines_used': list(successful_results.keys()),
                'synthesis_strategy': strategy.strategy_name,
                'synthesis_time_ms': synthesis_time_ms,
                'quality_score': self._calculate_quality_score(synthesized_result),
                'conflicts_detected': 0,  # TODO: Implement conflict detection
                'timestamp': datetime.now().isoformat()
            }
            
            # Update synthesis stats
            self._update_synthesis_stats(synthesis_time_ms)
            
            self.logger.info(f"✅ Result synthesis complete: {synthesis_time_ms:.1f}ms")
            return synthesized_result
            
        except Exception as e:
            self.logger.error(f"❌ Result synthesis failed: {e}")
            return {
                'synthesis_status': 'error',
                'error': str(e),
                'raw_results': {name: result.result for name, result in engine_results.items() if result.success}
            }
    
    async def _synthesize_with_strategy(self, results: Dict[str, EngineResult], 
                                      strategy: SynthesisStrategy, request_type: str) -> Dict[str, Any]:
        """Synthesize results using the specified strategy"""
        
        # Extract result data
        result_data = {name: result.result for name, result in results.items()}
        
        # Route to appropriate synthesis method based on request type
        if request_type == 'cross_platform_analysis':
            return await self._synthesize_cross_platform(result_data, strategy)
        
        elif request_type == 'real_time_synthesis':
            return await self._synthesize_real_time(result_data, strategy)
        
        elif request_type == 'semantic_analysis':
            return await self._synthesize_semantic(result_data, strategy)
        
        elif request_type == 'fusion_analysis':
            return await self._synthesize_fusion(result_data, strategy)
        
        elif request_type == 'temporal_analysis':
            return await self._synthesize_temporal(result_data, strategy)
        
        else:
            return await self._synthesize_comprehensive(result_data, strategy)
    
    async def _synthesize_cross_platform(self, results: Dict[str, Any], strategy: SynthesisStrategy) -> Dict[str, Any]:
        """Synthesize cross-platform analysis results"""
        
        synthesis = {
            'synthesis_type': 'cross_platform_analysis',
            'platform_insights': {},
            'cross_platform_patterns': [],
            'opportunity_scores': {},
            'recommendations': []
        }
        
        # Process cross-platform engine results
        if 'cross_platform' in results:
            cp_result = results['cross_platform']
            if isinstance(cp_result, dict):
                synthesis['platform_insights'] = cp_result.get('platform_insights', {})
                synthesis['cross_platform_patterns'] = cp_result.get('patterns', [])
                synthesis['opportunity_scores'] = cp_result.get('opportunity_scores', {})
        
        # Enhance with semantic analysis
        if 'semantic' in results:
            semantic_result = results['semantic']
            if isinstance(semantic_result, dict):
                synthesis['semantic_insights'] = semantic_result.get('insights', {})
                synthesis['content_analysis'] = semantic_result.get('analysis', {})
        
        # Add temporal context
        if 'temporal' in results:
            temporal_result = results['temporal']
            if isinstance(temporal_result, dict):
                synthesis['temporal_trends'] = temporal_result.get('trends', [])
                synthesis['pattern_predictions'] = temporal_result.get('predictions', [])
        
        # Generate combined recommendations
        synthesis['recommendations'] = self._generate_cross_platform_recommendations(synthesis)
        
        return synthesis
    
    async def _synthesize_real_time(self, results: Dict[str, Any], strategy: SynthesisStrategy) -> Dict[str, Any]:
        """Synthesize real-time analysis results"""
        
        synthesis = {
            'synthesis_type': 'real_time_synthesis',
            'real_time_insights': {},
            'contextual_understanding': {},
            'immediate_recommendations': [],
            'confidence_score': 0.0
        }
        
        # Process dialectical engine results
        if 'dialectical' in results:
            dialectical_result = results['dialectical']
            if isinstance(dialectical_result, dict):
                synthesis['real_time_insights'] = dialectical_result.get('synthesis', {})
                synthesis['contextual_understanding'] = dialectical_result.get('context', {})
                synthesis['confidence_score'] = dialectical_result.get('confidence', 0.0)
        
        # Enhance with fusion results
        if 'fusion' in results:
            fusion_result = results['fusion']
            if isinstance(fusion_result, dict):
                synthesis['multimodal_insights'] = fusion_result.get('insights', {})
                synthesis['signal_quality'] = fusion_result.get('quality_score', 0.0)
        
        # Add semantic context
        if 'semantic' in results:
            semantic_result = results['semantic']
            if isinstance(semantic_result, dict):
                synthesis['semantic_context'] = semantic_result.get('context', {})
        
        # Generate immediate recommendations
        synthesis['immediate_recommendations'] = self._generate_real_time_recommendations(synthesis)
        
        return synthesis
    
    async def _synthesize_semantic(self, results: Dict[str, Any], strategy: SynthesisStrategy) -> Dict[str, Any]:
        """Synthesize semantic analysis results"""
        
        synthesis = {
            'synthesis_type': 'semantic_analysis',
            'semantic_insights': {},
            'understanding_depth': 0.0,
            'key_concepts': [],
            'contextual_relevance': 0.0
        }
        
        # Process semantic engine results
        if 'semantic' in results:
            semantic_result = results['semantic']
            if isinstance(semantic_result, dict):
                synthesis['semantic_insights'] = semantic_result.get('insights', {})
                synthesis['understanding_depth'] = semantic_result.get('depth_score', 0.0)
                synthesis['key_concepts'] = semantic_result.get('concepts', [])
                synthesis['contextual_relevance'] = semantic_result.get('relevance_score', 0.0)
        
        # Enhance with contextual intelligence
        if 'contextual' in results:
            contextual_result = results['contextual']
            if isinstance(contextual_result, dict):
                synthesis['contextual_sources'] = contextual_result.get('sources', [])
                synthesis['source_quality'] = contextual_result.get('quality_scores', {})
        
        return synthesis
    
    async def _synthesize_fusion(self, results: Dict[str, Any], strategy: SynthesisStrategy) -> Dict[str, Any]:
        """Synthesize multimodal fusion results"""
        
        synthesis = {
            'synthesis_type': 'fusion_analysis',
            'multimodal_insights': {},
            'signal_quality': 0.0,
            'fusion_confidence': 0.0,
            'modality_contributions': {}
        }
        
        # Process fusion engine results
        if 'fusion' in results:
            fusion_result = results['fusion']
            if isinstance(fusion_result, dict):
                synthesis['multimodal_insights'] = fusion_result.get('insights', {})
                synthesis['signal_quality'] = fusion_result.get('quality_score', 0.0)
                synthesis['fusion_confidence'] = fusion_result.get('confidence', 0.0)
        
        # Add semantic enhancement
        if 'semantic' in results:
            semantic_result = results['semantic']
            if isinstance(semantic_result, dict):
                synthesis['semantic_enhancement'] = semantic_result.get('insights', {})
        
        # Add temporal patterns
        if 'temporal' in results:
            temporal_result = results['temporal']
            if isinstance(temporal_result, dict):
                synthesis['temporal_patterns'] = temporal_result.get('patterns', [])
        
        return synthesis
    
    async def _synthesize_temporal(self, results: Dict[str, Any], strategy: SynthesisStrategy) -> Dict[str, Any]:
        """Synthesize temporal analysis results"""
        
        synthesis = {
            'synthesis_type': 'temporal_analysis',
            'temporal_patterns': [],
            'trend_predictions': [],
            'pattern_confidence': 0.0,
            'time_horizon': 'unknown'
        }
        
        # Process temporal engine results
        if 'temporal' in results:
            temporal_result = results['temporal']
            if isinstance(temporal_result, dict):
                synthesis['temporal_patterns'] = temporal_result.get('patterns', [])
                synthesis['trend_predictions'] = temporal_result.get('predictions', [])
                synthesis['pattern_confidence'] = temporal_result.get('confidence', 0.0)
                synthesis['time_horizon'] = temporal_result.get('time_horizon', 'unknown')
        
        # Add semantic context
        if 'semantic' in results:
            semantic_result = results['semantic']
            if isinstance(semantic_result, dict):
                synthesis['semantic_context'] = semantic_result.get('context', {})
        
        return synthesis
    
    async def _synthesize_comprehensive(self, results: Dict[str, Any], strategy: SynthesisStrategy) -> Dict[str, Any]:
        """Synthesize comprehensive analysis from all engines"""
        
        synthesis = {
            'synthesis_type': 'comprehensive_analysis',
            'comprehensive_insights': {},
            'multi_engine_consensus': {},
            'confidence_scores': {},
            'integrated_recommendations': []
        }
        
        # Combine insights from all engines
        for engine_name, result in results.items():
            if isinstance(result, dict):
                synthesis['comprehensive_insights'][engine_name] = result.get('insights', result)
                
                # Extract confidence scores
                if 'confidence' in result:
                    synthesis['confidence_scores'][engine_name] = result['confidence']
                elif 'quality_score' in result:
                    synthesis['confidence_scores'][engine_name] = result['quality_score']
        
        # Generate integrated recommendations
        synthesis['integrated_recommendations'] = self._generate_comprehensive_recommendations(synthesis)
        
        return synthesis
    
    def _generate_cross_platform_recommendations(self, synthesis: Dict[str, Any]) -> List[str]:
        """Generate recommendations for cross-platform analysis"""
        recommendations = []
        
        # Analyze platform insights
        platform_insights = synthesis.get('platform_insights', {})
        if platform_insights:
            recommendations.append("Focus on platforms with highest opportunity scores")
            recommendations.append("Leverage cross-platform patterns for broader reach")
        
        # Add temporal recommendations
        if 'temporal_trends' in synthesis:
            recommendations.append("Consider temporal trends for timing optimization")
        
        return recommendations
    
    def _generate_real_time_recommendations(self, synthesis: Dict[str, Any]) -> List[str]:
        """Generate immediate recommendations for real-time analysis"""
        recommendations = []
        
        confidence = synthesis.get('confidence_score', 0.0)
        if confidence > 0.7:
            recommendations.append("High confidence - proceed with immediate action")
        elif confidence > 0.5:
            recommendations.append("Moderate confidence - gather additional data")
        else:
            recommendations.append("Low confidence - require further analysis")
        
        return recommendations
    
    def _generate_comprehensive_recommendations(self, synthesis: Dict[str, Any]) -> List[str]:
        """Generate integrated recommendations from comprehensive analysis"""
        recommendations = []
        
        # Analyze confidence scores
        confidence_scores = synthesis.get('confidence_scores', {})
        if confidence_scores:
            avg_confidence = sum(confidence_scores.values()) / len(confidence_scores)
            if avg_confidence > 0.7:
                recommendations.append("High multi-engine consensus - strong recommendation confidence")
            else:
                recommendations.append("Mixed engine results - consider additional validation")
        
        return recommendations
    
    def _calculate_quality_score(self, synthesis: Dict[str, Any]) -> float:
        """Calculate overall quality score for synthesis"""
        
        # Basic quality assessment based on data completeness
        quality_factors = []
        
        # Check for key synthesis components
        if synthesis.get('synthesis_type'):
            quality_factors.append(0.2)
        
        if synthesis.get('recommendations') or synthesis.get('immediate_recommendations') or synthesis.get('integrated_recommendations'):
            quality_factors.append(0.3)
        
        # Check for confidence/quality indicators
        if synthesis.get('confidence_score', 0) > 0:
            quality_factors.append(synthesis['confidence_score'] * 0.3)
        elif synthesis.get('signal_quality', 0) > 0:
            quality_factors.append(synthesis['signal_quality'] * 0.3)
        
        # Check for insights
        insights_keys = ['insights', 'semantic_insights', 'multimodal_insights', 'comprehensive_insights']
        if any(key in synthesis for key in insights_keys):
            quality_factors.append(0.2)
        
        return sum(quality_factors) if quality_factors else 0.5
    
    def _update_synthesis_stats(self, synthesis_time_ms: float):
        """Update synthesis performance statistics"""
        
        self.synthesis_stats['syntheses_performed'] += 1
        
        # Update average synthesis time
        current_avg = self.synthesis_stats['avg_synthesis_time_ms']
        syntheses = self.synthesis_stats['syntheses_performed']
        new_avg = ((current_avg * (syntheses - 1)) + synthesis_time_ms) / syntheses
        self.synthesis_stats['avg_synthesis_time_ms'] = new_avg
    
    def get_synthesis_stats(self) -> Dict[str, Any]:
        """Get synthesis performance statistics"""
        return {
            'synthesis_stats': self.synthesis_stats.copy(),
            'available_strategies': list(self.synthesis_strategies.keys()),
            'timestamp': datetime.now().isoformat()
        } 