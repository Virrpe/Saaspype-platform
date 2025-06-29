"""
User Model
SQLAlchemy model for user management and authentication
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
import uuid

Base = declarative_base()

class User(Base):
    """User model for authentication and profile management"""
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # User identification
    user_id = Column(String(36), unique=True, index=True, nullable=False)  # UUID
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=True)
    
    # Authentication
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Profile information
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    display_name = Column(String(100), nullable=True)
    
    # Account management
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    login_count = Column(Integer, default=0, nullable=False)
    
    # Security and verification
    verification_token = Column(String(255), nullable=True)
    verification_sent_at = Column(DateTime(timezone=True), nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    password_reset_sent_at = Column(DateTime(timezone=True), nullable=True)
    
    # User preferences and settings
    preferences = Column(Text, nullable=True)  # JSON string for user preferences
    
    def __init__(self, email: str, password_hash: str, **kwargs):
        """Initialize user with required fields"""
        self.user_id = str(uuid.uuid4())
        self.email = email.lower().strip()
        self.password_hash = password_hash
        
        # Set optional fields
        self.username = kwargs.get('username')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.display_name = kwargs.get('display_name')
        self.is_active = kwargs.get('is_active', True)
        self.is_verified = kwargs.get('is_verified', False)
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, user_id={self.user_id}, email={self.email})>"
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """
        Convert user to dictionary representation
        
        Args:
            include_sensitive: Whether to include sensitive fields
            
        Returns:
            User data as dictionary
        """
        user_dict = {
            "id": self.id,
            "user_id": self.user_id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "display_name": self.display_name,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "login_count": self.login_count
        }
        
        if include_sensitive:
            user_dict.update({
                "password_hash": self.password_hash,
                "verification_token": self.verification_token,
                "verification_sent_at": self.verification_sent_at.isoformat() if self.verification_sent_at else None,
                "password_reset_token": self.password_reset_token,
                "password_reset_sent_at": self.password_reset_sent_at.isoformat() if self.password_reset_sent_at else None,
                "preferences": self.preferences
            })
        
        return user_dict
    
    def get_display_name(self) -> str:
        """Get the best available display name for the user"""
        if self.display_name:
            return self.display_name
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.first_name:
            return self.first_name
        if self.username:
            return self.username
        return self.email.split('@')[0]  # Use email prefix as fallback
    
    def update_last_login(self) -> None:
        """Update last login timestamp and increment login count"""
        self.last_login = datetime.now(timezone.utc)
        self.login_count += 1
    
    def is_verification_token_valid(self, token: str, max_age_hours: int = 24) -> bool:
        """
        Check if verification token is valid and not expired
        
        Args:
            token: Token to validate
            max_age_hours: Maximum age of token in hours
            
        Returns:
            True if token is valid, False otherwise
        """
        if not self.verification_token or self.verification_token != token:
            return False
        
        if not self.verification_sent_at:
            return False
        
        # Check if token is expired
        max_age = timedelta(hours=max_age_hours)
        age = datetime.now(timezone.utc) - self.verification_sent_at.replace(tzinfo=timezone.utc)
        
        return age <= max_age
    
    def is_password_reset_token_valid(self, token: str, max_age_hours: int = 2) -> bool:
        """
        Check if password reset token is valid and not expired
        
        Args:
            token: Token to validate
            max_age_hours: Maximum age of token in hours
            
        Returns:
            True if token is valid, False otherwise
        """
        if not self.password_reset_token or self.password_reset_token != token:
            return False
        
        if not self.password_reset_sent_at:
            return False
        
        # Check if token is expired
        max_age = timedelta(hours=max_age_hours)
        age = datetime.now(timezone.utc) - self.password_reset_sent_at.replace(tzinfo=timezone.utc)
        
        return age <= max_age
    
    def clear_verification_token(self) -> None:
        """Clear verification token after successful verification"""
        self.verification_token = None
        self.verification_sent_at = None
        self.is_verified = True
    
    def clear_password_reset_token(self) -> None:
        """Clear password reset token after successful reset"""
        self.password_reset_token = None
        self.password_reset_sent_at = None
    
    @classmethod
    def create_user(cls, email: str, password_hash: str, **kwargs) -> 'User':
        """
        Factory method to create a new user
        
        Args:
            email: User email address
            password_hash: Hashed password
            **kwargs: Additional user fields
            
        Returns:
            New User instance
        """
        return cls(email=email, password_hash=password_hash, **kwargs)
    
    @property
    def full_name(self) -> Optional[str]:
        """Get full name if both first and last names are available"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return None
    
    @property
    def is_email_verified(self) -> bool:
        """Check if email is verified"""
        return self.is_verified
    
    @property
    def account_age_days(self) -> int:
        """Get account age in days"""
        if not self.created_at:
            return 0
        
        age = datetime.now(timezone.utc) - self.created_at.replace(tzinfo=timezone.utc)
        return age.days
    
    def can_login(self) -> bool:
        """Check if user can login (active and verified)"""
        return self.is_active and self.is_verified 