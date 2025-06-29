import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent.parent

# Database configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "luciq_discovery.db"))

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "luciq-discovery-secret-key-2025")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# API configuration
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Frontend configuration
FRONTEND_HOST = os.getenv("FRONTEND_HOST", "localhost")
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "3000"))

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = BASE_DIR / "logs"

# CORS configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Memory system configuration
MEMORY_DIR = BASE_DIR / "working-memory"
PROCESSED_POSTS_FILE = MEMORY_DIR / "processed-posts.json"

# Ensure directories exist
LOG_DIR.mkdir(exist_ok=True)
MEMORY_DIR.mkdir(exist_ok=True) 