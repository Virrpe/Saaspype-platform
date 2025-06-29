#!/usr/bin/env python3
"""
Engine Coordinator - Smart Parallel Execution of Intelligence Engines
Coordinates parallel execution of multiple engines with dependency management
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ExecutionPhase:
    """Represents a phase of engine execution with dependencies"""
    phase_id: int
    engines: Dict[str, Dict[str, Any]]
    dependencies: List[int]

@dataclass
class EngineResult:
    """Result from individual engine execution"""
    engine_name: str
    success: bool
    result: Any
    processing_time_ms: float
    error: Optional[str] = None

class EngineCoordinator:
    """
    Coordinates parallel execution of multiple engines
    
    Features:
    - Dependency-aware execution planning
    - Parallel execution where possible
    - Error handling and graceful degradation
    - Performance monitoring
    """
    
    def __init__(self, engines: Dict[str, Any]):
        self.engines = engines
        self.logger = logging.getLogger(__name__)
        
        # Execution dependencies (which engines depend on others)
        self.dependencies = {
            'fusion': [],  # Can run independently
            'semantic': [],  # Can run independently
            'cross_platform': ['semantic'],  # Benefits from semantic analysis
            'temporal': [],  # Can run independently
            'dialectical': ['semantic', 'contextual'],  # Needs context and semantic
            'contextual': []  # Can run independently
        }
        
        # Performance tracking
        self.coordination_stats = {
            'executions_coordinated': 0,
            'parallel_executions': 0,
            'dependency_optimizations': 0,
            'avg_coordination_time_ms': 0.0
        }
    
    async def execute_engines(self, routing_config: Dict, data: Dict[str, Any], 
                            session_id: Optional[str] = None) -> Dict[str, EngineResult]:
        """
        Execute multiple engines according to routing configuration
        
        Args:
            routing_config: Configuration specifying primary and supporting engines
            data: Input data for engines
            session_id: Optional session ID for stateful engines
            
        Returns:
            Dictionary of engine results
        """
        start_time = datetime.now()
        
        try:
            # Extract engines to execute
            primary_engines = routing_config.get('primary', [])
            supporting_engines = routing_config.get('supporting', [])
            all_engines = list(set(primary_engines + supporting_engines))
            
            self.logger.info(f"🎯 Coordinating {len(all_engines)} engines: {all_engines}")
            
            # Create execution plan with dependency management
            execution_plan = self._create_execution_plan(all_engines)
            
            # Execute engines in phases
            all_results = {}
            for phase in execution_plan:
                phase_results = await self._execute_phase(phase, data, session_id, all_results)
                all_results.update(phase_results)
            
            # Update coordination stats
            coordination_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            self._update_coordination_stats(coordination_time_ms, len(all_engines), len(execution_plan) > 1)
            
            self.logger.info(f"✅ Engine coordination complete: {coordination_time_ms:.1f}ms")
            return all_results
            
        except Exception as e:
            self.logger.error(f"❌ Engine coordination failed: {e}")
            raise
    
    def _create_execution_plan(self, engine_names: List[str]) -> List[ExecutionPhase]:
        """
        Create execution plan with dependency-aware phases
        
        Engines with no dependencies can run in parallel in early phases.
        Dependent engines run in later phases after their dependencies complete.
        """
        # Filter to only requested engines
        available_engines = {name: self.engines[name] for name in engine_names if name in self.engines}
        
        if not available_engines:
            return []
        
        # Build dependency graph for requested engines
        engine_dependencies = {}
        for engine_name in available_engines.keys():
            deps = self.dependencies.get(engine_name, [])
            # Only include dependencies that are also being executed
            filtered_deps = [dep for dep in deps if dep in available_engines]
            engine_dependencies[engine_name] = filtered_deps
        
        # Create phases based on dependencies
        phases = []
        remaining_engines = set(available_engines.keys())
        phase_id = 0
        
        while remaining_engines:
            # Find engines with no remaining dependencies
            ready_engines = []
            for engine_name in remaining_engines:
                deps = engine_dependencies[engine_name]
                if all(dep not in remaining_engines for dep in deps):
                    ready_engines.append(engine_name)
            
            if not ready_engines:
                # Circular dependency or error - just take remaining engines
                ready_engines = list(remaining_engines)
                self.logger.warning(f"⚠️ Potential circular dependency, executing remaining engines: {ready_engines}")
            
            # Create phase
            phase_engines = {
                name: {'engine': available_engines[name], 'config': {}}
                for name in ready_engines
            }
            
            phases.append(ExecutionPhase(
                phase_id=phase_id,
                engines=phase_engines,
                dependencies=list(range(phase_id))  # Depends on all previous phases
            ))
            
            # Remove from remaining
            remaining_engines -= set(ready_engines)
            phase_id += 1
        
        self.logger.info(f"📋 Created execution plan with {len(phases)} phases")
        for i, phase in enumerate(phases):
            self.logger.info(f"   Phase {i}: {list(phase.engines.keys())}")
        
        return phases
    
    async def _execute_phase(self, phase: ExecutionPhase, data: Dict[str, Any], 
                           session_id: Optional[str], previous_results: Dict[str, EngineResult]) -> Dict[str, EngineResult]:
        """Execute all engines in a phase in parallel"""
        
        self.logger.info(f"⚡ Executing phase {phase.phase_id} with {len(phase.engines)} engines")
        
        # Create tasks for parallel execution
        tasks = []
        engine_names = []
        
        for engine_name, engine_config in phase.engines.items():
            task = self._execute_single_engine(
                engine_name, 
                engine_config['engine'], 
                data, 
                session_id, 
                previous_results
            )
            tasks.append(task)
            engine_names.append(engine_name)
        
        # Execute all engines in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        phase_results = {}
        for i, result in enumerate(results):
            engine_name = engine_names[i]
            if isinstance(result, Exception):
                self.logger.error(f"❌ Engine {engine_name} failed: {result}")
                phase_results[engine_name] = EngineResult(
                    engine_name=engine_name,
                    success=False,
                    result=None,
                    processing_time_ms=0.0,
                    error=str(result)
                )
            else:
                phase_results[engine_name] = result
        
        return phase_results
    
    async def _execute_single_engine(self, engine_name: str, engine: Any, data: Dict[str, Any], 
                                   session_id: Optional[str], previous_results: Dict[str, EngineResult]) -> EngineResult:
        """Execute a single engine with appropriate method call"""
        
        start_time = datetime.now()
        
        try:
            self.logger.debug(f"🔧 Executing {engine_name} engine")
            
            # Route to appropriate engine method based on engine type and data
            result = await self._route_engine_call(engine_name, engine, data, session_id, previous_results)
            
            processing_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            return EngineResult(
                engine_name=engine_name,
                success=True,
                result=result,
                processing_time_ms=processing_time_ms
            )
            
        except Exception as e:
            processing_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            self.logger.error(f"❌ Engine {engine_name} execution failed: {e}")
            
            return EngineResult(
                engine_name=engine_name,
                success=False,
                result=None,
                processing_time_ms=processing_time_ms,
                error=str(e)
            )
    
    async def _route_engine_call(self, engine_name: str, engine: Any, data: Dict[str, Any], 
                               session_id: Optional[str], previous_results: Dict[str, EngineResult]) -> Any:
        """Route to appropriate engine method based on engine type and data"""
        
        # Cross-platform intelligence
        if engine_name == 'cross_platform':
            platform_signals = data.get('platform_signals', {})
            return await engine.synthesize_cross_platform_intelligence(platform_signals)
        
        # Multimodal fusion
        elif engine_name == 'fusion':
            if 'signal' in data:
                return await engine.process_multimodal_signal(data['signal'])
            else:
                # Create a basic signal from data
                from src.api.domains.intelligence.services.multimodal_fusion_engine import MultiModalSignal, SignalType
                signal = MultiModalSignal(
                    signal_id=f"orchestrated_{datetime.now().timestamp()}",
                    timestamp=datetime.now(),
                    source_platform=data.get('source_platform', 'orchestrator'),
                    signal_type=SignalType.TEXT,
                    content=str(data.get('content', ''))
                )
                return await engine.process_multimodal_signal(signal)
        
        # Semantic analysis
        elif engine_name == 'semantic':
            content = data.get('content', '')
            context = data.get('context', {})
            return await engine.analyze_semantic_understanding(content, context)
        
        # Real-time dialectical
        elif engine_name == 'dialectical':
            query = data.get('query', '')
            force_context = data.get('force_context')
            if session_id:
                return await engine.real_time_synthesis(query, session_id, force_context)
            else:
                # Create temporary session
                temp_session = await engine.create_session()
                return await engine.real_time_synthesis(query, temp_session, force_context)
        
        # Temporal pattern analysis
        elif engine_name == 'temporal':
            signals = data.get('signals', [])
            timeframe_hours = data.get('timeframe_hours', 168)
            return await engine.analyze_temporal_patterns(signals, timeframe_hours)
        
        # Contextual source intelligence
        elif engine_name == 'contextual':
            query = data.get('query', '')
            from src.api.domains.intelligence.services.contextual_source_intelligence import QueryContext
            context = data.get('context', 'general')  # Use string instead of enum
            return await engine.determine_optimal_sources(query, context)
        
        else:
            raise ValueError(f"Unknown engine type: {engine_name}")
    
    def _update_coordination_stats(self, coordination_time_ms: float, engines_count: int, parallel_execution: bool):
        """Update coordination performance statistics"""
        self.coordination_stats['executions_coordinated'] += 1
        
        if parallel_execution:
            self.coordination_stats['parallel_executions'] += 1
        
        # Update average coordination time
        current_avg = self.coordination_stats['avg_coordination_time_ms']
        executions = self.coordination_stats['executions_coordinated']
        new_avg = ((current_avg * (executions - 1)) + coordination_time_ms) / executions
        self.coordination_stats['avg_coordination_time_ms'] = new_avg
    
    def get_coordination_stats(self) -> Dict[str, Any]:
        """Get coordination performance statistics"""
        return {
            'coordination_stats': self.coordination_stats.copy(),
            'available_engines': list(self.engines.keys()),
            'dependency_graph': self.dependencies.copy(),
            'timestamp': datetime.now().isoformat()
        } 