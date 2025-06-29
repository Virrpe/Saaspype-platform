#!/usr/bin/env python3
"""
Minimal Luciq API Startup
Works without heavy AI dependencies for initial Docker testing
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add project paths
sys.path.append('.')
sys.path.append('./src')

# Set environment variables for minimal mode
os.environ['LUCIQ_MINIMAL_MODE'] = 'true'
os.environ['LUCIQ_DISABLE_ALL_AI'] = 'true'
os.environ['LUCIQ_FAST_MODE'] = 'true'
os.environ['LUCIQ_SKIP_NLP_MODELS'] = 'true'
os.environ['LUCIQ_SKIP_TRANSFORMERS'] = 'true'

print("🚀 Starting Luciq API in Minimal Mode...")
print("⚡ All AI models disabled for dependency testing")
print("📁 Working directory:", os.getcwd())

try:
    # Import minimal FastAPI app
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    
    app = FastAPI(
        title="Luciq API - Minimal Mode",
        description="Minimal API for Docker testing",
        version="2.6-minimal"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    async def root():
        return {"message": "Luciq API - Minimal Mode", "status": "running"}
    
    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "mode": "minimal",
            "ai_engines": "disabled",
            "dependencies": "basic"
        }
    
    @app.get("/api/test")
    async def test():
        return {
            "backend": "operational",
            "containers": "docker",
            "frontend_port": 3001,
            "redis_port": 6379,
            "message": "Backend container is working!"
        }
    
    print("✅ Minimal FastAPI app created successfully")
    print("🌐 Starting server on 0.0.0.0:8003")
    print("📖 API docs available at http://localhost:8003/docs")
    
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
    print(f"❌ Failed to start minimal API server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 