#!/usr/bin/env python3
"""
Live AI Enhancement for Minimal Container - Port 8004
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

print("🚀 Starting Luciq Live Enhanced API on Port 8004...")
print("🧠 AI Enhancement Phase 23: Live Integration (Port 8004)")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enhanced AI engine using existing packages
class BasicSemanticEngine:
    """Enhanced semantic analysis using minimal dependencies"""
    
    def __init__(self):
        self.initialized = True
        logger.info("✅ Enhanced Semantic Engine initialized")
        
    async def analyze_basic_semantics(self, content: str, context: Dict = None) -> Dict:
        """Enhanced semantic analysis using string processing"""
        try:
            words = content.lower().split()
            word_count = len(words)
            char_count = len(content)
            
            # Enhanced keyword extraction
            word_freq = {}
            for word in words:
                clean_word = re.sub(r'[^\w]', '', word)
                if len(clean_word) > 3:
                    word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
            
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Enhanced sentiment analysis
            positive_words = [
                'good', 'great', 'excellent', 'amazing', 'love', 'best', 'perfect',
                'fantastic', 'wonderful', 'awesome', 'outstanding', 'brilliant',
                'helpful', 'efficient', 'effective', 'valuable', 'useful', 'innovative'
            ]
            negative_words = [
                'bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'poor',
                'disappointing', 'frustrating', 'useless', 'broken', 'slow',
                'expensive', 'difficult', 'confusing', 'unreliable', 'problematic'
            ]
            
            content_lower = content.lower()
            positive_score = sum(1 for word in positive_words if word in content_lower)
            negative_score = sum(1 for word in negative_words if word in content_lower)
            
            # Calculate sentiment with confidence
            if positive_score > negative_score:
                sentiment = "positive"
                confidence = min((positive_score - negative_score) / max(word_count/10, 1), 1.0)
            elif negative_score > positive_score:
                sentiment = "negative" 
                confidence = min((negative_score - positive_score) / max(word_count/10, 1), 1.0)
            else:
                sentiment = "neutral"
                confidence = 0.5
            
            # Basic intent detection
            intent = "unknown"
            if any(word in content_lower for word in ['need', 'want', 'looking for', 'require']):
                intent = "request"
            elif any(word in content_lower for word in ['how', 'what', 'when', 'where', 'why']):
                intent = "question"
            elif any(word in content_lower for word in ['thank', 'thanks', 'appreciate']):
                intent = "gratitude"
            
            # Business domain detection
            business_domains = []
            if any(word in content_lower for word in ['project', 'task', 'team', 'management']):
                business_domains.append('project_management')
            if any(word in content_lower for word in ['sales', 'customer', 'revenue']):
                business_domains.append('sales')
            if any(word in content_lower for word in ['software', 'tech', 'api']):
                business_domains.append('technology')
            
            return {
                "analysis_type": "enhanced_semantic_live_integration",
                "text_metrics": {
                    "word_count": word_count,
                    "character_count": char_count,
                    "avg_word_length": sum(len(word) for word in words) / max(len(words), 1)
                },
                "sentiment_analysis": {
                    "sentiment": sentiment,
                    "confidence": round(confidence, 2),
                    "positive_indicators": positive_score,
                    "negative_indicators": negative_score
                },
                "keywords": [{"word": word, "frequency": freq} for word, freq in top_keywords],
                "intent": intent,
                "business_domains": business_domains,
                "ai_engine_status": "enhanced_live_integration",
                "enhancement_level": "phase_23_live_deployment"
            }
        except Exception as e:
            return {"error": str(e), "analysis_type": "error_fallback"}

# Create FastAPI app
app = FastAPI(
    title="Luciq API - Live Enhanced (Port 8004)",
    description="Live Enhanced API with Basic AI Integration",
    version="2.6-live-enhanced-8004"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize enhanced AI engine
enhanced_ai_engine = BasicSemanticEngine()

class AnalysisRequest(BaseModel):
    content: str
    context: Optional[Dict[str, Any]] = {}

@app.get("/")
async def root():
    return {
        "message": "Luciq API - Live Enhanced Mode (Port 8004)",
        "ai_enhancement": "enhanced_semantic_enabled",
        "enhancement_type": "live_integration_port_8004",
        "phase": "23_live_ai_integration"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "mode": "live_enhanced",
        "port": 8004,
        "ai_engines": {"enhanced_semantic": "enabled"},
        "phase": "23_ai_enhancement_live_integration",
        "enhancement_method": "live_deployment_without_rebuild"
    }

@app.get("/api/test")
async def test():
    return {
        "backend": "operational_enhanced",
        "port": 8004,
        "ai_enhancement": "enhanced_semantic_live_integrated",
        "enhancement_approach": "live_deployment_incremental",
        "message": "Live enhanced backend with sophisticated AI capabilities!"
    }

@app.post("/api/intelligence/enhanced")
async def enhanced_ai_analysis(request: AnalysisRequest):
    """Enhanced AI Analysis with live integration"""
    start_time = datetime.now()
    
    try:
        result = await enhanced_ai_engine.analyze_basic_semantics(
            request.content, request.context
        )
        
        processing_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            "success": True,
            "engine_used": "enhanced_semantic_live",
            "processing_time_ms": processing_time_ms,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        processing_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        return {
            "success": False,
            "engine_used": "enhanced_semantic_live",
            "processing_time_ms": processing_time_ms,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/api/system/status")
async def system_status():
    """Live enhanced system status"""
    return {
        "system_status": "live_enhanced_operational",
        "api_mode": "enhanced_with_ai_port_8004",
        "ai_engines": {
            "enhanced_semantic": "enabled",
            "capabilities": ["sentiment", "keywords", "intent", "business_domains"]
        },
        "enhancement_phase": "23_live_ai_integration",
        "enhancement_method": "live_deployment_without_container_rebuild",
        "port": 8004,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/enhancement/demo")
async def enhancement_demo():
    """Demonstration of AI enhancement capabilities"""
    return {
        "demo_content": "This is a fantastic project management tool!",
        "capabilities_demonstrated": [
            "Text analysis (word count, character count)",
            "Sentiment analysis with confidence scoring",
            "Keyword extraction with frequency",
            "Intent detection (request, question, gratitude)",
            "Business domain classification",
            "Real-time processing with timing"
        ],
        "enhancement_achievements": {
            "deployment_method": "live_integration_without_rebuild",
            "ai_capabilities_added": "semantic_analysis_engine",
            "container_stability": "maintained",
            "performance_impact": "minimal"
        },
        "next_phase": "advanced_nlp_integration_with_container_rebuild"
    }

if __name__ == "__main__":
    print("✅ Live Enhanced FastAPI app ready on port 8004")
    print("🧠 Enhanced AI Engine: Operational")
    print("🌐 API accessible at: http://localhost:8004")
    uvicorn.run(app, host="0.0.0.0", port=8004) 