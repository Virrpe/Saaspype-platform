#!/usr/bin/env python3
"""
Intelligence Router - AI Analysis and Trend Detection Endpoints
Handles all intelligence, semantic analysis, and trend detection endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, BackgroundTasks
from typing import Optional, Dict, Any
import logging
import json

from src.api.domains.auth.endpoints.auth import get_current_user
from src.api.domains.discovery.models.requests import TrendDetectionRequest
from src.api.domains.streaming.services.trend_detection_service import CrossPlatformTrendDetector, TrendOpportunity
from src.api.domains.intelligence.services.market_intelligence_service import RealTimeMarketIntelligence
from src.api.domains.intelligence.services.semantic_analysis_engine import get_semantic_engine
from src.api.domains.streaming.services.temporal_pattern_engine import get_temporal_engine
from src.api.domains.streaming.services.semantic_trend_integration import get_semantic_trend_integration_engine
from src.api.domains.streaming.services.graph_trend_detector import GroundbreakingGraphTrendDetector

logger = logging.getLogger(__name__)

# Create router with intelligence prefix
router = APIRouter(prefix="/api", tags=["Intelligence & Trends"])

# Global instances (lazy-loaded)
_trend_detector = None
_market_intelligence = None

def get_trend_detector():
    """Get or create trend detector instance"""
    global _trend_detector
    if _trend_detector is None:
        _trend_detector = CrossPlatformTrendDetector()
    return _trend_detector

def get_market_intelligence():
    """Get or create market intelligence instance"""
    global _market_intelligence
    if _market_intelligence is None:
        _market_intelligence = RealTimeMarketIntelligence()
    return _market_intelligence

@router.get("/trends")
async def get_trends(
    limit_sessions: int = 50,
    include_predictions: bool = True,
    include_alerts: bool = True,
    current_user: dict = Depends(get_current_user)
):
    """Get trend analysis with predictions and alerts"""
    try:
        trend_detector = get_trend_detector()
        
        # Get trend data
        trends = await trend_detector.get_trends(
            limit=limit_sessions,
            include_predictions=include_predictions,
            include_alerts=include_alerts
        )
        
        return {
            "trends": trends,
            "metadata": {
                "limit_sessions": limit_sessions,
                "include_predictions": include_predictions,
                "include_alerts": include_alerts,
                "user_id": current_user["user_id"]
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get trends: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve trends: {str(e)}")

@router.post("/trends/detect")
async def detect_trends(request: TrendDetectionRequest, current_user: dict = Depends(get_current_user)):
    """Advanced trend detection with configurable parameters"""
    try:
        trend_detector = get_trend_detector()
        
        # Process trend detection request
        results = await trend_detector.detect_trends(
            subreddits=request.subreddits,
            time_window=request.time_window,
            min_score=request.min_score,
            advanced_analysis=request.advanced_analysis
        )
        
        logger.info(f"Trend detection completed for user {current_user.get('email')}: {len(results)} trends found")
        
        return {
            "trends": results,
            "detection_params": request.dict(),
            "user_id": current_user["user_id"]
        }
        
    except Exception as e:
        logger.error(f"Trend detection failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Trend detection failed: {str(e)}")

@router.get("/intelligence/cross-platform")
async def get_cross_platform_intelligence(current_user: dict = Depends(get_current_user)):
    """Get cross-platform intelligence analysis"""
    try:
        market_intel = get_market_intelligence()
        
        # Get cross-platform analysis
        intelligence = await market_intel.get_cross_platform_analysis()
        
        return {
            "intelligence": intelligence,
            "timestamp": market_intel.get_last_update(),
            "user_id": current_user["user_id"]
        }
        
    except Exception as e:
        logger.error(f"Failed to get cross-platform intelligence: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Intelligence analysis failed: {str(e)}")

@router.get("/market/updates")
async def get_market_updates(
    hours_back: int = 24,
    current_user: dict = Depends(get_current_user)
):
    """Get real-time market updates"""
    try:
        market_intel = get_market_intelligence()
        
        # Get market updates
        updates = await market_intel.get_market_updates(hours_back=hours_back)
        
        return {
            "updates": updates,
            "hours_back": hours_back,
            "user_id": current_user["user_id"]
        }
        
    except Exception as e:
        logger.error(f"Failed to get market updates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Market updates failed: {str(e)}")

@router.get("/opportunities/{opportunity_id}/momentum")
async def get_opportunity_momentum(
    opportunity_id: str,
    days_back: int = 7,
    current_user: dict = Depends(get_current_user)
):
    """Get momentum analysis for specific opportunity"""
    try:
        market_intel = get_market_intelligence()
        
        # Get opportunity momentum
        momentum = await market_intel.get_opportunity_momentum(
            opportunity_id=opportunity_id,
            days_back=days_back
        )
        
        return {
            "momentum": momentum,
            "opportunity_id": opportunity_id,
            "days_back": days_back,
            "user_id": current_user["user_id"]
        }
        
    except Exception as e:
        logger.error(f"Failed to get opportunity momentum: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Momentum analysis failed: {str(e)}")

@router.get("/semantic/analyze", tags=["Semantic Analysis"])
async def analyze_semantic_content(
    content: str = Query(..., description="Text content to analyze"),
    context: Optional[str] = Query(None, description="Additional context")
):
    """Analyze text content using semantic analysis"""
    try:
        semantic_engine = get_semantic_engine()
        
        # Perform semantic analysis
        analysis = await semantic_engine.analyze_content(
            content=content,
            context=context
        )
        
        return {
            "analysis": analysis,
            "content_length": len(content),
            "has_context": context is not None
        }
        
    except Exception as e:
        logger.error(f"Semantic analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Semantic analysis failed: {str(e)}")

@router.post("/semantic/batch", tags=["Semantic Analysis"])
async def batch_semantic_analysis(request: Dict[str, Any]):
    """Batch semantic analysis for multiple content items"""
    try:
        semantic_engine = get_semantic_engine()
        
        # Process batch analysis
        results = await semantic_engine.batch_analyze(request)
        
        return {
            "results": results,
            "batch_size": len(request.get("items", [])),
            "processed": True
        }
        
    except Exception as e:
        logger.error(f"Batch semantic analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")

@router.get("/temporal/patterns", tags=["Temporal Analysis"])
async def analyze_temporal_patterns(
    timeframe_hours: int = Query(168, description="Analysis timeframe in hours", ge=1, le=720),
    source: Optional[str] = Query(None, description="Filter by specific source")
):
    """Analyze temporal patterns in data"""
    try:
        temporal_engine = get_temporal_engine()
        
        # Analyze temporal patterns
        patterns = await temporal_engine.analyze_patterns(
            timeframe_hours=timeframe_hours,
            source=source
        )
        
        return {
            "patterns": patterns,
            "timeframe_hours": timeframe_hours,
            "source": source
        }
        
    except Exception as e:
        logger.error(f"Temporal analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Temporal analysis failed: {str(e)}")

@router.get("/intelligence/trends", tags=["Intelligent Trends"])
async def detect_intelligent_trends(
    hours_back: int = Query(24, description="Hours to look back for trend detection", ge=1, le=168),
    min_intelligence_score: Optional[float] = Query(0.6, description="Minimum intelligence score threshold", ge=0.0, le=1.0)
):
    """Detect intelligent trends with advanced analysis"""
    try:
        integration_engine = get_semantic_trend_integration_engine()
        
        # Detect intelligent trends
        trends = await integration_engine.detect_intelligent_trends(
            hours_back=hours_back,
            min_score=min_intelligence_score
        )
        
        return {
            "trends": trends,
            "hours_back": hours_back,
            "min_intelligence_score": min_intelligence_score
        }
        
    except Exception as e:
        logger.error(f"Intelligent trend detection failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Trend detection failed: {str(e)}")

@router.get("/intelligence/context/{opportunity_id}", tags=["Intelligent Trends"])
async def get_opportunity_context(opportunity_id: str):
    """Get contextual intelligence for specific opportunity"""
    try:
        integration_engine = get_semantic_trend_integration_engine()
        
        # Get opportunity context
        context = await integration_engine.get_opportunity_context(opportunity_id)
        
        return {
            "context": context,
            "opportunity_id": opportunity_id
        }
        
    except Exception as e:
        logger.error(f"Failed to get opportunity context: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Context analysis failed: {str(e)}")

@router.get("/phase2/status", tags=["System Status"])
async def get_phase2_status():
    """Get Phase 2 system status"""
    try:
        semantic_engine = get_semantic_engine()
        temporal_engine = get_temporal_engine()
        integration_engine = get_semantic_trend_integration_engine()
        
        status = {
            "semantic_engine": await semantic_engine.get_status(),
            "temporal_engine": await temporal_engine.get_status(),
            "integration_engine": await integration_engine.get_status(),
            "overall_status": "operational"
        }
        
        return status
        
    except Exception as e:
        logger.error(f"Failed to get Phase 2 status: {str(e)}")
        return {"status": "error", "message": str(e)}

@router.post("/graph/trends")
async def detect_graph_trends(request: Request):
    """Detect trends using graph-based analysis"""
    try:
        graph_detector = GroundbreakingGraphTrendDetector()
        
        # Mock signal data for demonstration
        class MockSignal:
            def __init__(self, source, content, keywords, timestamp, engagement_score):
                self.source = source
                self.content = content
                self.keywords = keywords
                self.timestamp = timestamp
                self.engagement_score = engagement_score
        
        # Create mock signals
        mock_signals = [
            MockSignal("reddit", "AI automation tools", ["AI", "automation"], "2025-01-14T22:00:00Z", 0.85),
            MockSignal("twitter", "No-code platforms", ["no-code", "automation"], "2025-01-14T22:05:00Z", 0.78),
            MockSignal("reddit", "API management", ["API", "management"], "2025-01-14T22:10:00Z", 0.82)
        ]
        
        # Detect graph trends
        trends = await graph_detector.detect_trends(mock_signals)
        
        return {
            "trends": trends,
            "method": "graph_based_analysis",
            "signal_count": len(mock_signals)
        }
        
    except Exception as e:
        logger.error(f"Graph trend detection failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Graph analysis failed: {str(e)}") 