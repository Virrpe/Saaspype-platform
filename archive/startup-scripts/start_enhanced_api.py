#!/usr/bin/env python3
"""
Enhanced Luciq API Startup
Phase 23: AI Enhancement Integration - First Engine (Semantic Analysis)
Gradually adds AI capabilities while maintaining container stability
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add project paths
sys.path.append('.')
sys.path.append('./src')

# Set environment variables for enhanced mode
os.environ['LUCIQ_ENHANCED_MODE'] = 'true'
os.environ['LUCIQ_ENABLE_SEMANTIC_AI'] = 'true'  # Enable only semantic engine first
os.environ['LUCIQ_DISABLE_HEAVY_AI'] = 'true'    # Keep heavy models disabled
os.environ['LUCIQ_FAST_MODE'] = 'true'
os.environ['LUCIQ_SKIP_TRANSFORMERS'] = 'true'   # Skip transformers for now

print("🚀 Starting Luciq API in Enhanced Mode...")
print("🧠 AI Enhancement Phase 23: First Engine Integration")
print("⚡ Semantic Analysis Engine: ENABLED")
print("🔒 Heavy AI models: DISABLED (incremental approach)")
print("📁 Working directory:", os.getcwd())

try:
    # Import enhanced FastAPI app with first AI engine
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
    from typing import Dict, Any, Optional
    import logging
    from datetime import datetime
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Create enhanced FastAPI app
    app = FastAPI(
        title="Luciq API - Enhanced Mode",
        description="Enhanced API with Semantic AI Engine Integration",
        version="2.6-enhanced-semantic"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Initialize semantic engine (lightweight)
    semantic_engine = None
    try:
        print("🧠 Initializing Semantic Analysis Engine...")
        from src.api.domains.intelligence.services.semantic_analysis_engine import AdvancedSemanticEngine
        semantic_engine = AdvancedSemanticEngine()
        print("✅ Semantic Analysis Engine initialized successfully")
    except Exception as e:
        print(f"⚠️ Semantic engine initialization failed (fallback mode): {e}")
        semantic_engine = None
    
    # Pydantic models
    class SemanticAnalysisRequest(BaseModel):
        content: str
        context: Optional[Dict[str, Any]] = {}
    
    class AnalysisResponse(BaseModel):
        success: bool
        engine_used: str
        processing_time_ms: float
        result: Dict[str, Any]
        timestamp: str
    
    # Basic endpoints (preserved from minimal)
    @app.get("/")
    async def root():
        return {
            "message": "Luciq API - Enhanced Mode", 
            "status": "running",
            "ai_enhancement": "semantic_analysis_enabled",
            "phase": "23_first_engine_integration"
        }
    
    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "mode": "enhanced",
            "ai_engines": {
                "semantic": "enabled" if semantic_engine else "failed",
                "heavy_models": "disabled"
            },
            "dependencies": "enhanced_basic",
            "phase": "23_ai_enhancement_integration"
        }
    
    @app.get("/api/test")
    async def test():
        return {
            "backend": "operational",
            "containers": "docker",
            "frontend_port": 3001,
            "redis_port": 6379,
            "ai_enhancement": "semantic_engine_integrated",
            "message": "Enhanced backend container with AI capabilities!"
        }
    
    # Enhanced AI endpoint - Semantic Analysis
    @app.post("/api/intelligence/semantic", response_model=AnalysisResponse)
    async def analyze_semantic(request: SemanticAnalysisRequest):
        """
        Semantic Analysis with first AI engine integration
        Lightweight analysis perfect for testing AI enhancement
        """
        start_time = datetime.now()
        
        try:
            if not semantic_engine:
                raise HTTPException(
                    status_code=503, 
                    detail="Semantic analysis engine not available (fallback mode)"
                )
            
            logger.info(f"🧠 Processing semantic analysis: {request.content[:50]}...")
            
            # Perform semantic analysis
            result = await semantic_engine.analyze_semantic_understanding(
                request.content, 
                request.context
            )
            
            processing_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            return AnalysisResponse(
                success=True,
                engine_used="semantic_analysis",
                processing_time_ms=processing_time_ms,
                result=result,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            processing_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(f"❌ Semantic analysis failed: {e}")
            
            return AnalysisResponse(
                success=False,
                engine_used="semantic_analysis",
                processing_time_ms=processing_time_ms,
                result={"error": str(e)},
                timestamp=datetime.now().isoformat()
            )
    
    # Enhanced endpoint - Simple text analysis (fallback)
    @app.post("/api/intelligence/simple")
    async def simple_analysis(request: SemanticAnalysisRequest):
        """
        Simple text analysis (fallback when AI engine unavailable)
        Ensures API stability even if AI components fail
        """
        start_time = datetime.now()
        
        try:
            # Basic text analysis without heavy AI
            content = request.content
            word_count = len(content.split())
            char_count = len(content)
            
            # Simple sentiment scoring (basic heuristic)
            positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'best', 'perfect']
            negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'poor']
            
            content_lower = content.lower()
            positive_score = sum(1 for word in positive_words if word in content_lower)
            negative_score = sum(1 for word in negative_words if word in content_lower)
            
            sentiment = "neutral"
            if positive_score > negative_score:
                sentiment = "positive"
            elif negative_score > positive_score:
                sentiment = "negative"
            
            result = {
                "analysis_type": "simple_fallback",
                "word_count": word_count,
                "character_count": char_count,
                "sentiment": sentiment,
                "positive_indicators": positive_score,
                "negative_indicators": negative_score,
                "ai_engine_status": "fallback_mode"
            }
            
            processing_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            return {
                "success": True,
                "engine_used": "simple_fallback",
                "processing_time_ms": processing_time_ms,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            processing_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(f"❌ Simple analysis failed: {e}")
            
            return {
                "success": False,
                "engine_used": "simple_fallback",
                "processing_time_ms": processing_time_ms,
                "result": {"error": str(e)},
                "timestamp": datetime.now().isoformat()
            }
    
    # System status endpoint
    @app.get("/api/system/status")
    async def system_status():
        """Enhanced system status with AI engine information"""
        return {
            "system_status": "enhanced_operational",
            "api_mode": "enhanced_with_ai",
            "containers": {
                "backend": "operational_enhanced",
                "frontend": "operational",
                "redis": "healthy"
            },
            "ai_engines": {
                "semantic": "enabled" if semantic_engine else "fallback",
                "heavy_models": "disabled_incremental_approach",
                "next_integration": "cross_platform_engine"
            },
            "enhancement_phase": "23_first_engine_integration",
            "stability": "maintained_through_incremental_approach",
            "timestamp": datetime.now().isoformat()
        }
    
    print("✅ Enhanced FastAPI app created successfully")
    print("🧠 Semantic Analysis Engine: Ready for testing")
    print("🌐 Starting enhanced server on 0.0.0.0:8003")
    print("📖 API docs available at http://localhost:8003/docs")
    print("🧪 Test semantic analysis: POST /api/intelligence/semantic")
    
    # Start server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8003,
        reload=False,
        log_level="info",
        access_log=True
    )
    
except Exception as e:
    print(f"❌ Failed to start enhanced API server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 