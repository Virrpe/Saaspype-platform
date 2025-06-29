"""
Luciq Authentication Service
Extracted from master_luciq_api.py - Phase 2 Core Architecture Refactoring

Handles user authentication, JWT tokens, and password management
"""

import jwt
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .database_service import MasterDatabaseService
from config import settings

logger = logging.getLogger(__name__)

class AuthService:
    """Authentication service for user management and JWT tokens"""
    
    def __init__(self, db_service: MasterDatabaseService):
        self.db_service = db_service
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.security = HTTPBearer()
    
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        """Get current user from JWT token"""
        try:
            payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        user = await self.db_service.get_user_by_username(username=username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    
    async def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user with username and password"""
        user = await self.db_service.get_user_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user["password_hash"]):
            return None
        return user
    
    async def create_user(self, username: str, email: str, password: str) -> Optional[int]:
        """Create a new user account"""
        try:
            password_hash = self.hash_password(password)
            user_id = await self.db_service.create_user(username, email, password_hash)
            return user_id
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            return None 