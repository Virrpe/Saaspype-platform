#!/usr/bin/env python3
"""
Discovery Models - Data structures for enhanced pain point discovery
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DiscoveryRequest:
    """Request model for discovery operations"""
    source: str
    query: str
    limit: int = 10
    hours_back: int = 24
    enhanced_analysis: bool = True
    
@dataclass
class PainPoint:
    """Individual pain point discovered from content"""
    title: str
    description: str
    source: str
    url: str
    market_size_score: int
    urgency_score: int
    solution_gap_score: int
    monetization_score: int
    total_score: float
    confidence: float
    industry: str
    pain_indicators: List[str]
    reddit_metrics: Dict[str, Any]
    timestamp: datetime

@dataclass
class BusinessOpportunity:
    """Business opportunity derived from pain points"""
    title: str
    description: str
    domain: str
    target_market: str
    market_size: int
    urgency: int
    solution_gap: int
    monetization: int
    score: float
    confidence: float
    reddit_metrics: Dict[str, Any]
    validation_signals: List[str]
    timestamp: datetime

@dataclass
class DiscoveryResponse:
    """Response model for discovery operations"""
    success: bool
    message: str
    pain_points: List[PainPoint]
    ranked_opportunities: List[BusinessOpportunity]
    metadata: Dict[str, Any]
    timestamp: datetime 