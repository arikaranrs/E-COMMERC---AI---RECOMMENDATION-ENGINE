"""
User model and related tables.

Represents users in the e-commerce system with authentication,
profile, and preference management.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.database import Base


class User(Base):
    """
    User model for authentication and profile management.
    
    Attributes:
        id: Unique user identifier (Primary Key)
        email: User email (unique, used for login)
        password_hash: Bcrypt hashed password (never store plaintext)
        first_name: User's first name
        last_name: User's last name
        phone: User's phone number
        avatar_url: URL to user's avatar image
        bio: User's biography/about section
        is_active: Whether user account is active
        is_admin: Whether user has admin privileges
        created_at: Account creation timestamp
        updated_at: Last profile update timestamp
    
    Relationships:
        orders: User's orders (one-to-many)
        ratings: User's product ratings
        reviews: User's product reviews
        wishlist: User's wishlist items
        cart: User's shopping cart
    """
    
    __tablename__ = "users"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Authentication Fields
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile Fields
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    avatar_url = Column(String(500))
    bio = Column(Text)
    
    # Account Status
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships (lazy loading by default)
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    cart = relationship("Cart", back_populates="user", uselist=False, cascade="all, delete-orphan")
    activity = relationship("UserActivity", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.first_name} {self.last_name})>"
    
    def get_full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated and active."""
        return self.is_active


class Session(Base):
    """
    Session tracking for JWT token management.
    
    Allows invalidation of tokens (logout) by maintaining
    a blacklist of invalidated JWT tokens.
    
    Attributes:
        id: Session ID
        user_id: Reference to user
        token_jti: JWT ID (unique identifier) for token revocation
        expires_at: When this session expires
        created_at: Session creation time
    """
    
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    token_jti = Column(String(500), unique=True, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Session(user_id={self.user_id}, expires_at={self.expires_at})>"
