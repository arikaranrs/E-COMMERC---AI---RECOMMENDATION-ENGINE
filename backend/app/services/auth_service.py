"""
Authentication service with business logic.

Handles:
- User registration
- User login
- Password hashing
- Token refresh
- Token validation

Separates auth logic from FastAPI routes for reusability and testing.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from datetime import datetime, timezone
from typing import Optional, Tuple
import logging

from app.models.user import User, Session as UserSession
from app.schemas.user import UserRegisterRequest, TokenResponse
from app.utils.jwt_utils import create_access_token, create_refresh_token, verify_token
from app.config import settings

logger = logging.getLogger(__name__)

# Password hashing context using bcrypt
# rounds=12: higher = more secure but slower (bcrypt recommendation is 12)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
)


def hash_password(password: str) -> str:
    """
    Hash password using bcrypt.
    
    Bcrypt:
    - Adds salt automatically (prevents rainbow table attacks)
    - Generates hash unique each time (stored hash checks password)
    - Computationally expensive (slows down brute force attacks)
    - Industry standard for password hashing
    
    Why bcrypt over MD5/SHA1:
    - MD5/SHA1: Fast, not designed for passwords, vulnerable to GPU attacks
    - bcrypt: Slow by design, designed for passwords, resistant to attacks
    
    Args:
        password: Plaintext password
        
    Returns:
        Hashed password (safe to store in database)
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify plaintext password against hashed password.
    
    How it works:
    1. Extract salt from stored hash
    2. Hash provided password with extracted salt
    3. Compare new hash with stored hash
    4. If match, password is correct
    
    Args:
        plain_password: User-provided password
        hashed_password: Hashed password from database
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


class AuthService:
    """
    Authentication service with business logic.
    
    Methods:
    - register_user: Create new user account
    - authenticate_user: Verify credentials and return tokens
    - refresh_access_token: Get new token using refresh token
    - revoke_token: Invalidate token (logout)
    """
    
    def __init__(self, db: Session):
        """
        Initialize auth service with database session.
        
        Args:
            db: SQLAlchemy session for database operations
        """
        self.db = db
    
    def register_user(self, user_data: UserRegisterRequest) -> User:
        """
        Register new user.
        
        Process:
        1. Validate email not already registered
        2. Hash password using bcrypt
        3. Create user record in database
        4. Return user object
        
        Args:
            user_data: Registration request with email, password, etc.
            
        Returns:
            Created User object
            
        Raises:
            ValueError: If email already registered
            IntegrityError: If database constraint violated
        """
        # Check if user already exists
        existing_user = self.db.query(User).filter(
            User.email == user_data.email
        ).first()
        
        if existing_user:
            logger.warning(f"Registration attempt with existing email: {user_data.email}")
            raise ValueError(f"Email {user_data.email} already registered")
        
        # Create new user with hashed password
        user = User(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
            is_active=True,
            is_admin=False,
        )
        
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            logger.info(f"User registered successfully: {user.email}")
            return user
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Database error during registration: {str(e)}")
            raise ValueError("Registration failed. Please try again.")
    
    def authenticate_user(self, email: str, password: str) -> Tuple[User, TokenResponse]:
        """
        Authenticate user with email and password.
        
        Process:
        1. Find user by email
        2. Verify password matches hash
        3. Create access and refresh tokens
        4. Store session in database (for logout/invalidation)
        5. Return user and tokens
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Tuple of (user, token_response)
            
        Raises:
            ValueError: If email not found or password incorrect
        """
        # Find user by email
        user = self.db.query(User).filter(User.email == email).first()
        
        if not user:
            logger.warning(f"Login attempt with non-existent email: {email}")
            raise ValueError("Invalid email or password")
        
        # Check if user account is active
        if not user.is_active:
            logger.warning(f"Login attempt for inactive user: {email}")
            raise ValueError("User account is inactive")
        
        # Verify password
        if not verify_password(password, user.password_hash):
            logger.warning(f"Failed login attempt for user: {email}")
            raise ValueError("Invalid email or password")
        
        # Create tokens
        access_token, jti = create_access_token(
            user_id=user.id,
            email=user.email,
            is_admin=user.is_admin,
        )
        refresh_token = create_refresh_token(user_id=user.id)
        
        # Store session in database (for token revocation tracking)
        expires_at = datetime.now(timezone.utc) + \
            __import__('datetime').timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        session = UserSession(
            user_id=user.id,
            token_jti=jti,
            expires_at=expires_at,
        )
        
        self.db.add(session)
        self.db.commit()
        
        logger.info(f"User logged in successfully: {email}")
        
        # Return user and tokens
        return user, TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
    
    def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """
        Create new access token using refresh token.
        
        How it works:
        1. Verify refresh token is valid
        2. Extract user_id from token
        3. Create new access token
        4. Return new access token
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            New access token in TokenResponse
            
        Raises:
            ValueError: If refresh token is invalid or expired
        """
        try:
            payload = verify_token(refresh_token)
            
            # Check token is refresh token type
            if payload.get("type") != "refresh":
                raise ValueError("Invalid token type")
            
            user_id = payload.get("user_id")
            if not user_id:
                raise ValueError("Invalid token")
            
            # Fetch user to get current details
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError("User not found")
            
            # Create new access token
            access_token, jti = create_access_token(
                user_id=user.id,
                email=user.email,
                is_admin=user.is_admin,
            )
            
            # Store new session
            expires_at = datetime.now(timezone.utc) + \
                __import__('datetime').timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            
            session = UserSession(
                user_id=user.id,
                token_jti=jti,
                expires_at=expires_at,
            )
            
            self.db.add(session)
            self.db.commit()
            
            logger.info(f"Access token refreshed for user: {user_id}")
            
            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,  # Same refresh token
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            )
        
        except Exception as e:
            logger.warning(f"Token refresh failed: {str(e)}")
            raise ValueError("Invalid or expired refresh token")
    
    def revoke_token(self, user_id: int, jti: str) -> bool:
        """
        Revoke (invalidate) a token.
        
        Used during logout to prevent token reuse.
        
        Args:
            user_id: User ID
            jti: JWT ID to revoke
            
        Returns:
            True if revocation successful
        """
        try:
            # Delete session with matching JTI
            self.db.query(UserSession).filter(
                UserSession.user_id == user_id,
                UserSession.token_jti == jti,
            ).delete()
            self.db.commit()
            logger.info(f"Token revoked for user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to revoke token: {str(e)}")
            self.db.rollback()
            return False
