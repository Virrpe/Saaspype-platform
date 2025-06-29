#!/usr/bin/env python3
"""
Real-Time Dialectical Synthesis Engine - Phase 2 Tactical Improvement
Provides live context switching and real-time synthesis updates with WebSocket streaming
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import json
from collections import defaultdict, deque
import time

# Import existing services
from .contextual_source_intelligence import (
    ContextualSourceIntelligenceEngine, QueryContext, DialecticalSourceMetrics
)
from ...streaming.services.websocket_broadcaster import websocket_broadcaster

logger = logging.getLogger(__name__)

@dataclass
class RealTimeContext:
    """Real-time context information with switching metadata"""
    context: QueryContext
    confidence: float
    detected_at: datetime
    context_features: Dict[str, float] = field(default_factory=dict)
    switch_reason: Optional[str] = None
    previous_context: Optional[QueryContext] = None

@dataclass
class RealTimeSynthesis:
    """Real-time synthesis result with streaming metadata"""
    query: str
    context: RealTimeContext
    selected_sources: List[Dict]
    synthesis_score: float
    processing_time_ms: float
    synthesis_metadata: Dict
    dialectical_metrics: List[DialecticalSourceMetrics]
    timestamp: datetime
    session_id: str

@dataclass
class SynthesisSession:
    """Session tracking for real-time synthesis"""
    session_id: str
    created_at: datetime
    last_activity: datetime
    query_history: List[str] = field(default_factory=list)
    context_history: List[RealTimeContext] = field(default_factory=list)
    synthesis_history: List[RealTimeSynthesis] = field(default_factory=list)
    performance_metrics: Dict = field(default_factory=dict)

class RealTimeDialecticalEngine:
    """
    Real-Time Dialectical Synthesis Engine - Phase 2 Enhancement
    
    Provides:
    - Live context switching with <100ms latency
    - Real-time synthesis streaming via WebSocket
    - Session-aware context memory
    - Performance monitoring and optimization
    - Context transition analytics
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Core dialectical engine (Phase 1)
        self.core_engine = ContextualSourceIntelligenceEngine()
        
        # Real-time session management
        self.active_sessions: Dict[str, SynthesisSession] = {}
        self.session_contexts: Dict[str, RealTimeContext] = {}
        
        # Real-time processing queues
        self.synthesis_queue = asyncio.Queue(maxsize=1000)
        self.context_switch_queue = asyncio.Queue(maxsize=500)
        
        # Performance monitoring
        self.performance_metrics = {
            'total_queries_processed': 0,
            'avg_processing_time_ms': 0,
            'context_switches_per_hour': 0,
            'synthesis_quality_trend': deque(maxlen=100),
            'processing_time_trend': deque(maxlen=100),
            'active_sessions_count': 0,
            'real_time_accuracy': 0.0
        }
        
        # Context detection enhancement
        self.context_detection_cache = {}
        self.context_switch_patterns = defaultdict(list)
        
        # Real-time processing task
        self.processing_task = None
        self.is_streaming = False
        
        self.logger.info("Real-Time Dialectical Engine initialized with Phase 1 integration")
    
    async def start_real_time_processing(self):
        """Start real-time processing and streaming"""
        
        if not self.is_streaming:
            self.is_streaming = True
            self.processing_task = asyncio.create_task(self._real_time_processor())
            self.logger.info("🚀 Real-time dialectical processing started")
    
    async def stop_real_time_processing(self):
        """Stop real-time processing"""
        
        self.is_streaming = False
        if self.processing_task:
            self.processing_task.cancel()
            try:
                await self.processing_task
            except asyncio.CancelledError:
                pass
        self.logger.info("⏹️ Real-time dialectical processing stopped")
    
    async def create_session(self, session_id: str = None) -> str:
        """Create a new real-time synthesis session"""
        
        if session_id is None:
            session_id = f"session_{int(time.time())}_{len(self.active_sessions)}"
        
        session = SynthesisSession(
            session_id=session_id,
            created_at=datetime.now(),
            last_activity=datetime.now()
        )
        
        self.active_sessions[session_id] = session
        self.performance_metrics['active_sessions_count'] = len(self.active_sessions)
        
        # Broadcast session creation
        await websocket_broadcaster.broadcast_fusion_result({
            "type": "session_created",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "status": "active"
        })
        
        self.logger.info(f"📊 Real-time session created: {session_id}")
        return session_id
    
    async def real_time_synthesis(self, query: str, session_id: str, 
                                force_context: QueryContext = None) -> RealTimeSynthesis:
        """
        Perform real-time dialectical synthesis with live context switching
        """
        
        start_time = time.time()
        
        # Ensure session exists
        if session_id not in self.active_sessions:
            await self.create_session(session_id)
        
        session = self.active_sessions[session_id]
        session.last_activity = datetime.now()
        session.query_history.append(query)
        
        # Phase 2 Enhancement: Real-time context detection with session awareness
        current_context = await self._real_time_context_detection(
            query, session_id, force_context
        )
        
        # Check for context switching
        previous_context = self.session_contexts.get(session_id)
        context_switched = (previous_context and 
                          previous_context.context != current_context.context)
        
        if context_switched:
            await self._handle_context_switch(session_id, previous_context, current_context)
        
        # Store current context
        self.session_contexts[session_id] = current_context
        session.context_history.append(current_context)
        
        # Perform dialectical synthesis (using Phase 1 engine)
        synthesis_result = await self.core_engine.determine_optimal_sources(
            query, current_context.context
        )
        
        # Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000
        
        # Create real-time synthesis result
        real_time_synthesis = RealTimeSynthesis(
            query=query,
            context=current_context,
            selected_sources=synthesis_result['selected_sources'],
            synthesis_score=synthesis_result['synthesis_metadata']['avg_synthesis_score'],
            processing_time_ms=processing_time_ms,
            synthesis_metadata=synthesis_result['synthesis_metadata'],
            dialectical_metrics=synthesis_result.get('dialectical_metrics', []),
            timestamp=datetime.now(),
            session_id=session_id
        )
        
        # Store in session
        session.synthesis_history.append(real_time_synthesis)
        
        # Update performance metrics
        await self._update_performance_metrics(real_time_synthesis, context_switched)
        
        # Stream result to WebSocket clients
        await self._stream_synthesis_result(real_time_synthesis, context_switched)
        
        self.logger.info(f"⚡ Real-time synthesis complete: {processing_time_ms:.1f}ms, "
                        f"context: {current_context.context.value}")
        
        return real_time_synthesis
    
    async def _real_time_context_detection(self, query: str, session_id: str, 
                                         force_context: QueryContext = None) -> RealTimeContext:
        """Enhanced real-time context detection with session awareness"""
        
        if force_context:
            return RealTimeContext(
                context=force_context,
                confidence=1.0,
                detected_at=datetime.now(),
                context_features={'forced': True}
            )
        
        # Check cache for similar queries
        cache_key = query.lower().strip()
        if cache_key in self.context_detection_cache:
            cached_result = self.context_detection_cache[cache_key]
            if (datetime.now() - cached_result['timestamp']).seconds < 300:  # 5 min cache
                return RealTimeContext(
                    context=cached_result['context'],
                    confidence=cached_result['confidence'],
                    detected_at=datetime.now(),
                    context_features={'cached': True}
                )
        
        # Use core engine for detection
        detected_context = await self.core_engine._detect_query_context(query)
        
        # Session-aware confidence calculation
        session = self.active_sessions.get(session_id)
        confidence = 0.8  # Base confidence
        
        if session and session.context_history:
            # Boost confidence if consistent with recent context
            recent_contexts = [ctx.context for ctx in session.context_history[-3:]]
            if detected_context in recent_contexts:
                confidence += 0.15
        
        # Context features for analysis
        context_features = {
            'query_length': len(query),
            'session_history_length': len(session.context_history) if session else 0,
            'detection_method': 'enhanced_real_time'
        }
        
        real_time_context = RealTimeContext(
            context=detected_context,
            confidence=min(1.0, confidence),
            detected_at=datetime.now(),
            context_features=context_features
        )
        
        # Cache result
        self.context_detection_cache[cache_key] = {
            'context': detected_context,
            'confidence': confidence,
            'timestamp': datetime.now()
        }
        
        return real_time_context
    
    async def _handle_context_switch(self, session_id: str, 
                                   previous_context: RealTimeContext,
                                   new_context: RealTimeContext):
        """Handle context switching with analytics and streaming"""
        
        # Analyze context switch
        switch_reason = self._analyze_context_switch(previous_context, new_context)
        new_context.switch_reason = switch_reason
        new_context.previous_context = previous_context.context
        
        # Track switch patterns
        switch_pattern = f"{previous_context.context.value} -> {new_context.context.value}"
        self.context_switch_patterns[switch_pattern].append(datetime.now())
        
        # Stream context switch notification
        await websocket_broadcaster.broadcast_fusion_result({
            "type": "context_switch",
            "session_id": session_id,
            "previous_context": previous_context.context.value,
            "new_context": new_context.context.value,
            "switch_reason": switch_reason,
            "confidence": new_context.confidence,
            "timestamp": datetime.now().isoformat(),
            "priority": "high"
        })
        
        self.logger.info(f"🔄 Context switch in session {session_id}: "
                        f"{previous_context.context.value} → {new_context.context.value} "
                        f"({switch_reason})")
    
    def _analyze_context_switch(self, previous: RealTimeContext, 
                               new: RealTimeContext) -> str:
        """Analyze why context switched"""
        
        confidence_diff = new.confidence - previous.confidence
        
        if confidence_diff > 0.2:
            return "high_confidence_detection"
        elif confidence_diff > 0.1:
            return "improved_context_match"
        elif (datetime.now() - previous.detected_at).seconds > 300:
            return "session_evolution"
        else:
            return "query_change_driven"
    
    async def _update_performance_metrics(self, synthesis: RealTimeSynthesis, 
                                        context_switched: bool):
        """Update real-time performance metrics"""
        
        self.performance_metrics['total_queries_processed'] += 1
        
        # Update processing time trend
        self.performance_metrics['processing_time_trend'].append(synthesis.processing_time_ms)
        avg_time = sum(self.performance_metrics['processing_time_trend']) / \
                  len(self.performance_metrics['processing_time_trend'])
        self.performance_metrics['avg_processing_time_ms'] = avg_time
        
        # Update synthesis quality trend
        self.performance_metrics['synthesis_quality_trend'].append(synthesis.synthesis_score)
        avg_quality = sum(self.performance_metrics['synthesis_quality_trend']) / \
                     len(self.performance_metrics['synthesis_quality_trend'])
        self.performance_metrics['real_time_accuracy'] = avg_quality
        
        # Context switch frequency
        if context_switched:
            current_hour = datetime.now().hour
            # This is simplified - in production we'd maintain hourly counters
            self.performance_metrics['context_switches_per_hour'] += 1
        
        # Active sessions
        self.performance_metrics['active_sessions_count'] = len(self.active_sessions)
    
    async def _stream_synthesis_result(self, synthesis: RealTimeSynthesis, 
                                     context_switched: bool):
        """Stream synthesis result to WebSocket clients"""
        
        # Main synthesis result
        synthesis_data = {
            "type": "real_time_synthesis",
            "session_id": synthesis.session_id,
            "query": synthesis.query,
            "context": {
                "type": synthesis.context.context.value,
                "confidence": synthesis.context.confidence,
                "switched": context_switched,
                "switch_reason": synthesis.context.switch_reason
            },
            "sources": synthesis.selected_sources,
            "synthesis_score": synthesis.synthesis_score,
            "processing_time_ms": synthesis.processing_time_ms,
            "timestamp": synthesis.timestamp.isoformat(),
            "performance": {
                "latency_target_met": synthesis.processing_time_ms < 100,
                "quality_score": synthesis.synthesis_score
            }
        }
        
        await websocket_broadcaster.broadcast_fusion_result(synthesis_data)
        
        # Performance metrics update
        performance_data = {
            "type": "performance_metrics",
            "metrics": self.performance_metrics.copy(),
            "timestamp": datetime.now().isoformat()
        }
        
        await websocket_broadcaster.broadcast_trend_update(performance_data)
    
    async def _real_time_processor(self):
        """Background processor for real-time tasks"""
        
        self.logger.info("🔄 Real-time dialectical processor started")
        
        while self.is_streaming:
            try:
                # Clean up old sessions (older than 1 hour)
                await self._cleanup_old_sessions()
                
                # Update context switch analytics
                await self._update_context_analytics()
                
                # Stream performance updates
                await self._stream_performance_updates()
                
                # Wait before next cycle
                await asyncio.sleep(10)  # Process every 10 seconds
                
            except Exception as e:
                self.logger.error(f"Real-time processor error: {e}")
                await asyncio.sleep(5)
    
    async def _cleanup_old_sessions(self):
        """Clean up inactive sessions"""
        
        cutoff_time = datetime.now() - timedelta(hours=1)
        expired_sessions = [
            session_id for session_id, session in self.active_sessions.items()
            if session.last_activity < cutoff_time
        ]
        
        for session_id in expired_sessions:
            del self.active_sessions[session_id]
            if session_id in self.session_contexts:
                del self.session_contexts[session_id]
            
            # Notify about session cleanup
            await websocket_broadcaster.broadcast_fusion_result({
                "type": "session_expired",
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            })
        
        if expired_sessions:
            self.performance_metrics['active_sessions_count'] = len(self.active_sessions)
            self.logger.info(f"🧹 Cleaned up {len(expired_sessions)} expired sessions")
    
    async def _update_context_analytics(self):
        """Update context switching analytics"""
        
        # Calculate context switch frequency
        recent_switches = 0
        cutoff_time = datetime.now() - timedelta(hours=1)
        
        for pattern, timestamps in self.context_switch_patterns.items():
            recent_switches += len([t for t in timestamps if t > cutoff_time])
        
        self.performance_metrics['context_switches_per_hour'] = recent_switches
    
    async def _stream_performance_updates(self):
        """Stream periodic performance updates"""
        
        performance_update = {
            "type": "system_performance",
            "real_time_engine": {
                "active_sessions": len(self.active_sessions),
                "avg_processing_time": self.performance_metrics['avg_processing_time_ms'],
                "synthesis_quality": self.performance_metrics['real_time_accuracy'],
                "context_switches_per_hour": self.performance_metrics['context_switches_per_hour'],
                "total_queries": self.performance_metrics['total_queries_processed']
            },
            "latency_performance": {
                "target_met_percentage": self._calculate_latency_success_rate(),
                "avg_processing_time": self.performance_metrics['avg_processing_time_ms']
            },
            "timestamp": datetime.now().isoformat()
        }
        
        await websocket_broadcaster.broadcast_trend_update(performance_update)
    
    def _calculate_latency_success_rate(self) -> float:
        """Calculate percentage of queries meeting <100ms target"""
        
        if not self.performance_metrics['processing_time_trend']:
            return 100.0
        
        under_target = sum(1 for time_ms in self.performance_metrics['processing_time_trend'] 
                          if time_ms < 100)
        total = len(self.performance_metrics['processing_time_trend'])
        
        return (under_target / total) * 100 if total > 0 else 100.0
    
    def get_session_analytics(self, session_id: str) -> Dict:
        """Get analytics for a specific session"""
        
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        
        return {
            "session_id": session_id,
            "created_at": session.created_at.isoformat(),
            "last_activity": session.last_activity.isoformat(),
            "queries_processed": len(session.query_history),
            "contexts_detected": len(set(ctx.context for ctx in session.context_history)),
            "context_switches": len([ctx for ctx in session.context_history if ctx.switch_reason]),
            "avg_synthesis_score": (
                sum(s.synthesis_score for s in session.synthesis_history) / 
                len(session.synthesis_history) if session.synthesis_history else 0.0
            ),
            "avg_processing_time": (
                sum(s.processing_time_ms for s in session.synthesis_history) / 
                len(session.synthesis_history) if session.synthesis_history else 0.0
            ),
            "context_distribution": {
                ctx.value: sum(1 for c in session.context_history if c.context == ctx)
                for ctx in set(c.context for c in session.context_history)
            }
        }
    
    def get_real_time_performance_report(self) -> Dict:
        """Get comprehensive real-time performance report"""
        
        return {
            "engine_status": {
                "streaming": self.is_streaming,
                "active_sessions": len(self.active_sessions),
                "total_queries_processed": self.performance_metrics['total_queries_processed']
            },
            "performance_metrics": self.performance_metrics.copy(),
            "latency_analysis": {
                "target_latency_ms": 100,
                "success_rate_percentage": self._calculate_latency_success_rate(),
                "avg_processing_time_ms": self.performance_metrics['avg_processing_time_ms']
            },
            "context_analytics": {
                "context_switches_per_hour": self.performance_metrics['context_switches_per_hour'],
                "switch_patterns": {
                    pattern: len(timestamps) 
                    for pattern, timestamps in self.context_switch_patterns.items()
                }
            },
            "session_summary": {
                "active_sessions": len(self.active_sessions),
                "session_ids": list(self.active_sessions.keys())
            }
        }

# Global instance for the application
real_time_engine = RealTimeDialecticalEngine()

# Factory function
def get_real_time_dialectical_engine() -> RealTimeDialecticalEngine:
    """Get the real-time dialectical engine instance"""
    return real_time_engine 