"""
Luciq Master API - Secure Configuration Module
Phase 1 Emergency Stabilization: Security Hardening & Environment Management
"""

import os
import secrets
from typing import List, Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """
    Secure configuration management with environment variable support.
    
    Security Improvements:
    - No hardcoded secrets
    - Environment-based configuration
    - Secure defaults
    - Validation of critical settings
    """
    
    # API Configuration
    API_HOST: str = Field(default="0.0.0.0", env="API_HOST")
    API_PORT: int = Field(default=8000, env="API_PORT")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Security Configuration - NO MORE HARDCODED SECRETS!
    SECRET_KEY: str = Field(env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # CORS Configuration - Secure by default
    CORS_ORIGINS: str = Field(default="http://localhost:3000,http://localhost:3001,http://localhost:5173", env="CORS_ORIGINS")
    
    # Database Configuration
    DATABASE_URL: str = Field(default="luciq_master.db", env="DATABASE_URL")
    
    # Reddit API Configuration
    REDDIT_CLIENT_ID: Optional[str] = Field(default=None, env="REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET: Optional[str] = Field(default=None, env="REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT: str = Field(
        default="Luciq:discovery-engine:v3.0 (by /u/luciq_bot)", 
        env="REDDIT_USER_AGENT"
    )
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_WINDOW: int = Field(default=60, env="RATE_LIMIT_WINDOW")
    
    # Environment Mode
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    
    # MVP API Key Security
    MVP_API_KEY_SALT: str = Field(env="MVP_API_KEY_SALT")
    
    # Optional External API Keys
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        """Ensure SECRET_KEY is secure"""
        if not v:
            # Generate a secure secret key if not provided
            v = secrets.token_urlsafe(32)
            print("⚠️  WARNING: Generated temporary SECRET_KEY. Set SECRET_KEY environment variable for production!")
        elif len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long for security")
        elif v == "your-secret-key-change-in-production":
            raise ValueError("🚨 SECURITY ALERT: Change the default SECRET_KEY immediately!")
        return v
    
    @validator("MVP_API_KEY_SALT")
    def validate_api_key_salt(cls, v):
        """Ensure MVP API key salt is secure"""
        if not v:
            v = secrets.token_urlsafe(16)
            print("⚠️  WARNING: Generated temporary MVP_API_KEY_SALT. Set environment variable for production!")
        return v
    
    @validator("CORS_ORIGINS")
    def validate_cors_origins(cls, v):
        """Validate and warn about insecure CORS settings"""
        if "*" in v and cls.ENVIRONMENT == "production":
            raise ValueError("🚨 SECURITY ALERT: CORS wildcard (*) not allowed in production!")
        return v
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS_ORIGINS string to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.ENVIRONMENT.lower() == "development"
    
    class Config:
        # Load from .env file if present
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()


def validate_security_configuration():
    """
    Validate critical security configuration on startup.
    Part of Phase 1 Emergency Stabilization.
    """
    warnings = []
    errors = []
    
    # Check SECRET_KEY security
    if len(settings.SECRET_KEY) < 32:
        errors.append("SECRET_KEY must be at least 32 characters long")
    
    # Check CORS configuration in production
    if settings.is_production and "*" in settings.CORS_ORIGINS:
        errors.append("CORS wildcard (*) not allowed in production")
    
    # Check if using default/insecure values
    insecure_defaults = [
        "your-secret-key-change-in-production",
        "change-me",
        "default",
        "secret"
    ]
    
    if any(default in settings.SECRET_KEY.lower() for default in insecure_defaults):
        errors.append("SECRET_KEY appears to be using default/insecure value")
    
    # Reddit API warnings
    if not settings.REDDIT_CLIENT_ID or not settings.REDDIT_CLIENT_SECRET:
        warnings.append("Reddit API credentials not configured - some discovery features may be limited")
    
    # Production mode warnings
    if settings.is_production:
        if settings.LOG_LEVEL.lower() == "debug":
            warnings.append("DEBUG logging enabled in production mode")
    
    return {"warnings": warnings, "errors": errors}


def get_security_headers():
    """
    Generate security headers for the API.
    Part of Phase 1 security hardening.
    """
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains" if settings.is_production else None,
        "Content-Security-Policy": "default-src 'self'" if settings.is_production else None
    }


# Export commonly used settings
__all__ = [
    "settings",
    "validate_security_configuration", 
    "get_security_headers",
    "Settings"
] 