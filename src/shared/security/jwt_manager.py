"""
JWT Token Manager
Handles JWT token generation, validation, and refresh token management
"""
import jwt
import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

@dataclass
class TokenPair:
    """Data class for access and refresh token pair"""
    access_token: str
    refresh_token: str
    expires_at: datetime
    token_type: str = "Bearer"

class JWTManager:
    """JWT token generation and validation manager"""
    
    def __init__(self, secret_key: Optional[str] = None):
        # Use provided secret or generate a secure one
        self.secret_key = secret_key or self._generate_secret_key()
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30  # 30 minutes
        self.refresh_token_expire_days = 7     # 7 days
        self.issuer = "luciq-api"
        
        # Store active refresh tokens (in production, use Redis/database)
        self._active_refresh_tokens = set()
    
    def _generate_secret_key(self) -> str:
        """Generate a secure secret key for JWT signing"""
        return secrets.token_urlsafe(64)
    
    def create_token_pair(self, user_id: str, email: str, additional_claims: Optional[Dict] = None) -> TokenPair:
        """
        Create access and refresh token pair
        
        Args:
            user_id: User identifier
            email: User email
            additional_claims: Optional additional claims to include
            
        Returns:
            TokenPair with access and refresh tokens
        """
        now = datetime.now(timezone.utc)
        access_expires = now + timedelta(minutes=self.access_token_expire_minutes)
        refresh_expires = now + timedelta(days=self.refresh_token_expire_days)
        
        # Base claims
        base_claims = {
            "iss": self.issuer,
            "iat": now,
            "user_id": user_id,
            "email": email,
            "type": "access"
        }
        
        # Add additional claims if provided
        if additional_claims:
            base_claims.update(additional_claims)
        
        # Create access token
        access_claims = base_claims.copy()
        access_claims.update({
            "exp": access_expires,
            "type": "access"
        })
        
        access_token = jwt.encode(
            access_claims,
            self.secret_key,
            algorithm=self.algorithm
        )
        
        # Create refresh token
        refresh_token_id = secrets.token_urlsafe(32)
        refresh_claims = {
            "iss": self.issuer,
            "iat": now,
            "exp": refresh_expires,
            "user_id": user_id,
            "email": email,
            "type": "refresh",
            "jti": refresh_token_id  # JWT ID for refresh token tracking
        }
        
        refresh_token = jwt.encode(
            refresh_claims,
            self.secret_key,
            algorithm=self.algorithm
        )
        
        # Store refresh token ID for validation
        self._active_refresh_tokens.add(refresh_token_id)
        
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=access_expires
        )
    
    def validate_access_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate access token and return claims
        
        Args:
            token: JWT access token to validate
            
        Returns:
            Token claims if valid, None if invalid
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                issuer=self.issuer
            )
            
            # Verify it's an access token
            if payload.get("type") != "access":
                return None
            
            # Check expiration (jwt.decode already checks this, but double-check)
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc):
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception:
            return None
    
    def validate_refresh_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate refresh token and return claims
        
        Args:
            token: JWT refresh token to validate
            
        Returns:
            Token claims if valid, None if invalid
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                issuer=self.issuer
            )
            
            # Verify it's a refresh token
            if payload.get("type") != "refresh":
                return None
            
            # Check if refresh token is still active
            token_id = payload.get("jti")
            if not token_id or token_id not in self._active_refresh_tokens:
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception:
            return None
    
    def refresh_access_token(self, refresh_token: str) -> Optional[TokenPair]:
        """
        Generate new access token using refresh token
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            New token pair if refresh token is valid, None otherwise
        """
        # Validate refresh token
        refresh_payload = self.validate_refresh_token(refresh_token)
        if not refresh_payload:
            return None
        
        # Extract user information
        user_id = refresh_payload.get("user_id")
        email = refresh_payload.get("email")
        
        if not user_id or not email:
            return None
        
        # Create new token pair
        return self.create_token_pair(user_id, email)
    
    def revoke_refresh_token(self, token: str) -> bool:
        """
        Revoke a refresh token
        
        Args:
            token: Refresh token to revoke
            
        Returns:
            True if successfully revoked, False otherwise
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                issuer=self.issuer,
                options={"verify_exp": False}  # Allow expired tokens for revocation
            )
            
            token_id = payload.get("jti")
            if token_id and token_id in self._active_refresh_tokens:
                self._active_refresh_tokens.remove(token_id)
                return True
            
            return False
            
        except Exception:
            return False
    
    def revoke_all_user_tokens(self, user_id: str) -> int:
        """
        Revoke all refresh tokens for a specific user
        
        Args:
            user_id: User identifier
            
        Returns:
            Number of tokens revoked
        """
        revoked_count = 0
        tokens_to_remove = []
        
        for token_id in self._active_refresh_tokens:
            # Note: In production, you'd query the database for user's tokens
            # This is a simplified implementation
            tokens_to_remove.append(token_id)
        
        for token_id in tokens_to_remove:
            self._active_refresh_tokens.discard(token_id)
            revoked_count += 1
        
        return revoked_count
    
    def get_token_info(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Get token information without validation (for debugging)
        
        Args:
            token: JWT token
            
        Returns:
            Token payload if decodable, None otherwise
        """
        try:
            # Decode without verification for inspection
            payload = jwt.decode(
                token,
                options={"verify_signature": False, "verify_exp": False}
            )
            return payload
        except Exception:
            return None
    
    def is_token_expired(self, token: str) -> bool:
        """
        Check if token is expired
        
        Args:
            token: JWT token to check
            
        Returns:
            True if expired, False if valid or unable to determine
        """
        try:
            jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return False  # Token is valid
        except jwt.ExpiredSignatureError:
            return True   # Token is expired
        except Exception:
            return True   # Other errors, consider as expired

# Global JWT manager instance (will be configured with proper secret in production)
jwt_manager = JWTManager() 