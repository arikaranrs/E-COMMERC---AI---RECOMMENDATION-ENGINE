# Phase 1: Project Structure - COMPLETE

## What Was Built

In Phase 1, we designed and created the **complete folder structure** for an enterprise AI-powered e-commerce platform. This is NOT code yet - it's the blueprint.

## Project Overview

This is a **full-stack application** with clear separation of concerns:

```
┌─────────────────────────────────────────────────┐
│        Frontend (React/Next.js 16)              │
│  User sees products, adds to cart, sees         │
│  personalized recommendations                   │
└────────────────────┬────────────────────────────┘
                     │ HTTP API calls
                     ↓
┌─────────────────────────────────────────────────┐
│        Backend (FastAPI/Python)                 │
│  Handles business logic, authentication,        │
│  product management, order processing           │
└────────────────────┬────────────────────────────┘
                     │ SQL queries
                     ↓
┌─────────────────────────────────────────────────┐
│        Database (MySQL)                         │
│  Stores users, products, orders, reviews        │
└─────────────────────────────────────────────────┘

Separate components:
│
├─ ML Pipeline (PySpark)
│  ├─ Extract user behavior
│  ├─ Engineer features
│  └─ Train models (nightly)
│
└─ AI Service (Python ML)
   ├─ Load trained models
   └─ Make recommendations (milliseconds)
```

## Folder Structure Created

### Root Level
```
/vercel/share/v0-project/
├── frontend/              ← React/Next.js app (user interface)
├── backend/               ← FastAPI app (API server)
├── ml_pipeline/           ← PySpark jobs (data processing)
├── ai_service/            ← ML models (recommendations)
├── db/                    ← Database schema and migrations
├── docker/                ← Docker configurations
├── tests/                 ← Test suites
├── docs/                  ← Documentation
├── PHASE_1_COMPLETE.md    ← This file
└── README.md              ← Project overview
```

### Backend Structure (`backend/app/`)

```
app/
├── main.py                ← FastAPI application entry point
├── config.py              ← Configuration (database, JWT, CORS)
│
├── api/
│   ├── v1/
│   │   ├── __init__.py           ← Route registration
│   │   ├── auth.py               ← Login/register (to implement)
│   │   ├── products.py           ← Product endpoints (to implement)
│   │   ├── cart.py               ← Cart endpoints (to implement)
│   │   ├── orders.py             ← Order endpoints (to implement)
│   │   ├── users.py              ← User profile endpoints (to implement)
│   │   └── recommendations.py    ← ML recommendations (to implement)
│   └── middleware.py             ← Global middleware
│
├── models/                ← SQLAlchemy ORM (database tables)
│   ├── __init__.py
│   ├── base.py            ← Base model with common columns
│   ├── user.py            ← User table (to implement Phase 2)
│   ├── product.py         ← Product table (to implement Phase 2)
│   ├── order.py           ← Order tables (to implement Phase 2)
│   ├── review.py          ← Review table (to implement Phase 2)
│   ├── recommendation.py  ← Recommendation cache (to implement Phase 2)
│   └── wishlist.py        ← Wishlist table (to implement Phase 2)
│
├── schemas/               ← Pydantic validation schemas
│   ├── __init__.py
│   ├── user.py            ← User request/response schemas
│   ├── product.py         ← Product schemas
│   ├── order.py           ← Order schemas
│   └── common.py          ← Pagination, errors
│
├── services/              ← Business logic layer
│   ├── __init__.py
│   ├── auth_service.py    ← Register, login, logout
│   ├── product_service.py ← Product operations
│   ├── cart_service.py    ← Cart operations
│   ├── order_service.py   ← Order operations
│   ├── user_service.py    ← User profile operations
│   └── recommendation_service.py ← Call AI models
│
├── repositories/          ← Database access layer
│   ├── __init__.py
│   ├── base_repository.py ← Common repository methods
│   ├── user_repository.py ← User SQL queries
│   ├── product_repository.py ← Product SQL queries
│   ├── order_repository.py ← Order SQL queries
│   ├── review_repository.py ← Review SQL queries
│   └── wishlist_repository.py ← Wishlist SQL queries
│
├── utils/                 ← Helper functions
│   ├── __init__.py
│   ├── jwt_utils.py       ← JWT token creation/verification
│   ├── password_utils.py  ← Password hashing (bcrypt)
│   ├── database.py        ← Database connection
│   ├── logger.py          ← Logging setup
│   └── validators.py      ← Input validation
│
└── middleware/            ← Request/response middleware
    ├── __init__.py
    ├── auth_middleware.py ← JWT verification
    ├── cors_middleware.py ← Cross-origin handling
    └── error_handler.py   ← Global error handling
```

