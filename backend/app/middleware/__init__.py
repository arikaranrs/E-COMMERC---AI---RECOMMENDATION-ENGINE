"""
Request/Response Middleware

Middleware intercepts every request BEFORE it reaches route handlers
and every response BEFORE it goes to client.

Middleware Pipeline:
Request from Client
    ↓
CORS Middleware - Allow/block based on origin
    ↓
Auth Middleware - Verify JWT token (if needed)
    ↓
Error Handler Middleware - Wrap in try/catch
    ↓
Route Handler (api/)
    ↓
Response Format Middleware - Format response JSON
    ↓
Response to Client

Middleware Will Include (Phase 2+):

1. auth_middleware.py - Authentication Check
   - Verify JWT token in Authorization header
   - Extract user_id from token
   - Attach user_id to request
   - Allow route to use authenticated user
   
   Example:
   Request: GET /api/v1/profile
   Header: Authorization: Bearer eyJhbGciOiJIUzI1NiI...
   
   Middleware:
   - Extract token from header
   - Verify token signature (not tampered)
   - Decode token to get user_id
   - Attach to request.user = {"id": 123}
   - Continue to route handler

2. cors_middleware.py - Cross-Origin Requests
   - Allow frontend (different domain) to call backend
   - Specify which origins are allowed
   - Specify which methods are allowed
   - Specify which headers are allowed
   
   Example:
   Frontend: http://localhost:3000 (React development)
   Backend: http://localhost:8000 (FastAPI)
   
   Without CORS: Browser blocks requests (security)
   With CORS: Allow specific origins

3. error_handler_middleware.py - Global Error Handling
   - Catch exceptions from route handlers
   - Format errors consistently
   - Don't leak sensitive info to clients
   - Log errors for debugging
   
   Example Error Response:
   {
       "detail": "User not found",
       "status_code": 404,
       "error_type": "NotFoundError"
   }

Why Middleware?
✓ Runs for every request (centralized logic)
✓ Can reject requests early (auth check)
✓ Can format all responses consistently
✓ Can handle errors globally
✓ Separates concerns from route handlers

Middleware vs Route Handler:
- Middleware: Applies to ALL routes
- Route: Applies to specific endpoint

Example: Authentication

Without middleware:
@router.get("/profile")
def get_profile(request: Request):
    token = extract_token(request.headers)
    if not token:
        raise UnauthorizedError()
    user_id = verify_token(token)
    # ... business logic

Every route would repeat this code!

With middleware:
Middleware does auth check for all routes automatically

@router.get("/profile")
def get_profile(request: Request):
    user_id = request.user.id  # Already verified by middleware
    # ... business logic

Phase 1 Status: Folder structure created, implementation in Phase 2
"""
