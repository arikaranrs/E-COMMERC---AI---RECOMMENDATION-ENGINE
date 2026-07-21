"""
JWT token utilities for authentication.

Handles creation, verification, and validation of JWT tokens.
Uses HS256 algorithm (HMAC-SHA256) for signing.

JWT (JSON Web Token) structure:
  header.payload.signature
  
Where:
  - header: {alg: "HS256", typ: "JWT"}
  - payload: {user_id, email, role, exp, iat, jti}
  - signature: HMAC-SHA256(header.payload, secret_key)

The signature ensures tokens haven't been tampered with.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import JWTError, jwt
import uuid
import logging

from app.config import settings

logger = logging.getLogger(__name__)


def create_access_token(
    user_id: int,
    email: str,
    is_admin: bool = False,
    expires_delta: Optional[timedelta] = None,
) -> tuple[str, str]:
    """
    Create JWT access token.
    
    Args:
        user_id: User's ID
        email: User's email
        is_admin: Whether user is admin
        expires_delta: Custom expiration time (defaults to settings)
        
    Returns:
        Tuple of (token, jti) where jti is JWT ID for tracking
        
    Raises:
        Exception: If token creation fails
        
    Token payload:
    {
        "user_id": 123,
        "email": "user@example.com",
        "is_admin": false,
        "exp": 1234567890,  # Unix timestamp when token expires
        "iat": 1234567000,  # Unix timestamp when token was issued
        "jti": "unique-id"  # JWT ID for token invalidation
    }
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Calculate expiration time (current UTC + delta)
    now = datetime.now(timezone.utc)
    expires = now + expires_delta
    
    # Generate unique JWT ID (for token invalidation tracking)
    jti = str(uuid.uuid4())
    
    # Build token payload
    payload = {
        "user_id": user_id,
        "email": email,
        "is_admin": is_admin,
        "exp": expires,  # Expiration time
        "iat": now,      # Issued at time
        "jti": jti,      # JWT ID (unique identifier)
    }
    
    try:
        # Sign token with secret key using HS256 algorithm
        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        logger.info(f"Access token created for user {user_id}")
        return token, jti
    except JWTError as e:
        logger.error(f"Failed to create access token: {str(e)}")
        raise


def create_refresh_token(user_id: int) -> str:
    """
    Create JWT refresh token.
    
    Refresh tokens:
    - Have longer expiration (days instead of minutes)
    - Used to get new access tokens without re-authenticating
    - Should be stored securely (httpOnly cookie)
    
    Args:
        user_id: User's ID
        
    Returns:
        Refresh token string
    """
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    now = datetime.now(timezone.utc)
    expires = now + expires_delta
    
    payload = {
        "user_id": user_id,
        "type": "refresh",
        "exp": expires,
        "iat": now,
    }
    
    try:
        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        logger.info(f"Refresh token created for user {user_id}")
        return token
    except JWTError as e:
        logger.error(f"Failed to create refresh token: {str(e)}")
        raise


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify JWT token and extract claims.
    
    Args:
        token: JWT token to verify
        
    Returns:
        Token payload (claims)
        
    Raises:
        JWTError: If token is invalid, expired, or signature doesn't match
        
    Security:
    - Verifies signature using secret key
    - Checks expiration time
    - Raises error if token tampered with
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError as e:
        logger.warning(f"Token verification failed: {str(e)}")
        raise


def extract_token_from_header(authorization_header: Optional[str]) -> Optional[str]:
    """
    Extract JWT token from Authorization header.
    
    Expected format: "Bearer <token>"
    
    Args:
        authorization_header: Value of Authorization header
        
    Returns:
        Token string or None if not found or invalid format
    """
    if not authorization_header:
        return None
    
    try:
        scheme, token = authorization_header.split()
        if scheme.lower() != "bearer":
            logger.warning(f"Invalid authorization scheme: {scheme}")
            return None
        return token
    except ValueError:
        logger.warning(f"Invalid authorization header format")
        return None


def get_token_user_id(token: str) -> Optional[int]:
    """
    Extract user ID from token.
    
    Args:
        token: JWT token
        
    Returns:
        User ID or None if invalid
    """
    try:
        payload = verify_token(token)
        return payload.get("user_id")
    except JWTError:
        return None


def is_token_expired(token: str) -> bool:
    """
    Check if token is expired without raising exception.
    
    Args:
        token: JWT token to check
        
    Returns:
        True if expired, False if valid
    """
    try:
        payload = verify_token(token)
        # If we get here, token is valid and not expired
        return False
    except JWTError:
        # Any JWT error means token is invalid/expired
        return True
