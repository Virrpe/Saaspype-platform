#!/usr/bin/env python3
"""
Luciq API Startup Script
Resolves import issues and starts the API server for development
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set environment variables
os.environ['PYTHONPATH'] = str(project_root)

# Import and run the API
if __name__ == "__main__":
    try:
        from src.api.main import app
        import uvicorn
        
        print("🚀 Starting Luciq API...")
        print(f"📂 Project root: {project_root}")
        print(f"🐍 Python path: {sys.path[0]}")
        
        uvicorn.run(
            app, 
            host="127.0.0.1", 
            port=8002,
            reload=False,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Attempting alternative import method...")
        
        # Alternative: run as module
        os.system("python -m src.api.main")
        
    except Exception as e:
        print(f"❌ Startup error: {e}")
        sys.exit(1) 