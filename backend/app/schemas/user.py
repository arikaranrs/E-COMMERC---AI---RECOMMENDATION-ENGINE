"""
Pydantic schemas for user-related request/response validation.

Pydantic provides:
- Input validation (type checking, constraints)
- Error messages if validation fails
- Automatic documentation in OpenAPI/Swagger
- Type safety
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr = Field(..., description="User email (must be valid email format)")
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    bio: Optional[str] = Field(None, max_length=1000)


class UserRegisterRequest(UserBase):
    """
    User registration request schema.
    
    Validates:
    - Email format (EmailStr)
    - Password strength (min 8 chars, complexity)
    """
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password must be at least 8 characters"
    )
    confirm_password: str = Field(..., description="Confirm password (must match)")
    
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Validate password strength.
        
        Requirements:
        - At least 8 characters
        - Mix of upper and lower case
        - At least one digit
        - At least one special character
        
        Args:
            v: Password to validate
            
        Returns:
            str: Validated password
            
        Raises:
            ValueError: If password is weak
        """
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        if not any(c in "!@#$%^&*" for c in v):
            raise ValueError("Password must contain special character (!@#$%^&*)")
        return v
    
    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        """Ensure password and confirm_password match."""
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v


class UserLoginRequest(BaseModel):
    """User login request schema."""
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")


class UserResponse(UserBase):
    """
    User response schema (returned from API).
    
    Excludes sensitive fields like password_hash.
    Includes timestamps and account status.
    """
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    avatar_url: Optional[str]
    
    class Config:
        from_attributes = True  # Allow ORM model conversion


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    bio: Optional[str] = Field(None, max_length=1000)
    avatar_url: Optional[str] = Field(None, max_length=500)


class PasswordChangeRequest(BaseModel):
    """Schema for password change."""
    old_password: str = Field(..., description="Current password")
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="New password (must be 8+ chars)"
    )
    confirm_password: str = Field(..., description="Confirm new password")
    
    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        """Validate new password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        return v
    
    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        """Ensure passwords match."""
        if "new_password" in info.data and v != info.data["new_password"]:
            raise ValueError("Passwords do not match")
        return v


class TokenResponse(BaseModel):
    """
    JWT token response schema.
    
    Contains access token for authenticated requests
    and refresh token for getting new access tokens.
    """
    access_token: str = Field(..., description="JWT access token (use in Authorization header)")
    refresh_token: str = Field(..., description="JWT refresh token (use to get new access token)")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer')")
    expires_in: int = Field(..., description="Access token expiration in seconds")


class PasswordResetRequest(BaseModel):
    """Request for password reset."""
    email: EmailStr = Field(..., description="Email to reset password for")


class PasswordResetConfirm(BaseModel):
    """Confirm password reset with token."""
    token: str = Field(..., description="Reset token from email")
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="New password"
    )
    confirm_password: str = Field(..., description="Confirm new password")
