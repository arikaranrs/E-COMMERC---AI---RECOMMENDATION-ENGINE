"""
API Routes Module

Contains all HTTP route handlers for the REST API.

Structure:
- v1/: API version 1 endpoints (allows multiple API versions in future)
  - __init__.py: Route registration
  - auth.py: Authentication endpoints (login, register, logout, refresh token)
  - products.py: Product management endpoints (list, search, filter, get by id)
  - cart.py: Shopping cart endpoints (add, remove, view, update)
  - orders.py: Order management endpoints (create, list, details, cancel)
  - users.py: User profile endpoints (get profile, update profile)
  - recommendations.py: AI recommendation endpoints (get personalized recommendations)

Route Registration Pattern:
1. Each feature has its own APIRouter (e.g., auth_router in auth.py)
2. v1/__init__.py imports all routers and combines them
3. main.py includes the v1 router in FastAPI app
4. Full route URL: /api/v1/{router_prefix}/{endpoint}

Example Route Structure:
- POST /api/v1/auth/login → auth.py login endpoint
- GET /api/v1/products → products.py list all products
- GET /api/v1/products/123 → products.py get specific product
- POST /api/v1/cart → cart.py add to cart
- GET /api/v1/recommendations → recommendations.py get recommendations

Why This Structure?
- Each feature is isolated and easier to test
- Routes are organized by feature, not by HTTP method
- Easy to add new features without touching existing code
- v1/ allows future API versioning (v2, v3, etc.)
"""
