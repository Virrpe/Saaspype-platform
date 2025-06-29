"""
Authentication API Endpoints
Handles user registration, login, logout, and verification
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
import logging

from src.api.domains.auth.services.auth_service import auth_service

logger = logging.getLogger(__name__)
security = HTTPBearer()

# Create router
router = APIRouter(prefix="/auth", tags=["authentication"])

# Request/Response Models
class UserRegistrationRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    username: Optional[str] = Field(None, max_length=50)

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class EmailVerificationRequest(BaseModel):
    email: EmailStr
    token: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirmRequest(BaseModel):
    email: EmailStr
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)

class TokenRefreshRequest(BaseModel):
    refresh_token: str

class LogoutRequest(BaseModel):
    refresh_token: str

class AuthResponse(BaseModel):
    success: bool
    message: str
    user: Optional[Dict[str, Any]] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_at: Optional[str] = None
    error: Optional[str] = None
    error_code: Optional[str] = None

# Helper Functions
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Get current authenticated user from JWT token
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        User data dictionary
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    user_data = auth_service.get_user_by_token(token)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user_data

# Authentication Endpoints

@router.post("/register", response_model=AuthResponse)
async def register_user(request: UserRegistrationRequest) -> AuthResponse:
    """
    Register a new user account
    
    Args:
        request: User registration data
        
    Returns:
        Registration result with user data and verification token
    """
    try:
        result = auth_service.register_user(
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name,
            username=request.username
        )
        
        if result["success"]:
            return AuthResponse(
                success=True,
                message=result["message"],
                user=result["user"]
            )
        else:
            # Determine HTTP status code based on error
            status_code = status.HTTP_400_BAD_REQUEST
            if result.get("error_code") == "EMAIL_EXISTS":
                status_code = status.HTTP_409_CONFLICT
            elif result.get("error_code") == "WEAK_PASSWORD":
                status_code = status.HTTP_400_BAD_REQUEST
            
            raise HTTPException(
                status_code=status_code,
                detail=result["error"]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed due to server error"
        )

@router.post("/login", response_model=AuthResponse)
async def login_user(request: UserLoginRequest) -> AuthResponse:
    """
    Authenticate user login
    
    Args:
        request: User login credentials
        
    Returns:
        Login result with tokens and user data
    """
    try:
        result = auth_service.login_user(
            email=request.email,
            password=request.password
        )
        
        if result["success"]:
            return AuthResponse(
                success=True,
                message=result["message"],
                user=result["user"],
                access_token=result["access_token"],
                refresh_token=result["refresh_token"],
                token_type=result["token_type"],
                expires_at=result["expires_at"]
            )
        else:
            # Determine HTTP status code based on error
            status_code = status.HTTP_401_UNAUTHORIZED
            if result.get("error_code") == "EMAIL_NOT_VERIFIED":
                status_code = status.HTTP_403_FORBIDDEN
            elif result.get("error_code") == "ACCOUNT_INACTIVE":
                status_code = status.HTTP_403_FORBIDDEN
            
            raise HTTPException(
                status_code=status_code,
                detail=result["error"]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed due to server error"
        )

@router.post("/verify-email", response_model=AuthResponse)
async def verify_email(request: EmailVerificationRequest) -> AuthResponse:
    """
    Verify user email address with verification token
    
    Args:
        request: Email verification data
        
    Returns:
        Verification result
    """
    try:
        result = auth_service.verify_email(
            email=request.email,
            token=request.token
        )
        
        if result["success"]:
            return AuthResponse(
                success=True,
                message=result["message"]
            )
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            if result.get("error_code") == "USER_NOT_FOUND":
                status_code = status.HTTP_404_NOT_FOUND
            elif result.get("error_code") == "INVALID_TOKEN":
                status_code = status.HTTP_400_BAD_REQUEST
            
            raise HTTPException(
                status_code=status_code,
                detail=result["error"]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Email verification endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email verification failed due to server error"
        )

@router.post("/refresh-token", response_model=AuthResponse)
async def refresh_token(request: TokenRefreshRequest) -> AuthResponse:
    """
    Refresh access token using refresh token
    
    Args:
        request: Token refresh data
        
    Returns:
        New token pair
    """
    try:
        result = auth_service.refresh_token(request.refresh_token)
        
        if result["success"]:
            return AuthResponse(
                success=True,
                message=result["message"],
                access_token=result["access_token"],
                refresh_token=result["refresh_token"],
                token_type=result["token_type"],
                expires_at=result["expires_at"]
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result["error"]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed due to server error"
        )

@router.post("/logout", response_model=AuthResponse)
async def logout_user(request: LogoutRequest) -> AuthResponse:
    """
    Logout user by revoking refresh token
    
    Args:
        request: Logout data with refresh token
        
    Returns:
        Logout result
    """
    try:
        result = auth_service.logout_user(request.refresh_token)
        
        return AuthResponse(
            success=True,
            message=result["message"]
        )
        
    except Exception as e:
        logger.error(f"Logout endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed due to server error"
        )

@router.post("/request-password-reset", response_model=AuthResponse)
async def request_password_reset(request: PasswordResetRequest) -> AuthResponse:
    """
    Request password reset token
    
    Args:
        request: Password reset request with email
        
    Returns:
        Reset request result
    """
    try:
        result = auth_service.request_password_reset(request.email)
        
        return AuthResponse(
            success=True,
            message=result["message"]
        )
        
    except Exception as e:
        logger.error(f"Password reset request endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset request failed due to server error"
        )

@router.post("/reset-password", response_model=AuthResponse)
async def reset_password(request: PasswordResetConfirmRequest) -> AuthResponse:
    """
    Reset user password with reset token
    
    Args:
        request: Password reset confirmation data
        
    Returns:
        Password reset result
    """
    try:
        result = auth_service.reset_password(
            email=request.email,
            token=request.token,
            new_password=request.new_password
        )
        
        if result["success"]:
            return AuthResponse(
                success=True,
                message=result["message"]
            )
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            if result.get("error_code") == "INVALID_TOKEN":
                status_code = status.HTTP_400_BAD_REQUEST
            elif result.get("error_code") == "WEAK_PASSWORD":
                status_code = status.HTTP_400_BAD_REQUEST
            
            raise HTTPException(
                status_code=status_code,
                detail=result["error"]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password reset endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset failed due to server error"
        )

@router.get("/me", response_model=Dict[str, Any])
async def get_current_user_profile(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Get current authenticated user profile
    
    Args:
        current_user: Current authenticated user (from token)
        
    Returns:
        User profile data
    """
    return current_user

@router.get("/validate-token")
async def validate_token(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Validate current access token
    
    Args:
        current_user: Current authenticated user (from token)
        
    Returns:
        Token validation result
    """
    return {
        "valid": True,
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "message": "Token is valid"
    } 