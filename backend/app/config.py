"""
Configuration Management (Phase 1 Structure)

Centralized configuration for the backend application.

Why Separate Config?
✓ Change settings without editing code
✓ Different settings per environment (dev, test, production)
✓ Keep secrets out of source code (password, JWT secret)
✓ Easy to deploy to different servers

Configuration Categories:
1. Database - Where to connect for data
2. JWT - Secret key for authentication tokens
3. CORS - Which frontend URLs can call backend
4. Logging - How verbose to be
5. Cache - Redis for performance
6. Email - SMTP for sending emails
7. ML Models - Path to saved models

Environment Variables:
DATABASE_URL: MySQL connection string
JWT_SECRET: Secret for signing tokens
CORS_ORIGINS: Allowed frontend URLs
LOG_LEVEL: DEBUG, INFO, WARNING, ERROR

Example .env file:
DATABASE_URL=mysql+pymysql://root:password@localhost/ecommerce
JWT_SECRET=my-secret-key-minimum-32-characters
CORS_ORIGINS=http://localhost:3000,https://example.com

Load in code:
from app.config import settings
print(settings.database_url)
print(settings.jwt_secret)

Phase 1 Status: Structure shown, implementation in Phase 2
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All configuration should be externalized here for flexibility
    across development, testing, and production environments.
    """
    
    # --- Database Configuration ---
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/ecommerce_db"
    SQLALCHEMY_ECHO: bool = False
    
    # --- JWT Configuration ---
    SECRET_KEY: str = "change-me-in-production-minimum-32-characters-required"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # --- CORS Configuration ---
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
    ]
    
    # --- Server Configuration ---
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # --- Logging ---
    LOG_LEVEL: str = "INFO"
    
    # --- Redis Configuration ---
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL_SECONDS: int = 86400  # 24 hours
    
    # --- Email Configuration ---
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    
    # --- ML Model Configuration ---
    MODEL_PATH: str = "/app/ml/models"
    MODEL_VERSION: str = "v1.0.0"
    
    # --- Pagination ---
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # --- Rate Limiting ---
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    
    class Config:
        """Pydantic config for reading .env file."""
        env_file = ".env"
        case_sensitive = True


# Initialize settings
settings = Settings()


def get_settings() -> Settings:
    """
    Dependency injection function to get settings.
    
    This allows for easy mocking in tests and provides
    a single source of truth for configuration.
    
    Returns:
        Settings: Application settings instance
    """
    return settings