### Frontend Structure (`frontend/`)

```
frontend/
├── app/
│   ├── layout.tsx         ← Root layout wrapper
│   ├── page.tsx           ← Home page (/)
│   ├── globals.css        ← Global styles
│   │
│   ├── (auth)/            ← Route group: auth pages
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   └── logout/page.tsx
│   │
│   ├── (store)/           ← Route group: shopping
│   │   ├── products/page.tsx
│   │   ├── products/[id]/page.tsx
│   │   ├── cart/page.tsx
│   │   └── checkout/page.tsx
│   │
│   ├── (dashboard)/       ← Route group: user dashboard
│   │   ├── profile/page.tsx
│   │   ├── orders/page.tsx
│   │   └── wishlist/page.tsx
│   │
│   └── (admin)/           ← Route group: admin panel
│       ├── products/page.tsx
│       ├── orders/page.tsx
│       └── analytics/page.tsx
│
├── components/            ← Reusable React components
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   └── RegisterForm.tsx
│   ├── product/
│   │   ├── ProductCard.tsx
│   │   ├── ProductGrid.tsx
│   │   └── ProductFilter.tsx
│   ├── cart/
│   │   ├── CartItem.tsx
│   │   └── CartSummary.tsx
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   └── Sidebar.tsx
│   └── common/
│       ├── Button.tsx
│       ├── Input.tsx
│       └── LoadingSpinner.tsx
│
├── hooks/                 ← Custom React hooks
│   ├── useAuth.ts         ← Authentication logic
│   ├── useProducts.ts     ← Fetch products
│   ├── useCart.ts         ← Shopping cart state
│   └── useFetch.ts        ← Generic data fetching
│
├── lib/                   ← Utilities
│   ├── api-client.ts      ← HTTP client for backend
│   ├── constants.ts       ← API URLs, constants
│   ├── types.ts           ← TypeScript types
│   ├── validation.ts      ← Zod validation
│   └── utils.ts           ← Helper functions
│
├── stores/                ← Global state (Zustand)
│   ├── auth-store.ts      ← Login state, tokens
│   ├── cart-store.ts      ← Cart items
│   └── ui-store.ts        ← UI state (theme, sidebar)
│
└── public/                ← Static assets
    ├── images/
    ├── icons/
    └── fonts/
```

### Database Structure (`db/`)

```
db/
├── schema.sql                    ← CREATE TABLE statements
├── DATABASE_STRUCTURE.md         ← Database documentation
│
├── migrations/                   ← Version-controlled schema changes
│   ├── 001_initial_schema.sql
│   ├── 002_add_recommendations.sql
│   └── migration_runner.py
│
└── seeds/                        ← Sample data
    ├── users.sql
    ├── products.sql
    └── seed_runner.py
```

### ML Pipeline Structure (`ml_pipeline/`)

```
ml_pipeline/
├── ML_PIPELINE_STRUCTURE.md
├── jobs/
│   ├── data_extraction.py        ← Query database
│   ├── feature_engineering.py    ← Extract features
│   └── model_training.py         ← Train models
│
├── config/
│   ├── spark_config.py           ← Spark settings
│   └── paths.py                  ← Data paths
│
└── requirements.txt
```

### AI Service Structure (`ai_service/`)

```
ai_service/
├── models/
│   ├── collaborative_filtering.py ← CF algorithm
│   ├── content_based.py           ← Content-based algorithm
│   └── hybrid.py                  ← Hybrid approach
│
├── inference/
│   ├── recommender.py            ← Main recommendation engine
│   └── model_loader.py           ← Load models from disk
│
├── saved_models/
│   ├── collaborative_filter.pkl
│   ├── content_based.pkl
│   └── hybrid.pkl
│
└── requirements.txt
```

## Key Concepts Explained

### Request Flow: User Viewing a Product

