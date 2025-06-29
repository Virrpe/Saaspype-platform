#!/usr/bin/env python3
"""
Request Router - Intelligent Engine Selection
Routes requests to appropriate engines based on analysis type and data characteristics
"""

import logging
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class RoutingRule:
    """Rule for routing requests to engines"""
    request_pattern: str
    primary_engines: List[str]
    supporting_engines: List[str]
    conditions: Dict[str, Any]
    priority: int = 0

class RequestRouter:
    """
    Routes requests to appropriate engines based on analysis type
    
    Features:
    - Pattern-based routing
    - Data-driven engine selection
    - Load balancing considerations
    - Performance optimization
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Define routing rules
        self.routing_rules = self._initialize_routing_rules()
        
        # Performance tracking
        self.routing_stats = {
            'requests_routed': 0,
            'routing_decisions': {},
            'engine_usage': {},
            'avg_engines_per_request': 0.0
        }
    
    def _initialize_routing_rules(self) -> List[RoutingRule]:
        """Initialize routing rules for different request types"""
        
        return [
            # Cross-platform analysis
            RoutingRule(
                request_pattern='cross_platform_analysis',
                primary_engines=['cross_platform'],
                supporting_engines=['semantic', 'temporal'],
                conditions={'requires_platform_data': True},
                priority=1
            ),
            
            # Real-time synthesis
            RoutingRule(
                request_pattern='real_time_synthesis',
                primary_engines=['dialectical', 'fusion'],
                supporting_engines=['semantic'],
                conditions={'requires_session': True},
                priority=1
            ),
            
            # Trend prediction
            RoutingRule(
                request_pattern='trend_prediction',
                primary_engines=['temporal'],
                supporting_engines=['cross_platform', 'semantic'],
                conditions={'requires_time_series': True},
                priority=1
            ),
            
            # Semantic analysis
            RoutingRule(
                request_pattern='semantic_analysis',
                primary_engines=['semantic'],
                supporting_engines=['contextual'],
                conditions={'requires_text_content': True},
                priority=1
            ),
            
            # Multimodal fusion
            RoutingRule(
                request_pattern='fusion_analysis',
                primary_engines=['fusion'],
                supporting_engines=['semantic', 'temporal'],
                conditions={'requires_signal_data': True},
                priority=1
            ),
            
            # Temporal analysis
            RoutingRule(
                request_pattern='temporal_analysis',
                primary_engines=['temporal'],
                supporting_engines=['semantic'],
                conditions={'requires_time_series': True},
                priority=1
            ),
            
            # Contextual intelligence
            RoutingRule(
                request_pattern='contextual_analysis',
                primary_engines=['contextual'],
                supporting_engines=['semantic'],
                conditions={'requires_query': True},
                priority=1
            ),
            
            # Full intelligence (comprehensive analysis)
            RoutingRule(
                request_pattern='full_intelligence',
                primary_engines=['cross_platform', 'fusion', 'semantic'],
                supporting_engines=['dialectical', 'temporal', 'contextual'],
                conditions={},
                priority=0
            ),
            
            # Discovery analysis
            RoutingRule(
                request_pattern='discovery_analysis',
                primary_engines=['semantic', 'cross_platform'],
                supporting_engines=['temporal', 'contextual'],
                conditions={'requires_discovery_data': True},
                priority=1
            ),
            
            # Quality analysis
            RoutingRule(
                request_pattern='quality_analysis',
                primary_engines=['semantic', 'fusion'],
                supporting_engines=['temporal'],
                conditions={'requires_quality_metrics': True},
                priority=1
            ),
            
            # Performance analysis
            RoutingRule(
                request_pattern='performance_analysis',
                primary_engines=['temporal', 'fusion'],
                supporting_engines=['semantic'],
                conditions={'requires_performance_data': True},
                priority=1
            ),
            
            # Business idea generation
            RoutingRule(
                request_pattern='business_idea_generation',
                primary_engines=['semantic', 'cross_platform'],
                supporting_engines=['contextual', 'fusion'],
                conditions={'requires_idea_generation': True},
                priority=1
            )
        ]
    
    def determine_engines(self, request_type: str, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Determine which engines to use for optimal analysis
        
        Args:
            request_type: Type of analysis requested
            data: Input data for analysis
            
        Returns:
            Dictionary with 'primary' and 'supporting' engine lists
        """
        
        try:
            self.logger.debug(f"🎯 Routing request type: {request_type}")
            
            # Find matching routing rule
            matching_rule = self._find_matching_rule(request_type, data)
            
            if matching_rule:
                # Validate engines are available for the data
                validated_config = self._validate_engine_requirements(matching_rule, data)
                
                # Update routing stats
                self._update_routing_stats(request_type, validated_config)
                
                self.logger.info(f"✅ Routed to engines - Primary: {validated_config['primary']}, Supporting: {validated_config['supporting']}")
                return validated_config
            
            else:
                # Fallback to intelligent analysis based on data characteristics
                fallback_config = self._intelligent_fallback_routing(request_type, data)
                
                self._update_routing_stats(request_type, fallback_config)
                
                self.logger.info(f"🔄 Fallback routing - Primary: {fallback_config['primary']}, Supporting: {fallback_config['supporting']}")
                return fallback_config
                
        except Exception as e:
            self.logger.error(f"❌ Routing failed: {e}")
            # Emergency fallback - use semantic engine only
            return {
                'primary': ['semantic'],
                'supporting': []
            }
    
    def _find_matching_rule(self, request_type: str, data: Dict[str, Any]) -> RoutingRule:
        """Find the best matching routing rule for the request"""
        
        # Look for exact pattern match first
        exact_matches = [rule for rule in self.routing_rules if rule.request_pattern == request_type]
        
        if exact_matches:
            # Return highest priority exact match
            return max(exact_matches, key=lambda r: r.priority)
        
        # Look for partial pattern matches
        partial_matches = [rule for rule in self.routing_rules if request_type in rule.request_pattern or rule.request_pattern in request_type]
        
        if partial_matches:
            return max(partial_matches, key=lambda r: r.priority)
        
        # No matches found
        return None
    
    def _validate_engine_requirements(self, rule: RoutingRule, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate that engines can handle the provided data"""
        
        primary_engines = rule.primary_engines.copy()
        supporting_engines = rule.supporting_engines.copy()
        
        # Check conditions
        for condition, required in rule.conditions.items():
            if required and not self._check_condition(condition, data):
                self.logger.warning(f"⚠️ Condition not met: {condition}")
                # Remove engines that require this condition
                if condition == 'requires_platform_data':
                    primary_engines = [e for e in primary_engines if e != 'cross_platform']
                elif condition == 'requires_session':
                    primary_engines = [e for e in primary_engines if e != 'dialectical']
                elif condition == 'requires_time_series':
                    primary_engines = [e for e in primary_engines if e != 'temporal']
                elif condition == 'requires_text_content':
                    primary_engines = [e for e in primary_engines if e != 'semantic']
                elif condition == 'requires_signal_data':
                    primary_engines = [e for e in primary_engines if e != 'fusion']
        
        # Ensure at least one primary engine
        if not primary_engines:
            primary_engines = ['semantic']  # Fallback to semantic
        
        return {
            'primary': primary_engines,
            'supporting': supporting_engines
        }
    
    def _check_condition(self, condition: str, data: Dict[str, Any]) -> bool:
        """Check if a routing condition is met by the data"""
        
        if condition == 'requires_platform_data':
            return 'platform_signals' in data or 'platforms' in data
        
        elif condition == 'requires_session':
            return 'session_id' in data or 'query' in data
        
        elif condition == 'requires_time_series':
            return 'signals' in data or 'timeframe_hours' in data or 'temporal_data' in data
        
        elif condition == 'requires_text_content':
            return 'content' in data or 'text' in data or 'query' in data
        
        elif condition == 'requires_signal_data':
            return 'signal' in data or 'signals' in data or 'multimodal_data' in data
        
        elif condition == 'requires_query':
            return 'query' in data or 'question' in data
        
        elif condition == 'requires_discovery_data':
            return 'discovery' in data or 'opportunities' in data or 'pain_points' in data
        
        elif condition == 'requires_quality_metrics':
            return 'quality' in data or 'metrics' in data or 'scores' in data
        
        elif condition == 'requires_performance_data':
            return 'performance' in data or 'metrics' in data or 'benchmarks' in data
        
        elif condition == 'requires_idea_generation':
            return 'content' in data or 'focus' in data or 'target_market' in data or 'analysis_depth' in data
        
        else:
            return True  # Unknown condition, assume met
    
    def _intelligent_fallback_routing(self, request_type: str, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Intelligent fallback routing based on data characteristics"""
        
        primary_engines = []
        supporting_engines = []
        
        # Analyze data characteristics
        has_text = any(key in data for key in ['content', 'text', 'query', 'description'])
        has_temporal = any(key in data for key in ['signals', 'timeframe', 'temporal_data', 'timestamps'])
        has_platforms = any(key in data for key in ['platform_signals', 'platforms', 'sources'])
        has_session = 'session_id' in data
        has_multimodal = any(key in data for key in ['signal', 'multimodal_data', 'fusion_data'])
        
        # Route based on data characteristics
        if has_text:
            primary_engines.append('semantic')
        
        if has_temporal:
            primary_engines.append('temporal')
        
        if has_platforms:
            primary_engines.append('cross_platform')
        
        if has_multimodal:
            primary_engines.append('fusion')
        
        if has_session:
            supporting_engines.append('dialectical')
        
        # Add contextual as supporting if we have queries
        if has_text and any(key in data for key in ['query', 'question']):
            supporting_engines.append('contextual')
        
        # Fallback to semantic if no engines selected
        if not primary_engines:
            primary_engines = ['semantic']
        
        return {
            'primary': primary_engines,
            'supporting': supporting_engines
        }
    
    def _update_routing_stats(self, request_type: str, routing_config: Dict[str, List[str]]):
        """Update routing performance statistics"""
        
        self.routing_stats['requests_routed'] += 1
        
        # Track routing decisions
        if request_type not in self.routing_stats['routing_decisions']:
            self.routing_stats['routing_decisions'][request_type] = 0
        self.routing_stats['routing_decisions'][request_type] += 1
        
        # Track engine usage
        all_engines = routing_config['primary'] + routing_config['supporting']
        for engine in all_engines:
            if engine not in self.routing_stats['engine_usage']:
                self.routing_stats['engine_usage'][engine] = 0
            self.routing_stats['engine_usage'][engine] += 1
        
        # Update average engines per request
        total_engines = sum(len(routing_config['primary']) + len(routing_config['supporting']) 
                          for _ in range(self.routing_stats['requests_routed']))
        self.routing_stats['avg_engines_per_request'] = total_engines / self.routing_stats['requests_routed']
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get routing performance statistics"""
        return {
            'routing_stats': self.routing_stats.copy(),
            'available_rules': len(self.routing_rules),
            'rule_patterns': [rule.request_pattern for rule in self.routing_rules],
            'timestamp': datetime.now().isoformat()
        }
    
    def add_routing_rule(self, rule: RoutingRule):
        """Add a new routing rule"""
        self.routing_rules.append(rule)
        self.routing_rules.sort(key=lambda r: r.priority, reverse=True)
        self.logger.info(f"➕ Added routing rule: {rule.request_pattern}")
    
    def remove_routing_rule(self, pattern: str):
        """Remove routing rule by pattern"""
        self.routing_rules = [rule for rule in self.routing_rules if rule.request_pattern != pattern]
        self.logger.info(f"➖ Removed routing rule: {pattern}") 