#!/usr/bin/env python3
"""
Luciq API - Refactored Main Application
Clean domain-driven FastAPI application with modular routers
"""

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import time
import logging
from pathlib import Path

# Configuration and core services
from src.shared.config.settings import (
    LOG_DIR, LOG_LEVEL, CORS_ORIGINS, API_HOST, API_PORT
)
from src.api.shared.services.metrics_service import metrics_service
from src.api.shared.services.performance_monitor import performance_monitor

# Domain routers
from src.api.domains.auth.endpoints.auth import router as auth_router, get_current_user
from src.api.domains.discovery.endpoints.discovery_router import router as discovery_router
from src.api.domains.intelligence.endpoints.intelligence_router import router as intelligence_router
from src.api.domains.intelligence.endpoints.real_time_router import router as real_time_router
from src.api.domains.streaming.endpoints.streaming_router import router as streaming_router
from src.api.domains.credibility.endpoints.credibility_router import router as credibility_router

# Orchestration layer
from src.services.orchestration.orchestration_api import router as orchestration_router

# Chat domain
from src.api.domains.chat.endpoints.chat_router import router as chat_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI with production metadata
app = FastAPI(
    title="Luciq API",
    description="SaaS Idea Discovery Engine - Real-time Reddit analysis with LLM intelligence",
    version="2.1.0-refactored",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request counting middleware
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    
    # Increment request counter
    metrics_service.increment_request_counter(request.url.path)
    
    try:
        response = await call_next(request)
        
        # Log request
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
        
        return response
    except Exception as e:
        metrics_service.increment_error_counter()
        logger.error(f"Request failed: {request.method} {request.url.path} - {str(e)}")
        raise

# Performance monitoring middleware
@app.middleware("http")
async def performance_middleware(request: Request, call_next):
    """Track request performance"""
    start_time = time.time()
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        # Record successful request
        performance_monitor.record_request(duration, success=True)
        
        # Add performance headers
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        response.headers["X-Request-ID"] = str(id(request))
        
        return response
        
    except Exception as e:
        duration = time.time() - start_time
        
        # Record failed request
        performance_monitor.record_request(duration, success=False)
        
        logger.error(f"Request failed after {duration:.3f}s: {e}")
        raise

# Include all domain routers
app.include_router(auth_router)
app.include_router(discovery_router)
app.include_router(intelligence_router)
app.include_router(real_time_router)
app.include_router(streaming_router)
app.include_router(credibility_router)

# Include orchestration layer
app.include_router(orchestration_router)

# Include chat domain
app.include_router(chat_router)

# Core API endpoints
@app.get("/")
async def root():
    return {
        "message": "Luciq API v2.1-refactored - SaaS Idea Discovery Engine", 
        "status": "operational",
        "architecture": "domain-driven",
        "domains": ["auth", "discovery", "intelligence", "streaming", "credibility", "orchestration", "chat"]
    }

@app.get("/viewer")
async def discovery_viewer():
    """Serve the discovery viewer HTML interface"""
    html_file = Path("discovery-viewer.html")
    if html_file.exists():
        return FileResponse(html_file, media_type="text/html")
    else:
        raise HTTPException(status_code=404, detail="Discovery viewer not found")

@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    health_data = metrics_service.get_health_check()
    status_code = 200 if health_data["status"] == "healthy" else 503
    return JSONResponse(content=health_data, status_code=status_code)

@app.get("/metrics")
async def get_metrics():
    """Get API metrics"""
    return metrics_service.get_metrics()

# User profile endpoint
@app.get("/api/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return current_user

# Development endpoint for auto-verifying test users
@app.post("/api/dev/verify-test-users")
async def verify_test_users():
    """Auto-verify test users for development (NOT for production)"""
    try:
        from src.shared.database.connection import db_service
        
        # Get all users
        users = await db_service.get_all_users()
        verified_count = 0
        
        for user in users:
            if not user.get("email_verified", False):
                await db_service.verify_user_email(user["user_id"])
                verified_count += 1
        
        logger.info(f"Auto-verified {verified_count} test users")
        
        return {
            "success": True,
            "message": f"Auto-verified {verified_count} test users",
            "total_users": len(users),
            "verified_count": verified_count
        }
        
    except Exception as e:
        logger.error(f"Auto-verification failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Auto-verification failed: {str(e)}")

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    logger.info("Luciq API v2.1-refactored starting up...")
    logger.info("✅ Domain-driven architecture loaded")
    logger.info("✅ Authentication domain ready")
    logger.info("✅ Discovery domain ready")
    logger.info("✅ Intelligence domain ready")
    logger.info("✅ Streaming domain ready")
    logger.info("✅ Credibility domain ready")
    logger.info("✅ Orchestration layer ready")
    logger.info("🚀 Luciq API ready for discovery!")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Luciq API shutting down...")
    logger.info("Final metrics:")
    summary = metrics_service.get_startup_summary()
    for key, value in summary.items():
        logger.info(f"   {key}: {value}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT) 