"""
API v1 Router

Registers all v1 endpoints.

This file imports all individual routers (auth, products, etc.)
and combines them into a single router that gets included in main.py

Pattern:
1. Each endpoint module (auth.py, products.py) defines its own APIRouter
2. This file imports all routers
3. Combines them into one router with prefix /api/v1
4. main.py includes this router: app.include_router(api_router)

Result: All routes become /api/v1/{endpoint}

In Phase 2+, we'll implement the actual routers here.
For now, this is just the skeleton.
"""