```
1. User clicks "View Products" in browser
                            ↓
2. Frontend (React component) makes HTTP request
   GET /api/v1/products?category=electronics
                            ↓
3. Request reaches Backend (FastAPI)
   - Route handler: api/v1/products.py
   - Validates request using Pydantic schema
                            ↓
4. Service Layer (services/product_service.py)
   - Business logic: filter by category
   - Calls repository for database access
                            ↓
5. Repository Layer (repositories/product_repository.py)
   - Executes SQL: SELECT * FROM products WHERE category = 'electronics'
   - SQLAlchemy translates Python to SQL
                            ↓
6. Database (MySQL)
   - Executes query
   - Returns matching rows
                            ↓
7. Data flows back up:
   Repository → Service → Route → Response Schema
   - Serializes to JSON
                            ↓
8. Frontend receives JSON array of products
   - Updates React state (SWR/Zustand)
   - Components re-render
                            ↓
9. User sees products on screen
```

### Layered Architecture Benefits

```
HTTP Layer (api/)              ← Routes/endpoints
    ↓
Business Logic (services/)     ← Where actual work happens
    ↓
Database Access (repositories/) ← SQL queries
    ↓
ORM (models/)                  ← Python ↔ SQL mapping
    ↓
MySQL Database                ← Data storage
```

**Why layers?**
- Easy to test each layer independently
- Change database without changing business logic
- Change business logic without changing routes
- Clear separation of concerns

### Authentication Flow

```
1. User enters email + password in frontend
2. Frontend sends POST /api/v1/auth/login
3. Backend auth_service:
   - Hash password using bcrypt
   - Query database: find user by email
   - Compare hashed password with stored hash
   - If match: create JWT token
4. Backend returns token to frontend
5. Frontend stores token in browser memory
6. Future requests include token in header:
   Authorization: Bearer <token>
7. Auth middleware verifies token:
   - Verify signature (token not tampered)
   - Check expiration
   - Extract user_id
8. Route handler proceeds with authenticated user
```

### ML Recommendation Flow

```
Nightly Training (10:00 PM):
1. PySpark job queries database
2. Extracts user behavior (clicks, purchases)
3. Extracts product features (price, category, ratings)
4. Engineers features (normalize, encode)
5. Trains 3 models (CF, content-based, hybrid)
6. Saves trained models to disk

User Views Product (Next Day):
1. Frontend calls: GET /api/v1/recommendations
2. Backend calls AI service
3. AI service loads trained model from disk
4. Makes prediction: [product_id_1, product_id_2, ...]
5. Backend fetches full product details
6. Frontend displays recommendations
```

## Documentation Created

1. **PHASE_1_PROJECT_STRUCTURE.md** (415 lines)
   - Complete architecture overview
   - Request flow explanation
   - Every folder explained
   - Design principles

2. **frontend/FRONTEND_STRUCTURE.md** (355 lines)
   - Next.js App Router structure
   - Component organization
   - State management (Zustand)
   - Data fetching (SWR)
   - Frontend/backend communication

3. **db/DATABASE_STRUCTURE.md** (262 lines)
   - Database concepts
   - Schema design (13 tables)
   - SQL examples
   - Relationships and indexes
   - Migration strategy

4. **ml_pipeline/ML_PIPELINE_STRUCTURE.md** (372 lines)
   - ETL pipeline (Extract, Transform, Load)
   - Machine learning models (5 algorithms)
   - Batch processing schedule
   - Model versioning
   - End-to-end data flow

## What We Know Now

After Phase 1, you understand:

✓ Why the project needs backend, frontend, database, ML
✓ How a request flows from browser to database and back
✓ Layered architecture: routes → services → repositories → database
✓ Authentication using JWT tokens
✓ ML pipeline: training models nightly, using for inference
✓ Clear folder structure for scalability
✓ Separation of concerns: each layer has one job

## What's Next: Phase 2

Phase 2: Database Schema & Setup

We will:
1. Design complete database schema (13 tables)
2. Create SQL files for table creation
3. Set up MySQL database locally
4. Create migration system for schema versioning
5. Seed sample data for testing

**Stop here. Phase 1 is complete.**

Please review the created documentation and folder structure, then confirm you're ready for Phase 2.
