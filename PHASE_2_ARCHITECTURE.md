# PHASE 2: System Architecture & Database Design

## 1. Detailed System Architecture

### 1.1 Frontend Architecture (Next.js 16)

```
frontend/
├── app/
│   ├── layout.tsx                 # Root layout with providers
│   ├── page.tsx                   # Homepage with recommendations
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   ├── signup/page.tsx
│   │   └── reset-password/page.tsx
│   ├── (shop)/
│   │   ├── products/page.tsx      # Product listing/search
│   │   ├── products/[id]/page.tsx # Product detail with similar items
│   │   ├── cart/page.tsx
│   │   ├── checkout/page.tsx
│   │   └── orders/page.tsx
│   ├── (user)/
│   │   ├── profile/page.tsx
│   │   ├── wishlist/page.tsx
│   │   └── orders/[id]/page.tsx
│   ├── (admin)/
│   │   ├── dashboard/page.tsx
│   │   ├── products/page.tsx
│   │   ├── analytics/page.tsx
│   │   └── users/page.tsx
│   └── api/
│       └── auth/[...nextauth]/route.ts
├── components/
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── Footer.tsx
│   ├── product/
│   │   ├── ProductCard.tsx
│   │   ├── ProductGrid.tsx
│   │   └── ProductDetail.tsx
│   ├── cart/
│   │   ├── CartItem.tsx
│   │   └── CartSummary.tsx
│   ├── recommendations/
│   │   ├── RecommendationCarousel.tsx
│   │   ├── SimilarProducts.tsx
│   │   └── TrendingProducts.tsx
│   └── common/
│       ├── Button.tsx
│       ├── Modal.tsx
│       └── LoadingSpinner.tsx
├── hooks/
│   ├── useAuth.ts
│   ├── useCart.ts
│   ├── useProducts.ts
│   └── useRecommendations.ts
├── lib/
│   ├── api-client.ts             # Axios instance with auth
│   ├── auth.ts                   # Auth utilities
│   ├── storage.ts                # LocalStorage helpers
│   └── validators.ts             # Zod schemas
├── types/
│   ├── user.ts
│   ├── product.ts
│   ├── order.ts
│   └── recommendation.ts
├── store/
│   ├── authStore.ts              # Zustand auth state
│   ├── cartStore.ts              # Cart state
│   └── userStore.ts              # User preferences
└── styles/
    └── globals.css

Frontend Data Flow:
User ← UI Components ← Custom Hooks ← API Client ← Backend APIs
                          ↓
                    Global State (Zustand)
```

### 1.2 Backend Architecture (FastAPI)

```
backend/
├── app/
│   ├── main.py                   # FastAPI app initialization
│   ├── config.py                 # Configuration, environment variables
│   ├── dependencies.py           # Dependency injection
│   ├── middleware.py             # Custom middleware
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # SQLAlchemy User model
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── brand.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   ├── cart.py
│   │   ├── wishlist.py
│   │   ├── review.py
│   │   ├── rating.py
│   │   ├── user_activity.py      # Tracks user behavior
│   │   └── session.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py              # Pydantic request/response schemas
│   │   ├── product.py
│   │   ├── order.py
│   │   └── recommendation.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py              # Generic repository pattern
│   │   ├── user_repository.py
│   │   ├── product_repository.py
│   │   ├── order_repository.py
│   │   └── rating_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py      # Business logic
│   │   ├── product_service.py
│   │   ├── order_service.py
│   │   ├── auth_service.py      # Authentication & JWT
│   │   ├── search_service.py    # Full-text search
│   │   └── recommendation_service.py  # Calls ML models
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # POST /api/auth/login, /signup
│   │   │   ├── users.py         # GET /api/users/me, PUT /api/users/me
│   │   │   ├── products.py      # GET /api/products, POST /api/products
│   │   │   ├── categories.py
│   │   │   ├── orders.py        # POST /api/orders (checkout)
│   │   │   ├── cart.py          # POST /api/cart/items
│   │   │   ├── wishlist.py
│   │   │   ├── reviews.py       # POST /api/reviews
│   │   │   ├── ratings.py       # POST /api/ratings
│   │   │   └── recommendations.py  # GET /api/recommendations/top-n
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── collaborative.py    # CF algorithms (User-Based, Item-Based)
│   │   │   ├── content_based.py    # TF-IDF, embeddings
│   │   │   ├── hybrid.py           # Hybrid recommendation
│   │   │   └── matrix_factorization.py  # SVD, ALS
│   │   ├── preprocessing.py       # Feature engineering
│   │   ├── evaluation.py          # Model evaluation metrics
│   │   └── model_loader.py        # Load pre-trained models
│   ├── ml_pipeline/
│   │   ├── __init__.py
│   │   ├── data_loader.py        # Load data from DB
│   │   ├── feature_engineering.py # PySpark transformations
│   │   ├── model_training.py     # Train models
│   │   └── save_models.py        # Persist trained models
│   ├── utils/
│   │   ├── logger.py             # Logging configuration
│   │   ├── jwt_utils.py          # JWT token handling
│   │   ├── validators.py         # Input validation helpers
│   │   └── constants.py          # Constants, enums
│   ├── exceptions/
│   │   ├── __init__.py
│   │   ├── base.py              # Base exception class
│   │   ├── auth_exceptions.py
│   │   ├── product_exceptions.py
│   │   └── order_exceptions.py
│   └── tests/
│       ├── __init__.py
│       ├── test_auth.py
│       ├── test_products.py
│       ├── test_recommendations.py
│       └── test_utils.py
├── migrations/                   # Alembic DB migrations
├── requirements.txt
├── .env.example
└── Dockerfile

Backend Data Flow:
Request → Auth Middleware → Route Handler → Service Layer → Repository → DB
                                  ↓
                            ML Service → Loaded Models → Prediction → Response
```

