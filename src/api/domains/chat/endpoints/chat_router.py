#!/usr/bin/env python3
"""
Chat API Router - NLP Chat Interface for Idea Generation and Insights
Handles natural language conversations, idea management, and data visualization
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import json
import re

from src.api.domains.auth.endpoints.auth import get_current_user
from src.services.orchestration.intelligence_orchestrator import get_intelligence_orchestrator
from ..services.chat_processor import ChatProcessor
from ..services.idea_manager import IdeaManager
from ..services.insights_generator import InsightsGenerator

logger = logging.getLogger(__name__)

# Pydantic models
class ChatMessage(BaseModel):
    """Chat message model"""
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Chat session ID")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")

class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    intent: str
    actions: List[Dict[str, Any]]
    data: Optional[Dict[str, Any]]
    session_id: str
    timestamp: str

class IdeaRequest(BaseModel):
    """Idea save request"""
    title: str
    description: str
    category: Optional[str] = "general"
    rating: Optional[int] = None
    tags: Optional[List[str]] = []

class InsightsRequest(BaseModel):
    """Insights generation request"""
    analysis_type: str = Field(..., description="Type of analysis: trends, categories, ratings, recommendations")
    filters: Optional[Dict[str, Any]] = Field(None, description="Filters for analysis")

# Create router
router = APIRouter(prefix="/api/chat", tags=["AI Chat Interface"])

# Initialize services
chat_processor = ChatProcessor()
idea_manager = IdeaManager()
insights_generator = InsightsGenerator()

# Demo endpoints (no authentication required)
@router.post("/demo/message", response_model=ChatResponse)
async def process_demo_chat_message(request: ChatMessage):
    """
    Demo chat endpoint - no authentication required
    """
    try:
        user_id = "demo_user"
        
        # Process message with NLP
        result = await chat_processor.process_message(
            message=request.message,
            user_id=user_id,
            session_id=request.session_id,
            context=request.context
        )
        
        return ChatResponse(
            response=result["response"],
            intent=result["intent"],
            actions=result["actions"],
            data=result.get("data"),
            session_id=result["session_id"],
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Demo chat processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/demo/save-idea")
async def save_demo_idea(request: IdeaRequest):
    """
    Demo save idea endpoint - no authentication required
    """
    try:
        user_id = "demo_user"
        
        idea_id = await idea_manager.save_idea(
            user_id=user_id,
            title=request.title,
            description=request.description,
            category=request.category,
            rating=request.rating,
            tags=request.tags
        )
        
        return {
            "success": True,
            "idea_id": idea_id,
            "message": f"Idea '{request.title}' saved successfully!"
        }
        
    except Exception as e:
        logger.error(f"Demo save idea error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/demo/ideas")
async def get_demo_ideas():
    """
    Demo get ideas endpoint - no authentication required
    """
    try:
        user_id = "demo_user"
        
        ideas = await idea_manager.get_user_ideas(
            user_id=user_id,
            limit=50
        )
        
        return {
            "success": True,
            "ideas": ideas,
            "total": len(ideas)
        }
        
    except Exception as e:
        logger.error(f"Demo get ideas error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/message", response_model=ChatResponse)
async def process_chat_message(
    request: ChatMessage,
    current_user: dict = Depends(get_current_user)
):
    """
    Process natural language chat message and return intelligent response
    """
    try:
        user_id = current_user["user_id"]
        
        # Process message with NLP
        result = await chat_processor.process_message(
            message=request.message,
            user_id=user_id,
            session_id=request.session_id,
            context=request.context
        )
        
        return ChatResponse(
            response=result["response"],
            intent=result["intent"],
            actions=result["actions"],
            data=result.get("data"),
            session_id=result["session_id"],
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Chat processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ideas/save")
async def save_idea(
    request: IdeaRequest,
    current_user: dict = Depends(get_current_user)
):
    """Save a new idea to user's collection"""
    try:
        user_id = current_user["user_id"]
        
        idea_id = await idea_manager.save_idea(
            user_id=user_id,
            title=request.title,
            description=request.description,
            category=request.category,
            rating=request.rating,
            tags=request.tags
        )
        
        return {
            "success": True,
            "idea_id": idea_id,
            "message": f"Idea '{request.title}' saved successfully!"
        }
        
    except Exception as e:
        logger.error(f"Save idea error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ideas")
