#!/usr/bin/env python3
"""
Luciq API v2.1 Startup Script
Clean architecture with service-based design
"""

import sys
import os
import uvicorn
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Start the Luciq API server"""
    print("Starting Luciq API v2.1...")
    print("Using clean architecture with service-based design")
    print("Configuration: Environment-based settings")
    print("Database: Centralized connection management")
    print("Security: JWT-based authentication")
    print("Discovery: Reddit scraping with spam detection")
    
    try:
        # Import after path setup
        from api.main import app
        from shared.config.settings import API_HOST, API_PORT
        
        print(f"Starting server on http://{API_HOST}:{API_PORT}")
        print("API Documentation: http://localhost:8000/docs")
        print("Health Check: http://localhost:8000/health")
        print("Metrics: http://localhost:8000/metrics")
        print("\nLuciq API v2.1 ready for discovery!")
        
        uvicorn.run(
            app,
            host=API_HOST,
            port=API_PORT,
            log_level="info",
            reload=False
        )
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure you're running from the project root directory")
        sys.exit(1)
    except Exception as e:
        print(f"Startup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 