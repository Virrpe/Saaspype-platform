#!/usr/bin/env python3
"""
Optimized Luciq API Startup
Disables heavy AI models for faster response times during validation
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add project paths
sys.path.append('.')
sys.path.append('./src')

# Set environment variables to optimize performance
os.environ['LUCIQ_DISABLE_HEAVY_MODELS'] = 'true'
os.environ['LUCIQ_FAST_MODE'] = 'true'
os.environ['LUCIQ_SKIP_NLP_MODELS'] = 'true'

print("🚀 Starting Luciq API in Optimized Mode...")
print("⚡ Heavy AI models disabled for faster response times")
print("📁 Working directory:", os.getcwd())

try:
    # Import the main app
    from src.api.main import app
    
    print("✅ FastAPI app imported successfully")
    print("🌐 Starting server on http://127.0.0.1:8003 (avoiding port conflict)")
    print("📖 API docs will be available at http://127.0.0.1:8003/docs")
    
    # Start server on different port to avoid conflict
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8003,
        reload=False,  # Disable reload for stability
        log_level="info",
        access_log=True
    )
    
except Exception as e:
    print(f"❌ Failed to start API server: {e}")
    print("🔍 Checking for import issues...")
    
    try:
        import fastapi
        print("✅ FastAPI available")
    except ImportError:
        print("❌ FastAPI not available")
    
    try:
        import uvicorn
        print("✅ Uvicorn available")
    except ImportError:
        print("❌ Uvicorn not available")
    
    sys.exit(1) 