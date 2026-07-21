"""
Database Models - SQLAlchemy ORM

What is an ORM (Object-Relational Mapping)?
- Converts database tables into Python classes
- Each class = a table
- Each instance = a row
- Attributes = columns

Example:
Database: users table (id, email, password_hash, name)
Python ORM:
  class User:
      id: int
      email: str
      password_hash: str
      name: str
  
  user = User(name="John", email="john@example.com")
  session.add(user)  # Saves to database

Models in This Package (will be implemented in Phase 2):
- base.py: Base model class with id, created_at, updated_at
- user.py: User table (authentication, profiles)
- product.py: Product and Category tables
- order.py: Order and OrderItem tables
- review.py: Product reviews
- recommendation.py: ML recommendation results
- wishlist.py: User wishlists

Why SQLAlchemy ORM?
✓ Write Python instead of SQL
✓ Type-safe queries
✓ Easy to test
✓ Automatic SQL generation
✓ Works with any database (MySQL, PostgreSQL, SQLite)

Phase 1 Status: Structure created, models will be implemented in Phase 2
"""
