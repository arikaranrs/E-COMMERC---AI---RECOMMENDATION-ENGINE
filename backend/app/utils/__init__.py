"""
Utility Functions and Helpers

Common helper functions used throughout the application.

Utils Will Include (Phase 2+):

1. jwt_utils.py - JWT Token Management
   - create_access_token(user_id) → generates JWT token
   - create_refresh_token(user_id) → generates refresh token
   - verify_token(token) → validates token and returns user_id
   
   JWT (JSON Web Token):
   Three parts separated by dots:
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
   eyJ1c2VyX2lkIjogMTIzLCAiZXhwIjogMTYyNDAwMDAwMH0.
   SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
   
   - Header: {"alg": "HS256", "typ": "JWT"}
   - Payload: {"user_id": 123, "exp": 1624000000}
   - Signature: cryptographic signature (prevents tampering)

2. password_utils.py - Password Management
   - hash_password(password) → hashes password with bcrypt
   - verify_password(plain, hashed) → validates password
   
   Why bcrypt?
   - Normal hash: 1ms (can try millions per second)
   - Bcrypt: 100ms (only thousands per second)
   - Makes brute force attacks impractical

3. database.py - Database Connection
   - get_db() → yields SQLAlchemy session
   - close_db() → closes connection
   
   Sessions are database connections.
   Each request gets its own session.

4. logger.py - Logging
   - setup_logger() → configures logging
   - log_error(message) → logs errors
   - log_info(message) → logs info
   
   Logs help debug issues in production.

5. validators.py - Input Validation
   - is_valid_email(email) → checks email format
   - is_strong_password(password) → enforces rules
   - sanitize_input(text) → removes dangerous chars
   
   Extra validation layer beyond Pydantic schemas.

Why Utils?
✓ Don't repeat code
✓ Centralize common logic
✓ Easy to test
✓ Easy to modify in one place

Example Usage in Services:

from app.utils.jwt_utils import create_access_token
from app.utils.password_utils import hash_password, verify_password

def register(email, password):
    hashed = hash_password(password)  # Hash password
    user = create_user(email, hashed)
    token = create_access_token(user.id)  # Create JWT
    return {"token": token, "user": user}

Phase 1 Status: Folder structure created, implementation in Phase 2
"""