### 1.3 Data Pipeline Architecture (PySpark/Batch)

```
ml_pipeline/
├── config/
│   └── spark_config.py
├── jobs/
│   ├── data_ingestion.py         # Extract from MySQL
│   ├── data_cleaning.py          # Remove nulls, outliers
│   ├── data_transformation.py    # PySpark transformations
│   ├── feature_engineering.py    # Create features for ML
│   ├── training_data_prep.py     # Prepare training/test sets
│   └── model_training.py         # Train recommendation models
├── utils/
│   ├── spark_utils.py
│   ├── mysql_utils.py
│   └── logging.py
└── main.py                       # Orchestrate pipeline

Pipeline Flow (Daily/Weekly):
Raw Data → Extract → Clean → Transform → Features → Train Models → Save Models → API Loads

Why PySpark?
- Distributed processing for 100GB+ data
- Handles millions of user-product interactions
- Feature engineering at scale
- Parallel model training
```

### 1.4 ML/AI Architecture

```
Recommendation System (3-Tier Approach):

┌─────────────────────────────────────────────┐
│           RECOMMENDATION ENGINE             │
├─────────────────────────────────────────────┤
│  Input: user_id, purchase_history,          │
│         browsing_history, ratings           │
└────────────┬────────────────────────────────┘
             │
    ┌────────┴────────┬─────────────────┐
    ↓                 ↓                 ↓
┌─────────┐    ┌──────────┐    ┌─────────────┐
│ COLLAB. │    │ CONTENT  │    │ POPULARITY  │
│FILTERING│    │ -BASED   │    │ /TRENDING   │
└────┬────┘    └────┬─────┘    └──────┬──────┘
     │              │                 │
     ├─ User-Based  ├─ TF-IDF         ├─ Recent sales
     ├─ Item-Based  ├─ Embeddings     ├─ Recent views
     └─ Matrix Fact.└─ Features       └─ Ratings
                       Similarity
     │              │                 │
     └────────┬─────┴─────────────────┘
              ↓
        ┌──────────────────┐
        │ HYBRID RANKER    │
        │ Weight Scores    │
        │ (W1: 0.5,        │
        │  W2: 0.3,        │
        │  W3: 0.2)        │
        └────────┬─────────┘
                 ↓
        ┌──────────────────┐
        │ DIVERSITY FILTER │
        │ Ensure variety   │
        │ across categories│
        └────────┬─────────┘
                 ↓
        ┌──────────────────┐
        │ COLD START HANDLER
        │ New user: popular
        │ New product: desc.
        └────────┬─────────┘
                 ↓
        ┌──────────────────┐
        │  TOP-20 RESULTS  │
        │  With Diversity  │
        └──────────────────┘

Algorithms Explained:

1. Collaborative Filtering (CF)
   - User-Based: If users A & B rated same products similarly,
                 recommend to A what B liked but A hasn't seen
   - Item-Based: If products X & Y are co-purchased often,
                 recommend X to users who liked Y
   - Matrix Fact.: Factorize user-item matrix into latent factors
                   User = [factor1, factor2, ..., factor_k]
                   Product = [factor1, factor2, ..., factor_k]
                   Score = User · Product (dot product)

2. Content-Based (CB)
   - Product Features: category, brand, price, description, ratings
   - TF-IDF: Vectorize product descriptions, measure similarity
   - Similarity: Cosine similarity between feature vectors
   - Personalized: Recommend products similar to ones user liked

3. Hybrid
   - Combine CF (collaborative signal) + CB (content signal)
   - Weights: CF 50%, CB 30%, Popularity 20%
   - Better coverage (handles cold start)
   - More diverse recommendations

Cold Start Problem:
   - New User: Use popularity-based or content-based approach
              → Popular/trending products
              → Products matching user's browsing signals
   - New Product: Use content-based + item-based approach
                 → Similar existing products
                 → Products in same category
```

