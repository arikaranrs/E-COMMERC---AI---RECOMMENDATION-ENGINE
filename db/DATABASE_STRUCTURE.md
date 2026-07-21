# Database Structure (Phase 1)

## What is a Database?

A database stores all application data persistently on disk.

Data Types:
- Users: emails, passwords, names
- Products: names, prices, descriptions, images
- Orders: what user bought, when, how much
- Reviews: user ratings and comments
- Shopping carts: temporary items being considered

Why Not Just Store in Memory?
- Memory is lost when server restarts
- Can't be accessed by other servers
- No transaction guarantees
- Not scalable

Why MySQL?

- Relational database (organize data in tables)
- SQL queries (standard language)
- ACID compliance (data integrity)
- Widely used and well-supported
- Free and open source

## Database Schema (Phase 2+)

### users table
```
id          INT PRIMARY KEY AUTO_INCREMENT
email       VARCHAR(255) UNIQUE NOT NULL
password_hash  VARCHAR(255) NOT NULL
name        VARCHAR(255) NOT NULL
created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at  TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

**What each column means:**
- `id`: Unique identifier (1, 2, 3, ...)
- `email`: User's email (must be unique)
- `password_hash`: Hashed password (never store plain text!)
- `name`: User's name
- `created_at`: When account was created
- `updated_at`: When account was last modified

**Why hashing passwords?**
- If database is stolen, attackers can't read passwords
- Even admin can't see user passwords
- One-way: hash("password123") → "asd89f7sad8f"
- Can't reverse: can't go from hash back to password
- Verify: hash(user_input) == stored_hash

### products table
```
id          INT PRIMARY KEY AUTO_INCREMENT
name        VARCHAR(255) NOT NULL
description TEXT
price       DECIMAL(10, 2) NOT NULL
stock       INT DEFAULT 0
created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

### orders table
```
id          INT PRIMARY KEY AUTO_INCREMENT
user_id     INT NOT NULL FOREIGN KEY(users.id)
total_price DECIMAL(10, 2)
status      ENUM('pending', 'paid', 'shipped', 'delivered')
created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

**Foreign Key:**
- `user_id` references `users.id`
- Links each order to a user
- Database enforces: can't have order without user
- If user deleted: delete their orders (cascade)

### order_items table
```
id          INT PRIMARY KEY AUTO_INCREMENT
order_id    INT NOT NULL FOREIGN KEY(orders.id)
product_id  INT NOT NULL FOREIGN KEY(products.id)
quantity    INT
price       DECIMAL(10, 2)
```

**Why separate order and order_items?**
- Order: one row per order
- Order_items: one row per product in order

Example:
Order #1 from John: Total $50
- order_items: product_id=1, qty=2, price=$20
- order_items: product_id=2, qty=1, price=$10

Query to get what John bought:
```sql
SELECT p.name, oi.quantity, oi.price
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.user_id = 1
```

### recommendations table
```
id          INT PRIMARY KEY AUTO_INCREMENT
user_id     INT NOT NULL FOREIGN KEY(users.id)
product_id  INT NOT NULL FOREIGN KEY(products.id)
score       FLOAT  (0.0 to 1.0)
algorithm   VARCHAR(50) ('collaborative_filtering', 'content_based', 'hybrid')
created_at  TIMESTAMP
```

**Stores ML model predictions:**
- For each user, list recommended products
- Score: confidence (0.0 = not sure, 1.0 = very sure)
- Algorithm: which model generated recommendation
- Updated daily by ml_pipeline

## Relationships

### One-to-Many: User to Orders
```
User(id=1) ──→ Order(user_id=1)
John           Order #1, Order #2, Order #3
```

### Many-to-Many: Orders to Products
```
Order(id=1) ──→ OrderItem ──→ Product
                  product_id=1
                  product_id=2
```

## SQL Examples (Phase 2+)

### Get all products
```sql
SELECT id, name, price FROM products;
```

### Get user's orders
```sql
SELECT o.id, o.total_price, o.status, o.created_at
FROM orders o
WHERE o.user_id = 1
ORDER BY o.created_at DESC;
```

### Get items in specific order
```sql
SELECT p.name, oi.quantity, oi.price
FROM order_items oi
JOIN products p ON oi.product_id = p.id
WHERE oi.order_id = 5;
```

### Get recommendations for user
```sql
SELECT p.id, p.name, p.price, r.score
FROM recommendations r
JOIN products p ON r.product_id = p.id
WHERE r.user_id = 1
ORDER BY r.score DESC
LIMIT 5;
```

## Migrations

What are migrations?
- Version control for database schema
- Track changes over time
- Can rollback if needed

Example:
```
001_initial_schema.sql
├─ Create users table
├─ Create products table
├─ Create orders table

002_add_recommendations.sql
├─ Create recommendations table
├─ Add indexes for performance

003_add_user_preferences.sql
├─ Add preferences column to users
```

When you change schema:
1. Create new migration file
2. Write SQL for change
3. Run migration
4. Now all databases (dev, staging, production) are in sync

## Indexes

What are indexes?
- Speed up queries (like table of contents)
- Slower inserts/updates (must update index)
- Use when frequently filtered

Example:
```sql
CREATE INDEX idx_user_email ON users(email);
```

Now this is fast:
```sql
SELECT * FROM users WHERE email = 'john@example.com';
```

Without index: scan all rows
With index: direct lookup

## Database Connection

Backend connects to database:

```python
# app/config.py
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/ecommerce_db"

# Connection string format:
# mysql+pymysql://username:password@hostname:port/database_name
```

SQLAlchemy converts:
```python
user = session.query(User).filter(User.email == "john@example.com").first()
```

To:
```sql
SELECT * FROM users WHERE email = 'john@example.com' LIMIT 1;
```

## Folder Structure

```
db/
├── schema.sql              # All CREATE TABLE statements
├── migrations/
│   ├── 001_initial.sql
│   ├── 002_add_recommendations.sql
│   └── migration_runner.py # Script to run all migrations
├── seeds/
│   ├── users.sql          # Sample users for testing
│   ├── products.sql       # Sample products
│   └── seed_runner.py     # Script to insert sample data
└── DATABASE_STRUCTURE.md  # This file
```

## Phase 1 Status

Structure explained. Schema will be created in Phase 2.

Next: Design complete schema with all tables and relationships.
