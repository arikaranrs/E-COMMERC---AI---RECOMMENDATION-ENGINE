"""
Request/Response Validation Schemas (Pydantic)

What is Pydantic?
- Library for data validation and type checking
- Validates INCOMING requests before code processes them
- Validates OUTGOING responses before sending to client
- Catches invalid data early with helpful error messages

How It Works:

1. Client sends HTTP request with JSON body:
   POST /api/v1/auth/login
   {"email": "john@example.com", "password": "secret123"}

2. Route handler defines a schema:
   class LoginRequest(BaseModel):
       email: str
       password: str

3. Pydantic validates automatically:
   - email field is a string? ✓
   - password field is a string? ✓
   - Any unexpected fields? ✗ Rejected
   - Are all required fields present? ✓

4. If validation fails, return error immediately:
   {"detail": "email must be a valid email address"}

5. If validation passes, proceed to business logic

Response Validation Pattern:
1. Service returns Python object
2. Response schema serializes to JSON
3. Pydantic validates output matches schema
4. Client receives consistent JSON response

Schemas Will Include (Phase 2+):
- user.py: UserCreate, UserLogin, UserResponse, UserUpdate
- product.py: ProductResponse, ProductCreate, ProductFilter
- order.py: OrderCreate, OrderResponse, OrderItem
- common.py: PaginationResponse, ErrorResponse

Benefits:
✓ Type safety - catch bugs before runtime
✓ Auto documentation - Swagger docs generated from schemas
✓ Early validation - fail fast
✓ Consistent API - clients know what to expect
✓ Error clarity - users know exactly what's wrong

Phase 1 Status: Folder structure created, actual schemas in Phase 2
"""
