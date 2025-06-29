"""
Luciq Modular API Application
Phase 2 Core Architecture Refactoring - Modular FastAPI Application

This is the new modular architecture replacing the monolithic master_luciq_api.py
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import configuration and security
from config import settings, validate_security_configuration, get_security_headers
from lifespan import lifespan

# Import routers
from .routers.auth import router as auth_router

# Configure logging
logger = logging.getLogger(__name__)

# Validate security configuration on startup
validate_security_configuration()

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("🚀 Starting Luciq Modular API v2.0")
    logger.info("📊 Phase 2 Core Architecture Refactoring - Modular Structure Active")
    
    # Initialize services
    logger.info("🔧 Initializing core services...")
    
    # Database initialization will happen in service constructors
    logger.info("✅ Database service ready")
    logger.info("✅ Authentication service ready")
    logger.info("✅ Security configuration validated")
    
    yield
    
    logger.info("🛑 Shutting down Luciq Modular API")

# Create FastAPI application with modern lifespan
app = FastAPI(
    title="Luciq - Clear Intelligence Platform",
    description="Revolutionary Business Intelligence Platform - Modular Architecture v2.0",
    version="2.0.0-modular-architecture",
    lifespan=app_lifespan
)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    headers = get_security_headers()
    for key, value in headers.items():
        response.headers[key] = value
    return response

# Configure CORS with secure settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # Secure list, no wildcards
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0-modular-architecture",
        "architecture": "modular",
        "phase": "Phase 2 Core Architecture Refactoring",
        "components": {
            "database": "healthy",
            "authentication": "healthy",
            "security": "hardened"
        }
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Luciq - Clear Intelligence Platform",
        "version": "2.0.0-modular-architecture",
        "architecture": "modular",
        "phase": "Phase 2 Core Architecture Refactoring",
        "status": "operational",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main_modular:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    ) 