"""
Luciq Phase 5: Multi-Modal Signal Fusion Engine
Revolutionary multi-modal signal integration with real-time broadcasting
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import numpy as np
from collections import defaultdict, deque
import logging
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SignalType(Enum):
    TEXT = "text"
    NETWORK = "network" 
    TEMPORAL = "temporal"
    BEHAVIORAL = "behavioral"
    SEMANTIC = "semantic"

@dataclass
class MultiModalSignal:
    """Unified signal structure for multi-modal fusion"""
    signal_id: str
    timestamp: datetime
    source_platform: str
    signal_type: SignalType
    content: str
    
    # Text modality
    semantic_score: float = 0.0
    sentiment_score: float = 0.0
    context_relevance: float = 0.0
    
    # Network modality
    influence_score: float = 0.0
    viral_potential: float = 0.0
    network_centrality: float = 0.0
    
    # Temporal modality
    velocity: float = 0.0
    acceleration: float = 0.0
    trend_strength: float = 0.0
    
    # Behavioral modality
    engagement_rate: float = 0.0
    user_quality: float = 0.0
    authenticity_score: float = 0.0
    
    # Fusion results
    fusion_score: float = 0.0
    confidence_level: float = 0.0
    cross_modal_correlations: Dict[str, float] = None
    
    def __post_init__(self):
        if self.cross_modal_correlations is None:
            self.cross_modal_correlations = {}

class MultiModalFusionEngine:
    """
    Phase 5: Revolutionary Multi-Modal Signal Fusion Engine
    
    Combines signals from multiple modalities:
    - Text/Semantic: NLP analysis, sentiment, context
    - Network: Graph analysis, influence, viral potential  
    - Temporal: Time series patterns, velocity, acceleration
    - Behavioral: User engagement, authenticity, quality
    
    Features:
    - Real-time fusion with adaptive weights
    - Cross-modal correlation detection
    - WebSocket broadcasting
    - Confidence estimation
    - Pattern emergence detection
    """
    
    def __init__(self):
        self.fusion_weights = {
            SignalType.TEXT: 0.25,
            SignalType.NETWORK: 0.25, 
            SignalType.TEMPORAL: 0.25,
            SignalType.BEHAVIORAL: 0.25
        }
        
        # Real-time signal buffers (sliding windows)
        self.signal_buffer = defaultdict(lambda: deque(maxlen=1000))
        self.fusion_history = deque(maxlen=5000)
        
        # Cross-modal correlation tracking
        self.correlation_matrix = defaultdict(lambda: defaultdict(float))
        self.correlation_history = deque(maxlen=1000)
        
        # WebSocket broadcasting
        self.websocket_clients = set()
        self.broadcast_queue = asyncio.Queue(maxsize=10000)
        
        # Performance metrics
        self.fusion_stats = {
            'signals_processed': 0,
            'fusion_operations': 0,
            'correlations_detected': 0,
            'patterns_emerged': 0,
            'average_fusion_time': 0.0,
            'confidence_distribution': defaultdict(int)
        }
        
        # Adaptive learning
        self.pattern_templates = {}
        self.emergence_thresholds = {
            'fusion_score': 0.75,
            'correlation_strength': 0.6,
            'confidence_level': 0.8,
            'cross_modal_agreement': 0.7
        }
        
        logger.info("Phase 5 Multi-Modal Fusion Engine initialized")
    
    async def process_multimodal_signal(self, signal: MultiModalSignal) -> Dict[str, Any]:
        """
        Process a signal through multi-modal fusion
        
        Returns fusion results with cross-modal analysis
        """
        start_time = time.time()
        
        try:
            # Step 1: Store signal in appropriate buffer
            self.signal_buffer[signal.signal_type].append(signal)
            
            # Step 2: Perform multi-modal fusion
            fusion_result = await self._perform_fusion(signal)
            
            # Step 3: Detect cross-modal correlations
            correlations = await self._detect_cross_modal_correlations(signal)
            
            # Step 4: Calculate confidence and emergence probability
            confidence = self._calculate_confidence(fusion_result, correlations)
            emergence_prob = self._detect_pattern_emergence(fusion_result)
            
            # Step 5: Update signal with fusion results
            signal.fusion_score = fusion_result['fusion_score']
            signal.confidence_level = confidence
            signal.cross_modal_correlations = correlations
            
            # Step 6: Store in fusion history
            fusion_record = {
                'timestamp': signal.timestamp,
                'signal_id': signal.signal_id,
                'signal_type': signal.signal_type.value,
                'fusion_score': fusion_result['fusion_score'],
                'confidence': confidence,
                'correlations': correlations,
                'emergence_probability': emergence_prob,
                'processing_time': time.time() - start_time
            }
            
            self.fusion_history.append(fusion_record)
            
            # Step 7: Broadcast to WebSocket clients
            await self._broadcast_fusion_result(fusion_record)
            
            # Step 8: Update statistics
            self._update_fusion_stats(time.time() - start_time, confidence)
            
            return {
                'signal': asdict(signal),
                'fusion_result': fusion_result,
                'correlations': correlations,
                'confidence': confidence,
                'emergence_probability': emergence_prob,
                'processing_time': time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Multi-modal fusion error: {str(e)}")
            return {'error': str(e), 'signal_id': signal.signal_id}
    
    async def _perform_fusion(self, signal: MultiModalSignal) -> Dict[str, Any]:
        """Perform multi-modal signal fusion"""
        
        # Extract modality scores
        modality_scores = {
            SignalType.TEXT: self._calculate_text_score(signal),
            SignalType.NETWORK: self._calculate_network_score(signal),
            SignalType.TEMPORAL: self._calculate_temporal_score(signal),
            SignalType.BEHAVIORAL: self._calculate_behavioral_score(signal)
        }
        
        # Apply adaptive weights
        weighted_scores = {}
        for modality, score in modality_scores.items():
            weight = self._get_adaptive_weight(modality, signal)
            weighted_scores[modality.value] = score * weight
        
        # Calculate fusion score
        fusion_score = sum(weighted_scores.values())
        
        # Detect fusion patterns
        fusion_patterns = self._detect_fusion_patterns(modality_scores)
        
        return {
            'fusion_score': fusion_score,
            'modality_scores': {k.value: v for k, v in modality_scores.items()},
            'weighted_scores': weighted_scores,
            'fusion_patterns': fusion_patterns,
            'dominant_modality': max(modality_scores.items(), key=lambda x: x[1])[0].value
        }
    
    def _calculate_text_score(self, signal: MultiModalSignal) -> float:
        """Calculate text/semantic modality score"""
        return np.mean([
            signal.semantic_score,
            signal.sentiment_score,
            signal.context_relevance
        ])
    
    def _calculate_network_score(self, signal: MultiModalSignal) -> float:
        """Calculate network modality score"""
        return np.mean([
            signal.influence_score,
            signal.viral_potential,
            signal.network_centrality
        ])
    
    def _calculate_temporal_score(self, signal: MultiModalSignal) -> float:
        """Calculate temporal modality score"""
        return np.mean([
            signal.velocity,
            signal.acceleration,
            signal.trend_strength
        ])
    
    def _calculate_behavioral_score(self, signal: MultiModalSignal) -> float:
        """Calculate behavioral modality score"""
        return np.mean([
            signal.engagement_rate,
            signal.user_quality,
            signal.authenticity_score
        ])
    
    def _get_adaptive_weight(self, modality: SignalType, signal: MultiModalSignal) -> float:
        """Get adaptive weight based on recent performance"""
        
        # Base weight
        base_weight = self.fusion_weights[modality]
        
        # Adjust based on recent correlation strength
        recent_correlations = []
        correlation_history_list = list(self.correlation_history)
        if len(correlation_history_list) > 0:
            # Get last 100 records or all if less than 100
            recent_records = correlation_history_list[-100:] if len(correlation_history_list) >= 100 else correlation_history_list
            
            for record in recent_records:
                if modality.value in record.get('correlations', {}):
                    recent_correlations.append(record['correlations'][modality.value])
        
        if recent_correlations:
            avg_correlation = np.mean(recent_correlations)
            # Boost weight for highly correlated modalities
            weight_adjustment = (avg_correlation - 0.5) * 0.3
            return min(max(base_weight + weight_adjustment, 0.1), 0.6)
        
        return base_weight
    
    async def _detect_cross_modal_correlations(self, signal: MultiModalSignal) -> Dict[str, float]:
        """Detect correlations between different modalities"""
        
        correlations = {}
        
        # Get recent signals from different modalities
        for modality_type in SignalType:
            if modality_type == signal.signal_type:
                continue
                
            recent_signals = list(self.signal_buffer[modality_type])[-10:]
            if not recent_signals:
                continue
            
            # Calculate correlation with current signal
            correlation = self._calculate_signal_correlation(signal, recent_signals)
            correlations[modality_type.value] = correlation
        
        # Update correlation matrix
        for modality, correlation in correlations.items():
            self.correlation_matrix[signal.signal_type.value][modality] = correlation
        
        return correlations
    
    def _calculate_signal_correlation(self, current_signal: MultiModalSignal, 
                                   recent_signals: List[MultiModalSignal]) -> float:
        """Calculate correlation between current signal and recent signals"""
        
        if not recent_signals:
            return 0.0
        
        # Simple correlation based on content similarity and timing
        content_similarity = self._calculate_content_similarity(
            current_signal.content, [s.content for s in recent_signals]
        )
        
        # Temporal proximity factor
        time_weights = []
        for recent_signal in recent_signals:
            time_diff = abs((current_signal.timestamp - recent_signal.timestamp).total_seconds())
            time_weight = max(0, 1 - (time_diff / 3600))  # 1-hour decay
            time_weights.append(time_weight)
        
        if not time_weights:
            return content_similarity
        
        # Weighted correlation
        weighted_correlation = content_similarity * np.mean(time_weights)
        return min(weighted_correlation, 1.0)
    
    def _calculate_content_similarity(self, content: str, other_contents: List[str]) -> float:
        """Calculate content similarity (simplified implementation)"""
        
        # Convert to lowercase and tokenize
        tokens = set(content.lower().split())
        
        similarities = []
        for other_content in other_contents:
            other_tokens = set(other_content.lower().split())
            
            # Jaccard similarity
            intersection = len(tokens & other_tokens)
            union = len(tokens | other_tokens)
            
            if union == 0:
                similarity = 0.0
            else:
                similarity = intersection / union
            
            similarities.append(similarity)
        
        return np.mean(similarities) if similarities else 0.0
    
    def _detect_fusion_patterns(self, modality_scores: Dict[SignalType, float]) -> List[str]:
        """Detect patterns in multi-modal fusion"""
        
        patterns = []
        
        # Dominant modality pattern
        max_score = max(modality_scores.values())
        dominant_modalities = [
            modality for modality, score in modality_scores.items() 
            if score == max_score
        ]
        
        if len(dominant_modalities) == 1:
            patterns.append(f"dominant_{dominant_modalities[0].value}")
        elif len(dominant_modalities) > 1:
            patterns.append("multi_modal_dominance")
        
        # High correlation pattern
        avg_score = np.mean(list(modality_scores.values()))
        if avg_score > 0.7:
            patterns.append("high_consensus")
        elif avg_score < 0.3:
            patterns.append("low_consensus")
        
        # Balanced pattern
        score_variance = np.var(list(modality_scores.values()))
        if score_variance < 0.1:
            patterns.append("balanced_fusion")
        
        return patterns
    
    def _calculate_confidence(self, fusion_result: Dict[str, Any], 
                            correlations: Dict[str, float]) -> float:
        """Calculate confidence in fusion result"""
        
        # Base confidence from fusion score
        fusion_confidence = min(fusion_result['fusion_score'], 1.0)
        
        # Cross-modal agreement factor
        if correlations:
            correlation_confidence = np.mean(list(correlations.values()))
        else:
            correlation_confidence = 0.5
        
        # Pattern consistency factor
        pattern_confidence = len(fusion_result['fusion_patterns']) * 0.1
        
        # Combined confidence
        confidence = np.mean([
            fusion_confidence * 0.5,
            correlation_confidence * 0.3,
            pattern_confidence * 0.2
        ])
        
        return min(confidence, 1.0)
    
    def _detect_pattern_emergence(self, fusion_result: Dict[str, Any]) -> float:
        """Detect probability of pattern emergence"""
        
        # Check recent fusion history for emergence indicators
        recent_fusions = list(self.fusion_history)[-20:]
        
        if len(recent_fusions) < 5:
            return 0.0
        
        # Rising fusion scores
        recent_scores = [f['fusion_score'] for f in recent_fusions]
        score_trend = np.polyfit(range(len(recent_scores)), recent_scores, 1)[0]
        
        # Increasing correlations
        recent_correlations = []
        for fusion in recent_fusions:
            if fusion.get('correlations'):
                recent_correlations.append(np.mean(list(fusion['correlations'].values())))
        
        correlation_trend = 0.0
        if len(recent_correlations) >= 2:
            correlation_trend = np.polyfit(range(len(recent_correlations)), recent_correlations, 1)[0]
        
        # Pattern consistency
        pattern_consistency = 0.0
        if 'fusion_patterns' in fusion_result:
            recent_patterns = []
            for fusion in recent_fusions:
                if 'fusion_patterns' in fusion:
                    recent_patterns.extend(fusion['fusion_patterns'])
            
            if recent_patterns:
                unique_patterns = set(recent_patterns)
                pattern_consistency = len(recent_patterns) / len(unique_patterns) / 10
        
        # Emergence probability
        emergence_prob = np.mean([
            max(score_trend, 0) * 0.4,
            max(correlation_trend, 0) * 0.4,
            pattern_consistency * 0.2
        ])
        
        return min(emergence_prob, 1.0)
    
    async def _broadcast_fusion_result(self, fusion_record: Dict[str, Any]):
        """Broadcast fusion result to WebSocket clients"""
        
        if not self.websocket_clients:
            return
        
        broadcast_data = {
            'type': 'multimodal_fusion',
            'timestamp': fusion_record['timestamp'].isoformat(),
            'fusion_score': fusion_record['fusion_score'],
            'confidence': fusion_record['confidence'],
            'correlations': fusion_record['correlations'],
            'emergence_probability': fusion_record['emergence_probability']
        }
        
        # Add to broadcast queue
        try:
            await self.broadcast_queue.put(broadcast_data)
        except asyncio.QueueFull:
            logger.warning("Broadcast queue full, dropping fusion result")
    
    def _update_fusion_stats(self, processing_time: float, confidence: float):
        """Update fusion statistics"""
        
        self.fusion_stats['signals_processed'] += 1
        self.fusion_stats['fusion_operations'] += 1
        
        # Update average processing time
        current_avg = self.fusion_stats['average_fusion_time']
        operations = self.fusion_stats['fusion_operations']
        self.fusion_stats['average_fusion_time'] = (
            (current_avg * (operations - 1) + processing_time) / operations
        )
        
        # Update confidence distribution
        confidence_bucket = int(confidence * 10) * 10
        self.fusion_stats['confidence_distribution'][confidence_bucket] += 1
    
    async def add_websocket_client(self, websocket):
        """Add WebSocket client for broadcasting"""
        self.websocket_clients.add(websocket)
        logger.info(f"WebSocket client added. Total clients: {len(self.websocket_clients)}")
    
    async def remove_websocket_client(self, websocket):
        """Remove WebSocket client"""
        self.websocket_clients.discard(websocket)
        logger.info(f"WebSocket client removed. Total clients: {len(self.websocket_clients)}")
    
    def get_fusion_statistics(self) -> Dict[str, Any]:
        """Get comprehensive fusion statistics"""
        
        recent_fusions = list(self.fusion_history)[-100:]
        
        stats = {
            'overview': dict(self.fusion_stats),
            'recent_performance': {
                'avg_fusion_score': np.mean([f['fusion_score'] for f in recent_fusions]) if recent_fusions else 0,
                'avg_confidence': np.mean([f['confidence'] for f in recent_fusions]) if recent_fusions else 0,
                'avg_emergence_prob': np.mean([f['emergence_probability'] for f in recent_fusions]) if recent_fusions else 0,
                'recent_patterns': len(set([p for f in recent_fusions for p in f.get('fusion_patterns', [])]))
            },
            'modality_distribution': {
                modality.value: len(self.signal_buffer[modality]) 
                for modality in SignalType
            },
            'correlation_matrix': dict(self.correlation_matrix),
            'websocket_clients': len(self.websocket_clients),
            'fusion_weights': {k.value: v for k, v in self.fusion_weights.items()}
        }
        
        return stats

# Global fusion engine instance
fusion_engine = MultiModalFusionEngine() 