async def get_user_ideas(
    current_user: dict = Depends(get_current_user),
    category: Optional[str] = None,
    limit: int = 50
):
    """Get user's saved ideas"""
    try:
        user_id = current_user["user_id"]
        
        ideas = await idea_manager.get_user_ideas(
            user_id=user_id,
            category=category,
            limit=limit
        )
        
        return {
            "success": True,
            "ideas": ideas,
            "total": len(ideas)
        }
        
    except Exception as e:
        logger.error(f"Get ideas error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class RatingRequest(BaseModel):
    """Rating request model"""
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")

@router.post("/ideas/{idea_id}/rate")
async def rate_idea(
    idea_id: str,
    request: RatingRequest,
    current_user: dict = Depends(get_current_user)
):
    """Rate an idea (1-5 stars)"""
    try:
        user_id = current_user["user_id"]
        
        success = await idea_manager.rate_idea(
            idea_id=idea_id,
            user_id=user_id,
            rating=request.rating
        )
        
        if success:
            return {"success": True, "message": f"Idea rated {request.rating} stars"}
        else:
            raise HTTPException(status_code=404, detail="Idea not found")
            
    except Exception as e:
        logger.error(f"Rate idea error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/insights/generate")
async def generate_insights(
    request: InsightsRequest,
    current_user: dict = Depends(get_current_user)
):
    """Generate insights and visualizations from user's ideas"""
    try:
        user_id = current_user["user_id"]
        
        insights = await insights_generator.generate_insights(
            user_id=user_id,
            analysis_type=request.analysis_type,
            filters=request.filters
        )
        
        return {
            "success": True,
            "insights": insights,
            "analysis_type": request.analysis_type,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Generate insights error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class GenerateIdeasRequest(BaseModel):
    """Generate ideas request model"""
    topic: str = Field(..., description="Topic or domain for idea generation")
    count: int = Field(5, ge=1, le=20, description="Number of ideas to generate")

@router.post("/generate-ideas")
async def generate_new_ideas(
    request: GenerateIdeasRequest,
    current_user: dict = Depends(get_current_user)
):
    """Generate new business ideas using the orchestration engine"""
    try:
        user_id = current_user["user_id"]
        
        # Use the existing orchestration system
        orchestrator = get_intelligence_orchestrator()
        
        from src.services.orchestration.intelligence_orchestrator import OrchestrationRequest
        
        orchestration_request = OrchestrationRequest(
            request_type="business_idea_generation",
            data={
                "topic": request.topic,
                "count": request.count,
                "user_context": "chat_interface",
                "personalization": True
            },
            session_id=f"chat_{user_id}_{int(datetime.now().timestamp())}",
            priority="high"
        )
        
        result = await orchestrator.analyze_intelligence(orchestration_request)
        
        if result.success:
            # Extract ideas from result
            ideas = result.results.get("business_ideas", [])
            
            return {
                "success": True,
                "ideas": ideas,
                "topic": request.topic,
                "processing_time_ms": result.processing_time_ms,
                "engines_used": result.engines_used
            }
        else:
            raise HTTPException(status_code=500, detail="Idea generation failed")
            
    except Exception as e:
        logger.error(f"Generate ideas error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/charts/{chart_type}")
async def generate_chart_data(
    chart_type: str,
    current_user: dict = Depends(get_current_user)
):
    """Generate chart data for visualization"""
    try:
        user_id = current_user["user_id"]
        
        chart_data = await insights_generator.generate_chart_data(
            user_id=user_id,
            chart_type=chart_type
        )
        
        return {
            "success": True,
            "chart_type": chart_type,
            "data": chart_data,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Generate chart error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export")
async def export_user_data(
    format: str = "json",
    current_user: dict = Depends(get_current_user)
):
    """Export user's ideas and data"""
    try:
        user_id = current_user["user_id"]
        
        export_data = await idea_manager.export_user_data(
            user_id=user_id,
            format=format
        )
        
        return {
            "success": True,
            "format": format,
            "data": export_data,
            "exported_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Export data error: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 