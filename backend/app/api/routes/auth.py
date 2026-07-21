"""
Authentication API routes.

Endpoints:
- POST /api/auth/register - Register new user
- POST /api/auth/login - Login with credentials
- POST /api/auth/refresh - Refresh access token
- POST /api/auth/logout - Logout and revoke token

FastAPI will automatically:
- Validate request body against Pydantic schema
- Generate OpenAPI/Swagger documentation
- Return 422 with validation errors if schema invalid
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.models.database import get_db
from app.schemas.user import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth_service import AuthService
from app.utils.jwt_utils import verify_token, extract_token_from_header, get_token_user_id
from app.models.user import User
from jose import JWTError

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
    responses={
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
        422: {"description": "Validation Error"},
    },
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="""
    Register a new user account.
    
    Requirements:
    - Email must be unique and valid format
    - Password must be at least 8 characters
    - Password must include uppercase, lowercase, digit, special char
    - Passwords must match
    
    Returns the created user profile (without password).
    """,
)
def register(
    user_data: UserRegisterRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Register new user account.
    
    Args:
        user_data: Registration data (email, password, name, etc.)
        db: Database session
        
    Returns:
        Created user profile
        
    Raises:
        HTTPException 400: If email already registered or validation fails
    """
    try:
        auth_service = AuthService(db)
        user = auth_service.register_user(user_data)
        return UserResponse.model_validate(user)
    
    except ValueError as e:
        logger.warning(f"Registration validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again.",
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login with credentials",
    description="""
    Authenticate user with email and password.
    
    Returns JWT access token and refresh token.
    
    Access token:
    - Use in Authorization header for API requests
    - Expires after 30 minutes (default)
    - Short-lived for security
    
    Refresh token:
    - Use to get new access token without re-authenticating
    - Longer expiration (7 days default)
    - Store securely in httpOnly cookie
    """,
)
def login(
    credentials: UserLoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Login user with email and password.
    
    Args:
        credentials: Email and password
        db: Database session
        
    Returns:
        TokenResponse with access_token and refresh_token
        
    Raises:
        HTTPException 401: If credentials invalid
    """
    try:
        auth_service = AuthService(db)
        user, tokens = auth_service.authenticate_user(
            email=credentials.email,
            password=credentials.password,
        )
        return tokens
    
    except ValueError as e:
        logger.warning(f"Login failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed. Please try again.",
        )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="""
    Get new access token using refresh token.
    
    Used when access token expires but refresh token is still valid.
    This allows continuing session without re-entering credentials.
    """,
)
def refresh_token(
    request_data: dict,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Refresh access token using refresh token.
    
    Args:
        request_data: Should contain "refresh_token" key
        db: Database session
        
    Returns:
        New TokenResponse with access_token
        
    Raises:
        HTTPException 401: If refresh token invalid/expired
    """
    refresh_token_str = request_data.get("refresh_token")
    
    if not refresh_token_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="refresh_token required",
        )
    
    try:
        auth_service = AuthService(db)
        tokens = auth_service.refresh_access_token(refresh_token_str)
        return tokens
    
    except ValueError as e:
        logger.warning(f"Token refresh failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed",
        )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout and revoke token",
    description="""
    Logout user and revoke token.
    
    Invalidates the provided access token so it cannot be reused.
    Client should delete tokens from storage (cookies, local storage).
    """,
)
def logout(
    authorization: Optional[str] = None,
    db: Session = Depends(get_db),
) -> dict:
    """
    Logout user by revoking token.
    
    Args:
        authorization: Authorization header value
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException 401: If token invalid/expired
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = extract_token_from_header(authorization)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = verify_token(token)
        user_id = payload.get("user_id")
        jti = payload.get("jti")
        
        if not user_id or not jti:
            raise ValueError("Invalid token")
        
        auth_service = AuthService(db)
        auth_service.revoke_token(user_id, jti)
        
        return {
            "success": True,
            "message": "Logged out successfully",
        }
    
    except JWTError as e:
        logger.warning(f"Logout failed - invalid token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed",
        )