---

## 2. Database Schema & ER Diagram

### 2.1 ER Diagram (ASCII)

```
                    ┌─────────────┐
                    │    Users    │
                    ├─────────────┤
                    │ id (PK)     │
                    │ email       │────┐
                    │ password    │    │
                    │ name        │    │
                    │ phone       │    │
                    │ created_at  │    │
                    │ updated_at  │    │
                    └─────────────┘    │
                         ▲ │           │
           ┌─────────────┘ │           │
           │               │           │
           │        ┌──────┴────────┐  │
           │        │               │  │
      ┌────┴──┐  ┌──┴────┐    ┌─────┴──┘
      │ Orders│  │ Cart  │    │ Wishlist
      ├───────┤  ├───────┤    ├────────
      │ id(PK)│  │ id(PK)│    │ id(PK)
      │user_id├──┤user_id├────┤user_id
      │..date │  │       │    │
      └───┬───┘  └───┬───┘    │product_id
          │          │        │created_at
          │          │        └────────
          │       ┌──┴─────────────────┐
          │       │                    │
      ┌───┴───┐   │   ┌─────────────┐  │
      │Order  │   └───┤  Products   │◄─┘
      │Items  │       ├─────────────┤
      ├───────┤       │ id (PK)     │
      │ id(PK)│       │ name        │
      │order_id├──────┤ description │
      │product_id     │ price       │
      │quantity│      │ category_id ├────┐
      │price   │      │ brand_id    ├──┐ │
      └───────┘       │ stock       │  │ │
                      │ created_at  │  │ │
                      └─────────────┘  │ │
                            ▲          │ │
                            │          │ │
                      ┌─────┴┐    ┌────┴─┴──┐
                      │      │    │         │
                  ┌───┴─┐  ┌─┴───┴──┐  ┌──┴──┐
                  │     │  │        │  │     │
            ┌─────┴──┐  │  │Reviews │  │Categ│
            │Ratings │  │  ├────────┤  ├─────┤
            ├────────┤  │  │id (PK) │  │id(PK)
            │id (PK) │  │  │product_id  name
            │product_│◄─┘  │user_id │
            │id      │     │rating  │
            │user_id ├─────┤review  │
            │rating  │     │created_│
            │created_│     └────────┘
            └────────┘
```

### 2.2 SQL Schema

