"""
Luciq Authentication Router
Extracted from master_luciq_api.py - Phase 2 Core Architecture Refactoring

Handles user registration, login, and authentication endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import timedelta

from src.services.auth_service import AuthService
from src.services.database_service import MasterDatabaseService

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Dependency injection
def get_db_service():
    return MasterDatabaseService()

def get_auth_service():
    return AuthService(get_db_service())

@router.post("/register", response_model=dict)
async def register_user(user: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    """Register a new user"""
    try:
        user_id = await auth_service.create_user(user.username, user.email, user.password)
        if user_id:
            return {"message": "User created successfully", "user_id": user_id}
        else:
            raise HTTPException(status_code=400, detail="Failed to create user")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login_user(user: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    """Login user and return JWT token"""
    authenticated_user = await auth_service.authenticate_user(user.username, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token_expires = timedelta(minutes=30)
    access_token = auth_service.create_access_token(
        data={"sub": authenticated_user["username"]}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_auth_service().get_current_user)):
    """Get current user information"""
    return {
        "username": current_user["username"],
        "email": current_user["email"],
        "created_at": current_user["created_at"]
    } 