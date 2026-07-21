# Phase 1: Project Structure

## Architecture Overview

This is an enterprise AI-powered e-commerce platform built as a monorepo with clear separation between:

1. **Frontend** (Next.js 16 React) - User interface
2. **Backend** (FastAPI Python) - Business logic and APIs
3. **ML Pipeline** (PySpark) - Data processing and feature engineering
4. **AI Service** (Python ML) - Recommendation model serving
5. **Database** (MySQL) - Data storage
6. **DevOps** (Docker) - Containerization

## Request Flow

```
Browser (HTTP Request)
    ↓
Next.js Frontend (React)
    ├─ Validates input locally
    ├─ Shows loading state
    └─ Makes API call
    ↓
FastAPI Backend (Python)
    ├─ Receives HTTP request
    ├─ Validates request (Pydantic)
    ├─ Calls service layer (business logic)
    ├─ Calls repository layer (database)
    └─ Returns JSON response
    ↓
MySQL Database
    ├─ Executes SQL query
    └─ Returns records
    ↓
Backend Response (JSON)
    ↓
Next.js Frontend (React)
    ├─ Receives JSON
    ├─ Updates state (SWR/Zustand)
    └─ Re-renders components
    ↓
Browser (User sees result)
```

## Project Structure

```
ecommerce-ai/
│
├── frontend/                        # Next.js React App
│   ├── app/
│   │   ├── layout.tsx              # Root layout
│   │   ├── page.tsx                # Home page
│   │   ├── globals.css             # Global styles
│   │   ├── (auth)/                 # Auth routes group
│   │   │   ├── login/page.tsx
│   │   │   ├── register/page.tsx
│   │   │   └── logout/page.tsx
│   │   ├── (store)/                # Store routes group
│   │   │   ├── products/page.tsx
│   │   │   ├── products/[id]/page.tsx
│   │   │   ├── cart/page.tsx
│   │   │   └── checkout/page.tsx
│   │   ├── (dashboard)/            # User dashboard routes
│   │   │   ├── profile/page.tsx
│   │   │   ├── orders/page.tsx
│   │   │   └── wishlist/page.tsx
│   │   ├── (admin)/                # Admin routes
│   │   │   ├── products/page.tsx
│   │   │   ├── orders/page.tsx
│   │   │   └── analytics/page.tsx
│   │   └── api/                    # API routes (if needed)
│   │
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── product/
│   │   │   ├── ProductCard.tsx
│   │   │   ├── ProductGrid.tsx
│   │   │   └── ProductFilter.tsx
│   │   ├── cart/
│   │   │   ├── CartItem.tsx
│   │   │   └── CartSummary.tsx
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Sidebar.tsx
│   │   └── common/
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       └── LoadingSpinner.tsx
│   │
│   ├── hooks/
│   │   ├── useAuth.ts              # Authentication logic
│   │   ├── useProducts.ts          # Fetch products
│   │   ├── useCart.ts              # Shopping cart state
│   │   └── useFetch.ts             # Generic data fetching
│   │
│   ├── lib/
│   │   ├── api-client.ts           # HTTP client for backend
│   │   ├── constants.ts            # API URLs, constants
│   │   ├── types.ts                # TypeScript types
│   │   ├── validation.ts           # Zod schemas for validation
│   │   └── utils.ts                # Helper functions
│   │
│   ├── stores/
│   │   ├── auth-store.ts           # Zustand auth store
│   │   ├── cart-store.ts           # Zustand cart store
│   │   └── ui-store.ts             # Zustand UI state
│   │
│   ├── public/                     # Static assets
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   │
│   ├── styles/
│   │   ├── globals.css
│   │   └── variables.css
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.mjs
│   ├── postcss.config.mjs
│   └── tailwind.config.ts
│
├── backend/                         # FastAPI Python App
│   ├── app/
│   │   ├── main.py                 # FastAPI app initialization
│   │   ├── config.py               # Configuration (DB, JWT secret)
│   │   │
│   │   ├── api/                    # HTTP route handlers
│   │   │   ├── __init__.py
│   │   │   ├── routes.py           # Register all routes
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py         # /api/v1/auth routes
│   │   │   │   ├── products.py     # /api/v1/products routes
│   │   │   │   ├── cart.py         # /api/v1/cart routes
│   │   │   │   ├── orders.py       # /api/v1/orders routes
│   │   │   │   ├── users.py        # /api/v1/users routes
│   │   │   │   └── recommendations.py  # /api/v1/recommendations
│   │   │   └── middleware.py       # CORS, auth middleware
│   │   │
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # Base model class
│   │   │   ├── user.py             # User table
│   │   │   ├── product.py          # Product, Category tables
│   │   │   ├── order.py            # Order, OrderItem tables
│   │   │   ├── review.py           # Review table
│   │   │   ├── recommendation.py   # Recommendation table
│   │   │   └── wishlist.py         # Wishlist table
│   │   │
│   │   ├── schemas/                # Pydantic validation schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py             # User request/response
│   │   │   ├── product.py          # Product request/response
│   │   │   ├── order.py            # Order request/response
│   │   │   └── common.py           # Pagination, error responses
│   │   │
│   │   ├── services/               # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py     # Register, login, logout
│   │   │   ├── product_service.py  # Product operations
│   │   │   ├── cart_service.py     # Cart operations
│   │   │   ├── order_service.py    # Order operations
│   │   │   ├── user_service.py     # User operations
│   │   │   └── recommendation_service.py  # Call AI service
│   │   │
│   │   ├── repositories/           # Database access layer
│   │   │   ├── __init__.py
│   │   │   ├── base_repository.py  # Base class with common methods
│   │   │   ├── user_repository.py  # User SQL queries
│   │   │   ├── product_repository.py  # Product SQL queries
│   │   │   ├── order_repository.py # Order SQL queries
│   │   │   ├── review_repository.py # Review SQL queries
│   │   │   └── wishlist_repository.py # Wishlist SQL queries
│   │   │
│   │   ├── utils/                  # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── jwt_utils.py        # JWT token creation/verification
│   │   │   ├── password_utils.py   # Password hashing/verification
│   │   │   ├── database.py         # Database connection
│   │   │   └── logger.py           # Logging setup
│   │   │
│   │   ├── middleware/             # Request/response middleware
│   │   │   ├── __init__.py
│   │   │   ├── auth_middleware.py  # JWT verification
│   │   │   ├── cors_middleware.py  # CORS setup
│   │   │   └── error_handler.py    # Global error handling
│   │   │
│   │   └── __init__.py
│   │
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example                # Example environment file
│   ├── run.sh                      # Start backend script
│   ├── wsgi.py                     # WSGI entry point (production)
│   └── pytest.ini                  # Pytest configuration
│
├── ml_pipeline/                    # PySpark ETL Jobs
│   ├── jobs/
│   │   ├── __init__.py
│   │   ├── feature_engineering.py  # Extract features from raw data
│   │   ├── data_preparation.py     # Clean and prepare data
│   │   └── training_scheduler.py   # Schedule jobs with Airflow
│   │
│   ├── config/
│   │   ├── spark_config.py         # Spark settings
│   │   └── paths.py                # Data paths
│   │
│   ├── requirements.txt            # PySpark dependencies
│   ├── run_etl.py                  # Main ETL runner
│   └── README.md                   # PySpark job documentation
│
├── ai_service/                     # ML Recommendation Service
│   ├── models/
│   │   ├── __init__.py
│   │   ├── collaborative_filtering.py  # User-item CF
│   │   ├── content_based.py        # Content-based filtering
│   │   ├── hybrid.py               # Hybrid approach
│   │   └── cold_start.py           # Handle new users/items
│   │
│   ├── inference/
│   │   ├── __init__.py
│   │   ├── recommender.py          # Main recommendation engine
│   │   └── model_loader.py         # Load trained models
│   │
│   ├── training/
│   │   ├── __init__.py
│   │   ├── trainer.py              # Model training pipeline
│   │   └── evaluate.py             # Model evaluation
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   └── data_loader.py          # Load training data
│   │
│   ├── saved_models/               # Trained model files
│   │   ├── collaborative_filter.pkl
│   │   ├── content_based.pkl
│   │   └── hybrid.pkl
│   │
│   ├── requirements.txt            # ML dependencies (scikit-learn, pandas)
│   └── config.py                   # Configuration
│
├── db/                             # Database
│   ├── schema.sql                  # Create all tables
│   ├── migrations/
│   │   ├── 001_initial_schema.sql
│   │   ├── 002_add_recommendations_table.sql
│   │   └── migration_runner.py     # Run migrations
│   │
│   └── seeds/
│       ├── users.sql               # Sample user data
│       ├── products.sql            # Sample product data
│       └── seed_runner.py          # Run seeds
│
├── docker/
│   ├── Dockerfile.backend          # Backend container
│   ├── Dockerfile.frontend         # Frontend container
│   ├── docker-compose.yml          # Orchestration
│   └── nginx.conf                  # Nginx reverse proxy
│
├── tests/
│   ├── backend/
│   │   ├── conftest.py             # Pytest fixtures
│   │   ├── test_auth.py            # Auth API tests
│   │   ├── test_products.py        # Product API tests
│   │   ├── test_orders.py          # Order API tests
│   │   └── test_services/          # Service layer tests
│   │
│   ├── frontend/
│   │   ├── __tests__/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   └── pages/
│   │   └── jest.config.js
│   │
│   └── integration/                # End-to-end tests
│       └── test_user_flow.py
│
├── docs/
│   ├── ARCHITECTURE.md             # System architecture
│   ├── API.md                      # API documentation
│   ├── SETUP.md                    # Setup instructions
│   ├── DATABASE.md                 # Database schema docs
│   └── DEVELOPMENT.md              # Development guide
│
├── .env.example                    # Example environment variables
├── .gitignore                      # Git ignore rules
├── docker-compose.yml              # Local docker setup
├── README.md                       # Project README
└── Makefile                        # Common commands
```

