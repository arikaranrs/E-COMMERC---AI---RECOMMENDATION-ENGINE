"""
Backend Application Package - FastAPI

This is the core backend API server for the e-commerce platform.
It handles all HTTP requests, business logic, and database operations.

Package Structure:
├── main.py              - FastAPI app initialization, route registration, middleware setup
├── config.py            - Configuration management (DB URLs, secrets, API settings)
├── api/                 - HTTP route handlers (organize by feature: auth, products, orders)
├── models/              - SQLAlchemy ORM models (Python classes representing database tables)
├── schemas/             - Pydantic validation schemas (request/response contracts)
├── services/            - Business logic layer (where actual work happens)
├── repositories/        - Database access layer (all SQL queries here)
├── utils/               - Helper functions (JWT, passwords, logging)
└── middleware/          - Request/response middleware (auth, CORS, error handling)

Request Flow:
1. Browser sends HTTP request → FastAPI route handler (api/)
2. Route validates request using Pydantic schema
3. Route calls service layer for business logic
4. Service calls repository for database access
5. Repository executes SQL query using SQLAlchemy models
6. Data flows back up: repository → service → route → response schema
7. Response sent to browser as JSON

Example: GET /api/v1/products
- api/v1/products.py: Route handler receives request
- product_service.py: Service fetches products with filters
- product_repository.py: Repository executes SQL query
- models/product.py: ORM maps SQL results to Python objects
- schemas/product.py: Response schema formats data for JSON
- Browser receives JSON product list
"""

__version__ = "1.0.0"
__author__ = "E-Commerce Team"
