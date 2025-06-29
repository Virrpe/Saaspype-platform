#!/usr/bin/env python3
"""
Real-Time Intelligence Router - Phase 2 Tactical Improvement
Provides endpoints for real-time dialectical synthesis and live context switching
"""

from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from typing import Optional, Dict, Any, List
import logging
import asyncio
import json
from datetime import datetime

from src.api.domains.auth.endpoints.auth import get_current_user
from ..services.real_time_dialectical_engine import (
    get_real_time_dialectical_engine, RealTimeDialecticalEngine
)
from ..services.contextual_source_intelligence import QueryContext

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/intelligence", tags=["Real-time Intelligence"])

@router.post("/real-time/session", tags=["Real-time Sessions"])
async def create_real_time_session(
    session_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Create a new real-time synthesis session"""
    
    try:
        engine = get_real_time_dialectical_engine()
        
        # Start real-time processing if not already running
        await engine.start_real_time_processing()
        
        # Create session
        created_session_id = await engine.create_session(session_id)
        
        return {
            "success": True,
            "session_id": created_session_id,
            "status": "active",
            "capabilities": [
                "real_time_synthesis",
                "context_switching",
                "live_streaming",
                "session_analytics"
            ],
            "performance_targets": {
                "latency_ms": 100,
                "synthesis_quality": 0.85
            },
            "websocket_endpoint": f"/api/intelligence/ws/real-time/{created_session_id}",
            "created_at": datetime.now().isoformat(),
            "user_id": current_user["user_id"]
        }
        
    except Exception as e:
        logger.error(f"Failed to create real-time session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Session creation failed: {str(e)}")

@router.post("/real-time/synthesis", tags=["Real-time Synthesis"])
async def real_time_synthesis(
    query: str,
    session_id: str,
    force_context: Optional[str] = Query(None, description="Force specific context"),
    current_user: dict = Depends(get_current_user)
):
    """Perform real-time dialectical synthesis with live context switching"""
    
    try:
        engine = get_real_time_dialectical_engine()
        
        # Parse force_context if provided
        context = None
        if force_context:
            try:
                context = QueryContext(force_context)
            except ValueError:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid context: {force_context}. Valid contexts: {[c.value for c in QueryContext]}"
                )
        
        # Perform real-time synthesis
        synthesis_result = await engine.real_time_synthesis(
            query=query,
            session_id=session_id,
            force_context=context
        )
        
        return {
            "success": True,
            "synthesis": {
                "query": synthesis_result.query,
                "session_id": synthesis_result.session_id,
                "context": {
                    "type": synthesis_result.context.context.value,
                    "confidence": synthesis_result.context.confidence,
                    "detected_at": synthesis_result.context.detected_at.isoformat(),
                    "switch_reason": synthesis_result.context.switch_reason,
                    "previous_context": synthesis_result.context.previous_context.value if synthesis_result.context.previous_context else None
                },
                "sources": synthesis_result.selected_sources,
                "synthesis_score": synthesis_result.synthesis_score,
                "processing_time_ms": synthesis_result.processing_time_ms,
                "timestamp": synthesis_result.timestamp.isoformat()
            },
            "performance": {
                "latency_target_met": synthesis_result.processing_time_ms < 100,
                "quality_score": synthesis_result.synthesis_score,
                "real_time_capable": True
            },
            "streaming": {
                "websocket_notified": True,
                "broadcast_type": "real_time_synthesis"
            },
            "user_id": current_user["user_id"]
        }
        
    except Exception as e:
        logger.error(f"Real-time synthesis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Real-time synthesis failed: {str(e)}")

@router.get("/real-time/session/{session_id}/analytics", tags=["Session Analytics"])
async def get_session_analytics(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get comprehensive analytics for a real-time session"""
    
    try:
        engine = get_real_time_dialectical_engine()
        analytics = engine.get_session_analytics(session_id)
        
        if "error" in analytics:
            raise HTTPException(status_code=404, detail=analytics["error"])
        
        return {
            "success": True,
            "analytics": analytics,
            "user_id": current_user["user_id"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get session analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analytics retrieval failed: {str(e)}")

@router.get("/real-time/performance", tags=["Performance Monitoring"])
async def get_real_time_performance(
    current_user: dict = Depends(get_current_user)
):
    """Get comprehensive real-time performance report"""
    
    try:
        engine = get_real_time_dialectical_engine()
        performance_report = engine.get_real_time_performance_report()
        
        return {
            "success": True,
            "performance": performance_report,
            "phase_2_status": "operational",
            "capabilities": {
                "real_time_synthesis": True,
                "context_switching": True,
                "session_management": True,
                "websocket_streaming": True,
                "performance_monitoring": True
            },
            "user_id": current_user["user_id"]
        }
        
    except Exception as e:
        logger.error(f"Failed to get performance report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Performance report failed: {str(e)}")

@router.post("/real-time/start", tags=["System Control"])
async def start_real_time_engine(
    current_user: dict = Depends(get_current_user)
):
    """Start the real-time dialectical engine"""
    
    try:
        engine = get_real_time_dialectical_engine()
        await engine.start_real_time_processing()
        
        return {
            "success": True,
            "status": "started",
            "message": "Real-time dialectical engine started successfully",
            "capabilities_enabled": [
                "real_time_synthesis",
                "context_switching", 
                "session_management",
                "websocket_streaming"
            ],
            "user_id": current_user["user_id"]
        }
        
    except Exception as e:
        logger.error(f"Failed to start real-time engine: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Engine start failed: {str(e)}")

@router.post("/real-time/stop", tags=["System Control"])
async def stop_real_time_engine(
    current_user: dict = Depends(get_current_user)
):
    """Stop the real-time dialectical engine"""
    
    try:
        engine = get_real_time_dialectical_engine()
        await engine.stop_real_time_processing()
        
        return {
            "success": True,
            "status": "stopped",
            "message": "Real-time dialectical engine stopped successfully",
            "user_id": current_user["user_id"]
        }
        
    except Exception as e:
        logger.error(f"Failed to stop real-time engine: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Engine stop failed: {str(e)}")

@router.get("/real-time/contexts", tags=["Context Information"])
async def get_available_contexts(
    current_user: dict = Depends(get_current_user)
):
    """Get all available query contexts for real-time synthesis"""
    
    contexts = [
        {
            "name": context.value,
            "description": _get_context_description(context),
            "typical_sources": _get_context_sources(context)
        }
        for context in QueryContext
    ]
    
    return {
        "success": True,
        "contexts": contexts,
        "total_contexts": len(contexts),
        "phase_2_enhancement": "Real-time context switching enabled",
        "user_id": current_user["user_id"]
    }

def _get_context_description(context: QueryContext) -> str:
    """Get description for a query context"""
    
    descriptions = {
        QueryContext.PAIN_POINT_DISCOVERY: "Identify user problems and frustrations",
        QueryContext.TECHNICAL_TRENDS: "Track emerging technologies and development trends",
        QueryContext.MARKET_VALIDATION: "Validate product-market fit and demand",
        QueryContext.STARTUP_INTELLIGENCE: "Monitor startup ecosystem and funding",
        QueryContext.REAL_TIME_MONITORING: "Track breaking news and trending topics",
        QueryContext.COMPETITIVE_ANALYSIS: "Analyze competitor activities and positioning",
        QueryContext.DEVELOPER_INSIGHTS: "Understand developer needs and preferences",
        QueryContext.GENERAL_EXPLORATION: "Balanced exploration across multiple domains"
    }
    
    return descriptions.get(context, "Context-specific information gathering")

def _get_context_sources(context: QueryContext) -> List[str]:
    """Get typical sources for a query context"""
    
    source_mapping = {
        QueryContext.PAIN_POINT_DISCOVERY: ["reddit", "stackoverflow", "hackernews"],
        QueryContext.TECHNICAL_TRENDS: ["github", "hackernews", "devto"],
        QueryContext.MARKET_VALIDATION: ["producthunt", "indiehackers", "reddit"],
        QueryContext.STARTUP_INTELLIGENCE: ["hackernews", "indiehackers", "producthunt"],
        QueryContext.REAL_TIME_MONITORING: ["twitter", "hackernews"],
        QueryContext.COMPETITIVE_ANALYSIS: ["github", "producthunt", "hackernews"],
        QueryContext.DEVELOPER_INSIGHTS: ["stackoverflow", "github", "devto"],
        QueryContext.GENERAL_EXPLORATION: ["hackernews", "github", "producthunt"]
    }
    
    return source_mapping.get(context, ["hackernews", "github"])

# WebSocket endpoint for real-time synthesis streaming
@router.websocket("/ws/real-time/{session_id}")
async def websocket_real_time_synthesis(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time synthesis streaming for a specific session"""
    
    try:
        await websocket.accept()
        
        # Get engine and verify session
        engine = get_real_time_dialectical_engine()
        
        if session_id not in engine.active_sessions:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": f"Session {session_id} not found",
                "timestamp": datetime.now().isoformat()
            }))
            await websocket.close()
            return
        
        logger.info(f"WebSocket connected for real-time session: {session_id}")
        
        # Send welcome message
        welcome_message = {
            "type": "session_connected",
            "session_id": session_id,
            "capabilities": [
                "real_time_synthesis",
                "context_switch_notifications",
                "performance_metrics",
                "session_analytics"
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        await websocket.send_text(json.dumps(welcome_message))
        
        # Keep connection alive and handle messages
        while True:
            try:
                # Wait for client message
                data = await websocket.receive_text()
                message = json.loads(data)
                
                message_type = message.get("type")
                
                if message_type == "ping":
                    await websocket.send_text(json.dumps({
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    }))
                
                elif message_type == "request_analytics":
                    analytics = engine.get_session_analytics(session_id)
                    await websocket.send_text(json.dumps({
                        "type": "session_analytics",
                        "data": analytics,
                        "timestamp": datetime.now().isoformat()
                    }))
                
                elif message_type == "request_performance":
                    performance = engine.get_real_time_performance_report()
                    await websocket.send_text(json.dumps({
                        "type": "performance_report",
                        "data": performance,
                        "timestamp": datetime.now().isoformat()
                    }))
                
                else:
                    await websocket.send_text(json.dumps({
                        "type": "unknown_message_type",
                        "received": message_type,
                        "timestamp": datetime.now().isoformat()
                    }))
                
            except WebSocketDisconnect:
                logger.info(f"WebSocket disconnected for session: {session_id}")
                break
            except Exception as e:
                logger.error(f"WebSocket error for session {session_id}: {e}")
                break
    
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
    finally:
        logger.info(f"WebSocket connection closed for session: {session_id}")

# Global WebSocket endpoint for all real-time events
@router.websocket("/ws/real-time")
async def websocket_real_time_global(websocket: WebSocket):
    """Global WebSocket endpoint for all real-time dialectical events"""
    
    try:
        await websocket.accept()
        logger.info("Global real-time WebSocket connected")
        
        # Send welcome message
        welcome_message = {
            "type": "global_connection",
            "capabilities": [
                "all_session_events",
                "system_performance",
                "context_switch_notifications",
                "synthesis_results"
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        await websocket.send_text(json.dumps(welcome_message))
        
        # Register with global broadcaster
        from ...streaming.services.websocket_broadcaster import websocket_broadcaster
        await websocket_broadcaster.connect(websocket, "real_time_global")
        
        # Keep connection alive
        while True:
            try:
                data = await websocket.receive_text()
                await websocket_broadcaster.handle_client_message(websocket, data)
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Global WebSocket error: {e}")
                break
    
    except Exception as e:
        logger.error(f"Global WebSocket connection error: {e}")
    finally:
        from ...streaming.services.websocket_broadcaster import websocket_broadcaster
        await websocket_broadcaster.disconnect(websocket)
        logger.info("Global real-time WebSocket disconnected") 