```sql
-- Users Table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    avatar_url VARCHAR(500),
    bio TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
);

-- Categories Table
CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name)
);

-- Brands Table
CREATE TABLE brands (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    logo_url VARCHAR(500),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name)
);

-- Products Table (Core Product Catalog)
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    discount_price DECIMAL(10, 2),
    category_id INT NOT NULL,
    brand_id INT,
    stock_quantity INT DEFAULT 0,
    image_url VARCHAR(500),
    rating DECIMAL(3, 2) DEFAULT 0,
    review_count INT DEFAULT 0,
    sku VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (brand_id) REFERENCES brands(id),
    INDEX idx_category (category_id),
    INDEX idx_price (price),
    INDEX idx_rating (rating),
    INDEX idx_created_at (created_at),
    FULLTEXT INDEX ft_name_description (name, description)
);

-- User Activity Log (for ML features)
CREATE TABLE user_activity (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    activity_type ENUM('view', 'click', 'add_to_cart', 'remove_from_cart', 'purchase', 'wishlist_add', 'wishlist_remove', 'review', 'rating') NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    INDEX idx_user_timestamp (user_id, timestamp),
    INDEX idx_product_timestamp (product_id, timestamp),
    INDEX idx_activity_type (activity_type)
);

-- Orders Table
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'confirmed', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    shipping_address TEXT NOT NULL,
    billing_address TEXT NOT NULL,
    payment_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- Order Items (Line items in an order)
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price_per_unit DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id),
    INDEX idx_order_id (order_id)
);

-- Shopping Cart
CREATE TABLE cart (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Cart Items
CREATE TABLE cart_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES cart(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id),
    UNIQUE KEY unique_cart_product (cart_id, product_id)
);

-- Wishlist
CREATE TABLE wishlist (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    UNIQUE KEY unique_user_product (user_id, product_id),
    INDEX idx_user_id (user_id)
);

-- Product Ratings (1-5 stars, numeric)
CREATE TABLE ratings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    UNIQUE KEY unique_user_product (user_id, product_id),
    INDEX idx_product_id (product_id),
    INDEX idx_user_id (user_id)
);

-- Product Reviews (Text reviews)
CREATE TABLE reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    helpful_count INT DEFAULT 0,
    unhelpful_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    INDEX idx_product_id (product_id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);

-- Recommendation Cache (Store pre-computed recommendations)
CREATE TABLE recommendation_cache (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    product_ids JSON NOT NULL,  -- Array of recommended product IDs
    recommendation_type ENUM('personalized', 'collaborative', 'content_based', 'hybrid') NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE KEY unique_user_type (user_id, recommendation_type),
    INDEX idx_expires_at (expires_at)
);

-- Search Query Log (for analytics)
CREATE TABLE search_queries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    query VARCHAR(255) NOT NULL,
    results_count INT,
    clicked_product_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (clicked_product_id) REFERENCES products(id),
    INDEX idx_query (query),
    INDEX idx_timestamp (timestamp)
);

-- Sessions (JWT sessions tracking)
CREATE TABLE sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    token_jti VARCHAR(500) UNIQUE,  -- JWT ID for token revocation
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_expires_at (expires_at)
);
```

### 2.3 Indexing Strategy

| Table | Index | Reason |
|-------|-------|--------|
| users | email | Unique lookup during login |
| products | category_id, price, rating | Filtering, sorting |
| products | FULLTEXT(name, description) | Full-text search |
| orders | user_id, status, created_at | Order history queries |
| user_activity | user_id+timestamp | Recent activity queries |
| ratings | product_id, unique(user_id, product_id) | Aggregate ratings, CF |
| wishlist | user_id | User's wishlist queries |
| reviews | product_id, created_at | Product reviews sorting |
| recommendation_cache | user_id+type, expires_at | Cache lookup, expiration |

---

## 3. API Architecture

### 3.1 RESTful API Endpoints

```
Authentication:
POST   /api/auth/register          - Register new user
POST   /api/auth/login             - Login, get JWT
POST   /api/auth/refresh           - Refresh JWT token
POST   /api/auth/logout            - Logout, blacklist token

User Management:
GET    /api/users/me               - Get current user
PUT    /api/users/me               - Update profile
GET    /api/users/me/preferences   - Get user preferences
PUT    /api/users/me/preferences   - Update preferences

Products:
GET    /api/products               - List products (paginated, filtered)
GET    /api/products/search        - Search products
GET    /api/products/{id}          - Get product details
GET    /api/products/{id}/similar  - Get similar products
POST   /api/products               - Create product (admin)
PUT    /api/products/{id}          - Update product (admin)
DELETE /api/products/{id}          - Delete product (admin)

Categories:
GET    /api/categories             - List all categories
GET    /api/categories/{id}        - Get category details

Brands:
GET    /api/brands                 - List all brands

Cart:
GET    /api/cart                   - Get current cart
POST   /api/cart/items             - Add item to cart
PUT    /api/cart/items/{item_id}   - Update cart item quantity
DELETE /api/cart/items/{item_id}   - Remove item from cart
DELETE /api/cart                   - Clear cart

Wishlist:
GET    /api/wishlist               - Get user's wishlist
POST   /api/wishlist/items         - Add to wishlist
DELETE /api/wishlist/items/{id}    - Remove from wishlist

Orders:
GET    /api/orders                 - List user's orders
GET    /api/orders/{id}            - Get order details
POST   /api/orders                 - Create order (checkout)
PUT    /api/orders/{id}            - Update order status (admin)

Ratings & Reviews:
GET    /api/products/{id}/ratings  - Get product ratings
POST   /api/products/{id}/ratings  - Create/update rating
GET    /api/products/{id}/reviews  - Get product reviews
POST   /api/products/{id}/reviews  - Create review
PUT    /api/reviews/{id}           - Update review
DELETE /api/reviews/{id}           - Delete review

Recommendations (Core ML APIs):
GET    /api/recommendations        - Get personalized recommendations
GET    /api/recommendations/trending - Get trending products
GET    /api/products/{id}/also-bought - "People who bought this also bought"
GET    /api/users/me/recommendations - Get top-N personalized recs

Analytics (Admin):
GET    /api/analytics/dashboard    - Get dashboard metrics
GET    /api/analytics/users        - User analytics
GET    /api/analytics/products     - Product analytics
GET    /api/analytics/recommendations - Recommendation performance
```

