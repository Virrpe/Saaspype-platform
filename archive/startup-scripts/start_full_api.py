#!/usr/bin/env python3
"""
Full Luciq API Startup
Complete API with all domains including orchestration layer
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add project paths
sys.path.append('.')
sys.path.append('./src')

print("🚀 Starting Luciq API in FULL Mode...")
print("🎯 All domains enabled: auth, discovery, intelligence, streaming, credibility, orchestration, chat")
print("📁 Working directory:", os.getcwd())

try:
    # Import the complete FastAPI app from main.py
    from src.api.main import app
    
    print("✅ Full FastAPI app imported successfully")
    print("🏗️ Domain-driven architecture loaded")
    print("🎼 Orchestration layer included")
    print("🌐 Starting server on http://127.0.0.1:8002 (full API)")
    print("📖 API docs will be available at http://127.0.0.1:8002/docs")
    
    # Run the full API
    uvicorn.run(app, host="127.0.0.1", port=8002)
    
except Exception as e:
    print(f"❌ Failed to start full API: {e}")
    sys.exit(1) 