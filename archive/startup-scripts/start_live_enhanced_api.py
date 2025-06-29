#!/usr/bin/env python3
"""
Live AI Enhancement for Minimal Container
Phase 23: Real-time AI integration without container rebuild
"""

import os
import sys
import uvicorn
import re
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add project paths
sys.path.append('.')
sys.path.append('./src')

print("🚀 Starting Luciq API with Live AI Enhancement...")
print("🧠 AI Enhancement Phase 23: Live Integration")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Basic AI engine using existing packages
class BasicSemanticEngine:
    """Basic semantic analysis using minimal dependencies"""
    
    def __init__(self):
        self.initialized = True
        logger.info("✅ Basic Semantic Engine initialized")
        
    async def analyze_basic_semantics(self, content: str, context: Dict = None) -> Dict:
        """Basic semantic analysis using string processing"""
        try:
            words = content.lower().split()
            word_count = len(words)
            
            # Basic sentiment analysis
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
            
            return {
                "analysis_type": "basic_semantic_live_enhancement",
                "sentiment": sentiment,
                "word_count": word_count,
                "positive_indicators": positive_score,
                "negative_indicators": negative_score,
                "ai_engine_status": "basic_live_enhancement"
            }
        except Exception as e:
            return {"error": str(e)}

# Create FastAPI app
app = FastAPI(
    title="Luciq API - Live Enhanced",
    description="Live Enhanced API with Basic AI",
    version="2.6-live-enhanced"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI engine
basic_ai_engine = BasicSemanticEngine()

class AnalysisRequest(BaseModel):
    content: str
    context: Optional[Dict[str, Any]] = {}

@app.get("/")
async def root():
    return {
        "message": "Luciq API - Live Enhanced Mode",
        "ai_enhancement": "basic_semantic_enabled",
        "phase": "23_first_ai_integration"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "mode": "live_enhanced",
        "ai_engines": {"basic_semantic": "enabled"},
        "phase": "23_ai_enhancement_live_integration"
    }

@app.get("/api/test")
async def test():
    return {
        "backend": "operational",
        "ai_enhancement": "basic_semantic_live_integrated",
        "message": "Live enhanced backend with basic AI capabilities!"
    }

@app.post("/api/intelligence/basic")
async def basic_ai_analysis(request: AnalysisRequest):
    """Basic AI Analysis with live enhancement"""
    start_time = datetime.now()
    
    try:
        result = await basic_ai_engine.analyze_basic_semantics(
            request.content, request.context
        )
        
        processing_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            "success": True,
            "engine_used": "basic_semantic_live",
            "processing_time_ms": processing_time_ms,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/system/status")
async def system_status():
    """Live enhanced system status"""
    return {
        "system_status": "live_enhanced_operational",
        "ai_engines": {"basic_semantic": "enabled"},
        "enhancement_phase": "23_live_ai_integration",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    print("✅ Live Enhanced FastAPI app ready")
    uvicorn.run(app, host="0.0.0.0", port=8003) 