### 3.2 Request/Response Format

```json
-- Success Response
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Product Name",
    ...
  },
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  },
  "timestamp": "2024-01-15T10:30:00Z"
}

-- Error Response
{
  "success": false,
  "error": {
    "code": "PRODUCT_NOT_FOUND",
    "message": "Product with ID 999 not found",
    "details": {}
  },
  "timestamp": "2024-01-15T10:30:00Z"
}

-- Recommendation Response
{
  "success": true,
  "data": {
    "recommendations": [
      {
        "product_id": 123,
        "name": "Product Name",
        "price": 49.99,
        "rating": 4.5,
        "reason": "collaborative_filtering",
        "score": 0.95
      },
      ...
    ],
    "model_version": "v1.0.2",
    "generated_at": "2024-01-15T10:30:00Z"
  }
}
```

---

## 4. Authentication & Authorization Flow

```
┌──────────────────────────────────────────────────────────┐
│               LOGIN/AUTHENTICATION FLOW                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│ User inputs email/password                              │
│         ↓                                                │
│ POST /api/auth/login                                    │
│         ↓                                                │
│ Backend validates credentials (hash comparison)         │
│         ↓                                                │
│ IF valid:                                               │
│   - Create JWT Token                                    │
│   - JWT payload: {user_id, email, role, exp}           │
│   - Sign with RS256 (private key)                       │
│   - Return token in response                            │
│   - Store in httpOnly cookie (secure)                   │
│         ↓                                                │
│ IF invalid:                                             │
│   - Return 401 Unauthorized                             │
│   - Suggest signup                                      │
│                                                          │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│          SUBSEQUENT REQUEST (Authorization)              │
├──────────────────────────────────────────────────────────┤
│                                                          │
│ Client sends request with JWT in Authorization header   │
│   Authorization: Bearer <JWT_TOKEN>                     │
│         ↓                                                │
│ Backend Auth Middleware:                                │
│   1. Extract token from header                          │
│   2. Verify signature using public key                  │
│   3. Check token expiration                             │
│   4. Extract user_id from payload                       │
│   5. Add user context to request                        │
│         ↓                                                │
│ IF valid: Request proceeds to route handler             │
│ IF invalid: Return 401 Unauthorized                     │
│                                                          │
└──────────────────────────────────────────────────────────┘

Roles & Permissions:
- admin: Create/update/delete products, view analytics
- user: Browse, search, purchase, review, get recommendations
- guest: Browse products (no personalized recs)
```

---

## 5. Recommendation Pipeline Architecture

