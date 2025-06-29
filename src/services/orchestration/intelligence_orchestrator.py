#!/usr/bin/env python3
"""
Intelligence Orchestrator - Unified Interface to All Intelligence Engines
Provides clean API while preserving all engine capabilities exactly
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Import all existing engines (preserve exactly)
from src.api.domains.intelligence.services.cross_platform_intelligence import CrossPlatformIntelligenceEngine
from src.api.domains.intelligence.services.multimodal_fusion_engine import MultiModalFusionEngine
from src.api.domains.intelligence.services.semantic_analysis_engine import AdvancedSemanticEngine
from src.api.domains.intelligence.services.real_time_dialectical_engine import RealTimeDialecticalEngine
from src.api.domains.streaming.services.temporal_pattern_engine import AdvancedTemporalPatternEngine
from src.api.domains.intelligence.services.contextual_source_intelligence import ContextualSourceIntelligenceEngine

# Import orchestration components
from .engine_coordinator import EngineCoordinator
from .request_router import RequestRouter
from .response_synthesizer import ResponseSynthesizer
from .data_standardizer import data_standardizer

logger = logging.getLogger(__name__)

@dataclass
class OrchestrationRequest:
    """Request structure for orchestrated intelligence analysis"""
    request_type: str
    data: Dict[str, Any]
    session_id: Optional[str] = None
    priority: str = "normal"  # normal, high, critical
    timeout_seconds: int = 30
    engines_override: Optional[List[str]] = None

@dataclass
class OrchestrationResult:
    """Result structure from orchestrated intelligence analysis"""
    request_id: str
    request_type: str
    success: bool
    results: Dict[str, Any]
    engines_used: List[str]
    processing_time_ms: float
    orchestration_metadata: Dict[str, Any]
    timestamp: datetime

class IntelligenceOrchestrator:
    """
    Unified interface to all intelligence engines
    
    Provides clean API while preserving all engine capabilities exactly.
    Enables parallel execution, smart routing, and result synthesis.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("🧠 Initializing Intelligence Orchestrator...")
        
        # Initialize all engines exactly as before (ZERO changes to engine logic)
        self._initialize_engines()
        
        # Initialize orchestration components
        self.coordinator = EngineCoordinator(self.engines)
        self.router = RequestRouter()
        self.synthesizer = ResponseSynthesizer()
        
        # Performance tracking
        self.orchestration_stats = {
            'requests_processed': 0,
            'engines_coordinated': 0,
            'avg_processing_time_ms': 0.0,
            'parallel_executions': 0,
            'cache_hits': 0,
            'error_rate': 0.0
        }
        
        # Request cache for performance
        self.result_cache = {}
        self.cache_ttl_seconds = 300  # 5 minutes
        
        self.logger.info("✅ Intelligence Orchestrator initialized successfully")
    
    def _initialize_engines(self):
        """Initialize all intelligence engines exactly as they were before"""
        try:
            self.engines = {
                'cross_platform': CrossPlatformIntelligenceEngine(),
                'fusion': MultiModalFusionEngine(),
                'semantic': AdvancedSemanticEngine(),
                'dialectical': RealTimeDialecticalEngine(),
                'temporal': AdvancedTemporalPatternEngine(),
                'contextual': ContextualSourceIntelligenceEngine()
            }
            
            self.logger.info("✅ All intelligence engines initialized:")
            for engine_name in self.engines.keys():
                self.logger.info(f"   🔧 {engine_name} engine ready")
                
        except Exception as e:
            self.logger.error(f"❌ Engine initialization failed: {e}")
            raise
    
    async def analyze_intelligence(self, request: OrchestrationRequest) -> OrchestrationResult:
        """
        Main orchestrated intelligence analysis entry point
        
        Routes requests to appropriate engines and coordinates execution
        """
        start_time = datetime.now()
        request_id = f"req_{int(start_time.timestamp())}_{id(request)}"
        
        try:
            self.logger.info(f"🎯 Processing orchestrated request: {request.request_type}")
            
            # Check cache first
            cache_key = self._generate_cache_key(request)
            if cache_key in self.result_cache:
                cached_result = self.result_cache[cache_key]
                if self._is_cache_valid(cached_result):
                    self.orchestration_stats['cache_hits'] += 1
                    self.logger.info(f"⚡ Cache hit for request: {request.request_type}")
                    return cached_result
            
            # Standardize input data to fix attribute access issues
            standardized_data = self._standardize_request_data(request)
            
            # Route to appropriate engines
            routing_config = self.router.determine_engines(request.request_type, standardized_data)
            
            # Override engines if specified
            if request.engines_override:
                routing_config = self._create_override_config(request.engines_override)
            
            # Coordinate parallel execution
            engine_results = await self.coordinator.execute_engines(
                routing_config, standardized_data, request.session_id
            )
            
            # Synthesize results
            synthesized_result = await self.synthesizer.combine_results(
                engine_results, request.request_type
            )
            
            # Calculate processing time
            processing_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            # Create orchestration result
            result = OrchestrationResult(
                request_id=request_id,
                request_type=request.request_type,
                success=True,
                results=synthesized_result,
                engines_used=list(routing_config.get('primary', [])) + list(routing_config.get('supporting', [])),
                processing_time_ms=processing_time_ms,
                orchestration_metadata={
                    'routing_config': routing_config,
                    'cache_used': False,
                    'parallel_execution': len(routing_config.get('primary', [])) > 1,
                    'engines_count': len(engine_results),
                    'synthesis_method': 'intelligent_combination'
                },
                timestamp=datetime.now()
            )
            
            # Cache result
            self.result_cache[cache_key] = result
            
            # Update stats
            self._update_orchestration_stats(result)
            
            self.logger.info(f"✅ Orchestrated analysis complete: {processing_time_ms:.1f}ms")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Orchestrated analysis failed: {e}")
            
            # Return error result
            processing_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            return OrchestrationResult(
                request_id=request_id,
                request_type=request.request_type,
                success=False,
                results={'error': str(e)},
                engines_used=[],
                processing_time_ms=processing_time_ms,
                orchestration_metadata={'error': True},
                timestamp=datetime.now()
            )
    
    async def analyze_cross_platform_intelligence(self, platform_signals: Dict[str, List]) -> Dict:
        """Direct access to cross-platform intelligence (backward compatibility)"""
        request = OrchestrationRequest(
            request_type='cross_platform_analysis',
            data={'platform_signals': platform_signals}
        )
        result = await self.analyze_intelligence(request)
        return result.results
    
    async def process_multimodal_fusion(self, signal_data: Dict) -> Dict:
        """Direct access to multimodal fusion (backward compatibility)"""
        request = OrchestrationRequest(
            request_type='fusion_analysis',
            data=signal_data
        )
        result = await self.analyze_intelligence(request)
        return result.results
    
    async def analyze_semantic_understanding(self, content: str, context: Dict = None) -> Dict:
        """Direct access to semantic analysis (backward compatibility)"""
        request = OrchestrationRequest(
            request_type='semantic_analysis',
            data={'content': content, 'context': context or {}}
        )
        result = await self.analyze_intelligence(request)
        return result.results
    
    async def real_time_synthesis(self, query: str, session_id: str, force_context=None) -> Dict:
        """Direct access to real-time synthesis (backward compatibility)"""
        request = OrchestrationRequest(
            request_type='real_time_synthesis',
            data={'query': query, 'force_context': force_context},
            session_id=session_id
        )
        result = await self.analyze_intelligence(request)
        return result.results
    
    async def analyze_temporal_patterns(self, signals: List[Dict], timeframe_hours: int = 168) -> Dict:
        """Direct access to temporal analysis (backward compatibility)"""
        request = OrchestrationRequest(
            request_type='temporal_analysis',
            data={'signals': signals, 'timeframe_hours': timeframe_hours}
        )
        result = await self.analyze_intelligence(request)
        return result.results
    
    def _generate_cache_key(self, request: OrchestrationRequest) -> str:
        """Generate cache key for request"""
        import hashlib
        import json
        
        cache_data = {
            'request_type': request.request_type,
            'data_hash': hashlib.md5(json.dumps(request.data, sort_keys=True).encode()).hexdigest()
        }
        return f"{request.request_type}_{cache_data['data_hash']}"
    
    def _is_cache_valid(self, cached_result: OrchestrationResult) -> bool:
        """Check if cached result is still valid"""
        age_seconds = (datetime.now() - cached_result.timestamp).total_seconds()
        return age_seconds < self.cache_ttl_seconds
    
    def _create_override_config(self, engine_names: List[str]) -> Dict:
        """Create routing config from engine override list"""
        return {
            'primary': engine_names,
            'supporting': []
        }
    
    def _standardize_request_data(self, request: OrchestrationRequest) -> Dict[str, Any]:
        """
        Standardize request data to fix attribute access issues
        
        Fixes:
        - Dict objects missing 'engagement_score' attribute
        - Dict objects missing 'value' attribute
        - Inconsistent signal structures across engines
        """
        data = request.data.copy()
        
        try:
            # Standardize platform signals for cross-platform engine
            if request.request_type == 'cross_platform_analysis' and 'platform_signals' in data:
                data['platform_signals'] = data_standardizer.standardize_platform_signals(data['platform_signals'])
                self.logger.debug("✅ Standardized platform signals for cross-platform analysis")
            
            # Standardize temporal signals for temporal engine
            elif request.request_type == 'temporal_analysis' and 'signals' in data:
                data['signals'] = data_standardizer.standardize_temporal_signals(data['signals'])
                self.logger.debug("✅ Standardized temporal signals for temporal analysis")
            
            # Standardize comprehensive analysis data
            elif request.request_type == 'full_intelligence':
                if 'platform_signals' in data:
                    data['platform_signals'] = data_standardizer.standardize_platform_signals(data['platform_signals'])
                if 'signals' in data:
                    data['signals'] = data_standardizer.standardize_temporal_signals(data['signals'])
                self.logger.debug("✅ Standardized comprehensive analysis data")
            
            return data
            
        except Exception as e:
            self.logger.warning(f"⚠️ Data standardization failed: {e}, using original data")
            return request.data
    
    def _update_orchestration_stats(self, result: OrchestrationResult):
        """Update orchestration performance statistics"""
        self.orchestration_stats['requests_processed'] += 1
        self.orchestration_stats['engines_coordinated'] += len(result.engines_used)
        
        # Update average processing time
        current_avg = self.orchestration_stats['avg_processing_time_ms']
        new_avg = ((current_avg * (self.orchestration_stats['requests_processed'] - 1)) + 
                  result.processing_time_ms) / self.orchestration_stats['requests_processed']
        self.orchestration_stats['avg_processing_time_ms'] = new_avg
        
        # Track parallel executions
        if result.orchestration_metadata.get('parallel_execution', False):
            self.orchestration_stats['parallel_executions'] += 1
        
        # Track error rate
        if not result.success:
            error_count = self.orchestration_stats.get('error_count', 0) + 1
            self.orchestration_stats['error_count'] = error_count
            self.orchestration_stats['error_rate'] = error_count / self.orchestration_stats['requests_processed']
    
    def get_orchestration_stats(self) -> Dict[str, Any]:
        """Get orchestration performance statistics"""
        return {
            'orchestration_stats': self.orchestration_stats.copy(),
            'engine_status': {
                name: 'operational' for name in self.engines.keys()
            },
            'cache_stats': {
                'cached_results': len(self.result_cache),
                'cache_hit_rate': (self.orchestration_stats['cache_hits'] / 
                                 max(self.orchestration_stats['requests_processed'], 1)) * 100
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def clear_cache(self):
        """Clear result cache"""
        self.result_cache.clear()
        self.logger.info("🗑️ Orchestration cache cleared")

# Global orchestrator instance
_orchestrator_instance = None

def get_intelligence_orchestrator() -> IntelligenceOrchestrator:
    """Get global intelligence orchestrator instance"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = IntelligenceOrchestrator()
    return _orchestrator_instance 