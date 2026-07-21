"""
Database configuration and base model.

This module sets up SQLAlchemy engine and session management.
Follows repository pattern for data access.
"""

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import Generator
import logging

from app.config import settings

logger = logging.getLogger(__name__)

if settings.DATABASE_URL.startswith("sqlite"):
    engine: Engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.SQLALCHEMY_ECHO,
        connect_args={"check_same_thread": False},
    )
else:
    engine: Engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.SQLALCHEMY_ECHO,
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=40,
        connect_args={"charset": "utf8mb4"},
    )

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for all models
# All SQLAlchemy models inherit from Base
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency injection for database sessions.
    
    Usage in FastAPI route:
        @app.get("/items/")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    
    Ensures:
    - Session is created before request
    - Session is properly closed after request (even on error)
    - Automatic transaction rollback on exception
    
    Yields:
        Session: SQLAlchemy session for database operations
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables.
    
    This should be called once during application startup.
    In production, use Alembic migrations instead.
    """
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")


def close_db():
    """
    Close database connection.
    
    Should be called during application shutdown.
    """
    engine.dispose()
    logger.info("Database connections closed")
