"""
Business Logic Layer (Services)

What is a Service Layer?
- Encapsulates business logic (the actual work of your application)
- Uses repositories to access data
- Called by route handlers
- Testable without HTTP involvement

Request Flow:
HTTP Request from Client
    ↓
Route Handler (api/v1/auth.py) - "I received login request"
    ↓
Service (services/auth_service.py) - "Here's how to validate & create user"
    ↓
Repository (repositories/user_repository.py) - "Get user data from DB"
    ↓
Database - "User record retrieved"
    ↓
Back up: Repository → Service → Route → HTTP Response to Client

Example: User Login Flow

1. Client: POST /api/v1/auth/login
   {"email": "john@example.com", "password": "secret123"}

2. Route Handler (api/v1/auth.py):
   - Validates JSON using LoginRequest schema (Pydantic)
   - Calls: auth_service.login(email, password)
   - Returns: {"access_token": "...", "token_type": "bearer"}

3. Service (services/auth_service.py):
   - Hash incoming password using bcrypt
   - Call: user_repo.find_by_email(email)
   - Compare hashed password with stored hash
   - If match: create JWT token and return it
   - If no match: raise LoginError

4. Repository (repositories/user_repository.py):
   - Execute SQL: SELECT * FROM users WHERE email = ?
   - Return User object or None

Why Separate Services?
✓ Route handles HTTP only (routing, validation)
✓ Service handles logic (business rules, calculations)
✓ Repository handles DB only (SQL queries)
✓ Each layer is testable independently
✓ Logic is reusable (can call from multiple routes)

Services Will Include (Phase 2+):
- auth_service.py: Register, login, logout, refresh token, verify email
- product_service.py: Search, filter, sort, recommendations
- order_service.py: Create, calculate totals, apply coupons, track
- user_service.py: Get profile, update info, manage preferences
- recommendation_service.py: Call ML model, cache results

Phase 1 Status: Folder structure created, implementation in Phase 2
"""