## Key Design Principles

### 1. **Separation of Concerns**
- Frontend handles UI and user interaction
- Backend handles business logic and security
- Database handles data persistence
- ML handles recommendations

### 2. **Layered Architecture (Backend)**
```
HTTP Request
    ↓
Route Handler (api/)
    ↓
Service Layer (services/) - Business logic
    ↓
Repository Layer (repositories/) - Database access
    ↓
Database Models (models/) - ORM
    ↓
MySQL Database
```

### 3. **Request Validation**
- Frontend: Zod schemas validate before API call
- Backend: Pydantic schemas validate after API call
- Database: NOT NULL, UNIQUE constraints as final safety

### 4. **Type Safety**
- Frontend: TypeScript with strict mode
- Backend: Python type hints (Pydantic)
- Shared: Types in `lib/types.ts` for frontend

### 5. **Error Handling**
- Global error middleware in backend
- Consistent error response format
- Frontend catches errors and shows user messages

### 6. **Authentication Flow**
```
Login Request
    ↓
Verify password (auth_service)
    ↓
Create JWT token (jwt_utils)
    ↓
Return token to frontend
    ↓
Store token in browser memory (useAuth hook)
    ↓
Send token with every request (Authorization header)
    ↓
Verify token in auth_middleware
    ↓
Continue to route handler
```

