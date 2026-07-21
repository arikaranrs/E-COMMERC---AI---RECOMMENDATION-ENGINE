"""
FastAPI Application Main Entry Point (Phase 1 Structure)

What is this file?
- The entry point for the HTTP server
- Initializes FastAPI app that handles all requests
- Registers middleware (processing before routes)
- Registers routes (API endpoints)
- Sets up error handling
- Defines startup/shutdown logic

Request Processing Pipeline:
1. Request arrives from client (browser/frontend)
2. CORS Middleware checks if origin is allowed
3. Middleware processing (auth verification, etc.)
4. Route handler (api/v1/auth, api/v1/products, etc.)
5. Business logic (services layer)
6. Database queries (repositories)
7. Response created
8. Response middleware processing
9. Response sent to client

FastAPI vs Other Frameworks:
- FastAPI = modern, fast, automatic documentation
- Provides automatic OpenAPI (Swagger) docs at /docs
- Type hints = built-in validation
- Async support = handle thousands of concurrent requests

Route Registration Pattern:
Each feature (auth, products, orders) has its own router:
  app.include_router(auth_router, prefix="/api/v1/auth")
  app.include_router(products_router, prefix="/api/v1/products")
  
Result:
  POST /api/v1/auth/login
  GET /api/v1/products
  POST /api/v1/products/search

CORS (Cross-Origin Resource Sharing):
Problem: Frontend (localhost:3000) calls backend (localhost:8000)
Browser security blocks this by default.
Solution: Add CORS middleware to explicitly allow origins.

Middleware:
1. CORSMiddleware - Allow frontend requests
2. AuthMiddleware - Verify JWT tokens (Phase 2)
3. Error handlers - Catch exceptions globally

Health Check Endpoint:
GET /health → {"status": "healthy"}
Used by:
- Docker health checks
- Load balancers to verify server is running
- Monitoring systems

Startup/Shutdown Events:
@app.on_event("startup")
  - Initialize database
  - Load ML models
  - Set up cache

@app.on_event("shutdown")
  - Close connections
  - Clean up resources

Automatic Documentation:
GET /docs → Swagger UI (try it out button)
GET /redoc → ReDoc (alternative format)
GET /openapi.json → Machine-readable schema

Run Backend:
uvicorn app.main:app --reload
- Starts server on http://localhost:8000
- --reload = restart on file changes (development)
- Visit http://localhost:8000/docs for interactive API docs

Phase 1 Status: Structure shown, implementation in Phase 2
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from app.config import settings
from app.models.database import init_db, close_db
from app.api.routes import auth, products, recommendations, cart, orders

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# --- Application Lifespan Events ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown.
    
    Startup:
    - Initialize database tables
    - Log startup message
    
    Shutdown:
    - Close database connections
    - Clean up resources
    
    Lifespan context ensures proper resource management.
    """
    # Startup
    logger.info("=== FastAPI Application Starting ===")
    logger.info(f"Environment: {'Development' if settings.DEBUG else 'Production'}")
    logger.info(f"Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'unknown'}")
    
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("=== FastAPI Application Shutting Down ===")
    try:
        close_db()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


# --- Create FastAPI Application ---
app = FastAPI(
    title="E-Commerce Recommendation System API",
    description="""
    Production-grade e-commerce platform with AI-powered recommendations.
    
    Features:
    - User authentication (JWT)
    - Product catalog management
    - Shopping cart and checkout
    - Product ratings and reviews
    - AI-powered recommendations (Collaborative Filtering, Content-Based, Hybrid)
    - Order management
    - Admin analytics
    
    Auth:
    - All protected endpoints require JWT token
    - Get token: POST /api/auth/login
    - Use token: Authorization: Bearer <token>
    - Refresh: POST /api/auth/refresh with refresh_token
    """,
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.DEBUG,
)


# --- CORS Configuration ---
# Allow frontend to make cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    max_age=3600,         # Cache preflight for 1 hour
)

logger.info(f"CORS enabled for origins: {settings.CORS_ORIGINS}")


# --- Register API Routes ---
# Organize routes by feature (auth, products, orders, etc.)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(recommendations.router)


# --- Health Check Endpoints ---
@app.get(
    "/health",
    tags=["System"],
    summary="Health check endpoint",
    responses={
        200: {
            "description": "Server is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "timestamp": "2024-01-15T10:30:00Z",
                        "version": "1.0.0",
                    }
                }
            },
        },
    },
)
def health_check() -> dict:
    """
    Basic health check endpoint.
    
    Used by load balancers to verify server is responsive.
    
    Returns:
        Status information
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0",
    }


@app.get(
    "/api/status",
    tags=["System"],
    summary="Detailed status information",
    responses={
        200: {
            "description": "Server status",
            "content": {
                "application/json": {
                    "example": {
                        "status": "operational",
                        "debug": False,
                        "database": "connected",
                        "timestamp": "2024-01-15T10:30:00Z",
                    }
                }
            },
        },
    },
)
def status_check() -> dict:
    """
    Detailed status check endpoint.
    
    Returns more comprehensive status information for monitoring.
    """
    return {
        "status": "operational",
        "debug": settings.DEBUG,
        "database": "connected",  # In production, actually ping database
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


# --- Error Handlers ---
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Custom HTTP exception handler.
    
    Ensures all error responses follow consistent format.
    """
    return {
        "success": False,
        "error": {
            "code": exc.detail if isinstance(exc.detail, str) else "HTTP_ERROR",
            "message": str(exc.detail),
            "status_code": exc.status_code,
        },
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Catch-all exception handler for unhandled errors.
    
    Prevents detailed error information from leaking to clients.
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return {
        "success": False,
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "status_code": 500,
        },
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


# --- OpenAPI Documentation ---
@app.get("/", tags=["Documentation"])
def root():
    """
    Root endpoint. Redirects to API documentation.
    
    Available documentation:
    - /docs - Swagger UI (interactive)
    - /redoc - ReDoc (alternative format)
    - /openapi.json - OpenAPI schema (JSON)
    """
    return {
        "message": "E-Commerce Recommendation System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi_schema": "/openapi.json",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