```
┌──────────────────────────────────────────────────────────┐
│      OFFLINE TRAINING PIPELINE (Daily/Weekly)           │
├──────────────────────────────────────────────────────────┤
│                                                          │
│ 1. DATA EXTRACTION                                       │
│    MySQL → Load user-product interactions               │
│            Load product features                        │
│            Load user preferences                        │
│         ↓                                                │
│ 2. DATA CLEANING (PySpark)                              │
│    - Remove duplicates                                  │
│    - Handle missing values                              │
│    - Remove outliers                                    │
│    - Validate data types                                │
│         ↓                                                │
│ 3. FEATURE ENGINEERING (PySpark)                        │
│    - TF-IDF for product descriptions                   │
│    - Normalize prices                                   │
│    - Encode categories                                  │
│    - User engagement score: log(views) + purchases     │
│    - Recency weighting: recent activities weighted higher
│    - Product popularity: normalize by category          │
│         ↓                                                │
│ 4. MODEL TRAINING (Python ML)                           │
│    - Train Collaborative Filtering models               │
│      • KNN for user-based & item-based CF              │
│      • Matrix Factorization (SVD/ALS)                  │
│    - Train Content-Based model                          │
│      • TF-IDF + Cosine Similarity                       │
│    - Train Hybrid model                                 │
│      • Weighted combination                             │
│         ↓                                                │
│ 5. MODEL EVALUATION                                      │
│    - Precision@K, Recall@K                              │
│    - Coverage, Diversity, Novelty                       │
│    - RMSE/MAE for rating predictions                    │
│    - A/B test metrics                                   │
│         ↓                                                │
│ 6. MODEL PERSISTENCE                                     │
│    - Save as pickle files or ONNX                       │
│    - Store model metadata (version, date, metrics)      │
│         ↓                                                │
│ 7. PRECOMPUTE & CACHE (optional, for hot items)         │
│    - Generate top-N recommendations for all users       │
│    - Store in recommendation_cache table                │
│    - Generate trending products list                    │
│                                                          │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│      ONLINE SERVING (Real-time API)                      │
├──────────────────────────────────────────────────────────┤
│                                                          │
│ User requests GET /api/recommendations                  │
│         ↓                                                │
│ Recommendation Service:                                 │
│   1. Check recommendation cache (Redis)                 │
│      IF cached & fresh → Return cached result           │
│         ↓                                                │
│   2. Get user context:                                  │
│      - User's purchase history                          │
│      - User's ratings & reviews                         │
│      - Browse history                                   │
│      - Wishlist items                                   │
│         ↓                                                │
│   3. Load pre-trained models from disk/cache           │
│         ↓                                                │
│   4. Generate Recommendations:                          │
│      - Collaborative Filtering score                    │
│      - Content-Based score                              │
│      - Popularity score                                 │
│      - Hybrid: W1*CF + W2*CB + W3*Popularity           │
│         ↓                                                │
│   5. Apply Filters:                                     │
│      - Exclude already purchased                        │
│      - Exclude out of stock                             │
│      - Apply user preferences (categories, price)       │
│      - Diversity: max 3 per category                    │
│         ↓                                                │
│   6. Rank & Sort                                        │
│      - Top-20 by score                                  │
│      - Apply diversity constraints                      │
│         ↓                                                │
│   7. Cache Result (Redis, 24h TTL)                     │
│      - Store in recommendation_cache table              │
│         ↓                                                │
│   8. Return to User                                      │
│      - Include product details                          │
│      - Include "reason" (why recommended)               │
│      - Include confidence score                         │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 6. Deployment Architecture

```
┌───────────────────────────────────────────────────────────┐
│                    PRODUCTION ARCHITECTURE                │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────────────────────────┐            │
│  │         FRONTEND (Next.js 16)            │            │
│  │  - Server-side rendering                │            │
│  │  - API routes                           │            │
│  │  - Static optimization                  │            │
│  │  - Deployed on Vercel/AWS EC2           │            │
│  └────────────┬────────────────────────────┘            │
│               │ HTTPS                                   │
│               ↓                                          │
│  ┌─────────────────────────────────────────┐            │
│  │      LOAD BALANCER (Nginx)              │            │
│  │  - Route requests                       │            │
│  │  - SSL termination                      │            │
│  │  - Request rate limiting                │            │
│  └────────────┬────────────────────────────┘            │
│               │ Internal Network                        │
│               ↓                                          │
│  ┌─────────────────────────────────────────┐            │
│  │    API BACKEND (FastAPI) - Scaled      │            │
│  │  Container 1 │ Container 2 │ Container 3│            │
│  │  - Gunicorn   │ - Gunicorn  │ - Gunicorn │            │
│  │  - FastAPI    │ - FastAPI   │ - FastAPI  │            │
│  │  - Port 8000  │ - Port 8000 │ - Port 8000│            │
│  └────────────┬────────────────────────────┘            │
│               │                                         │
│    ┌──────────┴──────────┬────────────────┐             │
│    ↓                     ↓                ↓             │
│  ┌──────────┐  ┌──────────────┐  ┌────────────┐        │
│  │ MySQL DB │  │ Redis Cache  │  │ File Store │        │
│  │  Master  │  │  (for quick  │  │ (S3 for    │        │
│  │  + Slave │  │   lookup)    │  │ images)    │        │
│  └──────────┘  └──────────────┘  └────────────┘        │
│       ↑                                                  │
│       │ (Batch Processing - Scheduled)                 │
│       ↓                                                  │
│  ┌──────────────────────────────────┐                  │
│  │  PySpark Batch Processing        │                  │
│  │  (Daily/Weekly scheduled jobs)   │                  │
│  │  - ML model training             │                  │
│  │  - Feature engineering           │                  │
│  │  - Cache pre-computed recs       │                  │
│  └──────────────────────────────────┘                  │
│                                                           │
│  ┌──────────────────────────────────┐                  │
│  │  Monitoring & Logging             │                  │
│  │  - ELK Stack (Elasticsearch,      │                  │
│  │    Logstash, Kibana)              │                  │
│  │  - Prometheus + Grafana           │                  │
│  │  - Alert system                   │                  │
│  └──────────────────────────────────┘                  │
│                                                           │
└───────────────────────────────────────────────────────────┘

