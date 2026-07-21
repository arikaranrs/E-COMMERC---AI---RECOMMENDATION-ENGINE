"""
Database Access Layer (Repositories)

What is a Repository?
- Encapsulates ALL database queries
- Converts SQL to Python
- Abstracts database details from service layer
- Makes it easy to switch databases later

Request Flow:
Service Layer (Business Logic)
    ↓
Repository Layer (Database Access)
    ↓
SQLAlchemy ORM (converts Python to SQL)
    ↓
MySQL Database

Why Repositories?
✓ All SQL queries in ONE place
✓ Services don't know SQL details
✓ Easy to test with mock repositories
✓ Can change database without changing services
✓ Query logic is reusable

Example: Get User by Email

Service needs a user:
  user = user_repository.find_by_email("john@example.com")

Repository finds user:
  def find_by_email(self, email: str):
      # Uses SQLAlchemy to generate SQL automatically:
      # SELECT * FROM users WHERE email = ?
      return session.query(User).filter(User.email == email).first()

SQLAlchemy converts to SQL and executes.
Database returns result.
Repository returns Python User object.
Service uses the object.

Repositories Will Include (Phase 2+):
- user_repository.py: Find by ID, email, create, update, delete
- product_repository.py: List, filter, search, get by ID
- order_repository.py: Create, find by user, find by ID
- review_repository.py: Add review, get product reviews
- wishlist_repository.py: Add/remove items, get user wishlist

Repository Pattern Benefits:
✓ Centralized database access
✓ Testable services (mock repository)
✓ Single responsibility (one repo per entity)
✓ Easy to optimize queries
✓ Prevents SQL scattered throughout code

Phase 1 Status: Folder structure created, implementation in Phase 2
"""