### 7. **Data Flow: Showing Products**
```
Frontend: User clicks "View Products"
    ↓
Frontend: Call GET /api/v1/products?category=electronics
    ↓
Backend: routes/products.py receives request
    ↓
Backend: product_service.get_products(category) - business logic
    ↓
Backend: product_repository.fetch_by_category() - database query
    ↓
Database: SELECT * FROM products WHERE category = 'electronics'
    ↓
Backend: Product models serialized to JSON via schemas
    ↓
Frontend: Receives JSON array of products
    ↓
Frontend: Updates SWR cache and re-renders ProductGrid
    ↓
User: Sees products on screen
```

### 8. **Recommendation Flow**
```
PySpark Job (nightly):
    ├─ Extract user behavior (clicks, purchases)
    ├─ Extract product features (price, category, popularity)
    └─ Train ML models (collaborative filtering, content-based)
        ↓
    Trained models saved to ai_service/saved_models/
        ↓
Frontend: User views product
    ↓
Backend: GET /api/v1/recommendations
    ↓
Backend: recommendation_service calls AI service
    ↓
AI Service: Load trained model, make prediction
    ↓
AI Service: Return top 5 product IDs
    ↓
Backend: Fetch full product data from database
    ↓
Frontend: Display recommendations to user
```

## What Happens in Phase 1

✅ Create empty folder structure
✅ Create starter files with docstrings
✅ Explain why each part exists
✅ Show how request flows through system

## What Happens in Phase 2+

- Phase 2: Database schema and setup
- Phase 3: User authentication
- Phase 4: Product management
- ... and so on

**This Phase 1 is complete when you understand the structure and can explain how a request flows from browser to database and back.**
