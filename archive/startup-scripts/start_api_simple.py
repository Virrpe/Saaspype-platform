#!/usr/bin/env python3
"""
Simple API Startup Script for Luciq
Testing basic FastAPI functionality
"""

import sys
import os
from pathlib import Path

# Add project paths
sys.path.append('.')
sys.path.append('./src')

print("🚀 Starting Luciq API Server...")
print(f"📁 Working directory: {os.getcwd()}")
print(f"🐍 Python path: {sys.path[:3]}...")

try:
    print("📦 Importing FastAPI...")
    from fastapi import FastAPI
    
    print("📦 Importing uvicorn...")
    import uvicorn
    
    print("✅ Basic imports successful")
    
    # Create simple app
    app = FastAPI(title="Luciq API Test", version="1.0.0")
    
    @app.get("/")
    async def root():
        return {"message": "Luciq API is running", "status": "operational"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "service": "luciq-api"}
    
    print("🌐 Starting server on http://127.0.0.1:8002")
    print("📖 API docs available at http://127.0.0.1:8002/docs")
    
    # Start server
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8002,
        log_level="info",
        access_log=True
    )
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("🔧 Please install required packages: pip install fastapi uvicorn")
    sys.exit(1)
except Exception as e:
    print(f"❌ Startup error: {e}")
    sys.exit(1) 