Docker Compose (Development):
- 1 service: mysql (database)
- 1 service: redis (cache)
- 1 service: backend (FastAPI)
- 1 service: frontend (Next.js - dev)
- 1 service: ml-pipeline (PySpark jobs)
```

---

## 7. Data Flow Diagrams

### 7.1 User Purchase → Recommendation Flow

```
User Purchases Product
    ↓
Activity logged: user_activity table
    ↓ (Trigger or scheduled job)
Update user's ratings/preferences
    ↓ (Daily batch job)
PySpark re-trains ML models
    ↓
Pre-compute new recommendations
    ↓
Store in recommendation_cache
    ↓
Next time user logs in → Serve cached recommendations
    ↓
User views recommendations → Log clicks/impressions
    ↓ (Feedback loop)
Improve model over time
```

### 7.2 Recommendation Generation Detail

```
GET /api/recommendations (user_id = 42)
    ↓
┌─────────────────────────────────────────────────┐
│ Recommendation Service                          │
├─────────────────────────────────────────────────┤
│ 1. Load user profile:                           │
│    - Age, Gender, Location                      │
│    - Purchase history (last 6 months)           │
│    - Ratings & reviews                          │
│    - Browse history                             │
│    - Wishlist                                   │
│                                                 │
│ 2. Load models:                                 │
│    - CF model: latent_factors_user[42]         │
│    - CB model: TF-IDF vectors                  │
│    - Popularity model: popularity_scores       │
│                                                 │
│ 3. Generate initial scores (for all products):│
│    FOR each product P:                          │
│      - CF_score = dot(user_factors, prod_factors)
│      - CB_score = cosine_sim(user_profile, P) │
│      - POP_score = popularity[P]               │
│      - HYBRID_score = 0.5*CF + 0.3*CB + 0.2*POP
│                                                 │
│ 4. Filter products:                            │
│    - Remove already purchased                  │
│    - Remove out of stock                       │
│    - Remove hidden products                    │
│    - Apply user preferences                    │
│                                                 │
│ 5. Apply diversity:                            │
│    - Sort by score descending                  │
│    - For each product, check category          │
│    - Max 3 per category in final list          │
│    - Result: diverse top-20 list               │
│                                                 │
│ 6. Enrich response:                            │
│    - Add product images, price, rating         │
│    - Add "reason": why recommended             │
│    - Add confidence_score (0-1)                │
│                                                 │
│ 7. Cache result (Redis, 24h)                  │
│    - Key: recommendation:user:42               │
│    - TTL: 86400 seconds                        │
│                                                 │
└─────────────────────────────────────────────────┘
    ↓
Return JSON response with top-20 recommendations
```

---

## Summary of Phase 2

Completed comprehensive system architecture covering:
- ✅ Frontend architecture (Next.js components, state management)
- ✅ Backend architecture (FastAPI services, layered design)
- ✅ Data pipeline (PySpark for batch processing)
- ✅ ML/AI architecture (3-tier recommendation system)
- ✅ Complete database schema (13 tables, optimized indexes)
- ✅ RESTful API design (35+ endpoints)
- ✅ Authentication & authorization flow
- ✅ Recommendation pipeline (offline & online)
- ✅ Deployment architecture (containerized, scalable)

**Key Design Decisions**:
- Clean layered architecture (Controller → Service → Repository → DB)
- Repository pattern for data access abstraction
- Recommendation system combines CF, CB, and hybrid approaches
- PySpark for distributed ML training
- Redis for caching recommendations
- JWT for stateless authentication

**Ready for Phase 3-4**: Database implementation and FastAPI backend

