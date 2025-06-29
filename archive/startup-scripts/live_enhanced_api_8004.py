#!/usr/bin/env python3
"""
Live AI Enhancement - Port 8004 Demo
Phase 23: AI integration without container rebuild
"""

import uvicorn
import re
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

print("🚀 Starting Live Enhanced API on Port 8004...")

# Enhanced AI engine
class EnhancedSemanticEngine:
    def __init__(self):
        self.initialized = True
        
    async def analyze_enhanced_semantics(self, content: str, context: Dict = None) -> Dict:
        try:
            words = content.lower().split()
            word_count = len(words)
            
            # Enhanced sentiment with confidence
            positive_words = ['good', 'great', 'excellent', 'amazing', 'fantastic', 'wonderful']
            negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disappointing', 'poor']
            
            content_lower = content.lower()
            positive_score = sum(1 for word in positive_words if word in content_lower)
            negative_score = sum(1 for word in negative_words if word in content_lower)
            
            if positive_score > negative_score:
                sentiment = "positive"
                confidence = min(positive_score / max(word_count/10, 1), 1.0)
            elif negative_score > positive_score:
                sentiment = "negative"
                confidence = min(negative_score / max(word_count/10, 1), 1.0)
            else:
                sentiment = "neutral"
                confidence = 0.5
            
            # Intent detection
            intent = "unknown"
            if any(word in content_lower for word in ['need', 'want', 'looking for']):
                intent = "request"
            elif any(word in content_lower for word in ['how', 'what', 'when']):
                intent = "question"
                
            return {
                "analysis_type": "enhanced_live_integration",
                "sentiment": sentiment,
                "confidence": round(confidence, 2),
                "word_count": word_count,
                "intent": intent,
                "positive_score": positive_score,
                "negative_score": negative_score,
                "enhancement_status": "live_deployed_without_rebuild"
            }
        except Exception as e:
            return {"error": str(e)}

# Create app
app = FastAPI(title="Luciq Live Enhanced API", version="2.6-enhanced-8004")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

# Initialize engine
ai_engine = EnhancedSemanticEngine()

class AnalysisRequest(BaseModel):
    content: str

@app.get("/")
async def root():
    return {
        "message": "Luciq Live Enhanced API (Port 8004)",
        "ai_enhancement": "live_integrated",
        "phase": "23_ai_enhancement"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "mode": "live_enhanced",
        "port": 8004,
        "ai_engine": "enhanced_semantic_enabled"
    }

@app.post("/api/intelligence/enhanced")
async def enhanced_analysis(request: AnalysisRequest):
    start_time = datetime.now()
    
    result = await ai_engine.analyze_enhanced_semantics(request.content)
    processing_time = (datetime.now() - start_time).total_seconds() * 1000
    
    return {
        "success": True,
        "engine": "enhanced_semantic_live",
        "processing_time_ms": processing_time,
        "result": result,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/demo")
async def demo():
    return {
        "demo_message": "AI Enhancement successfully deployed without container rebuild!",
        "capabilities": ["sentiment_analysis", "intent_detection", "enhanced_processing"],
        "achievement": "Phase 23: Live AI Integration Complete"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004) 