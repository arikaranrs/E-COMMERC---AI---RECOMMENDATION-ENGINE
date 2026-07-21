# Architecture Visual Guide - Phase 1

## System Overview Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER'S BROWSER                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │             NEXT.JS 16 REACT FRONTEND                      │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │ Components (ProductCard, Header, LoginForm, etc.)   │  │ │
│  │  ├──────────────────────────────────────────────────────┤  │ │
│  │  │ Hooks (useProducts, useAuth, useCart)               │  │ │
│  │  ├──────────────────────────────────────────────────────┤  │ │
│  │  │ Stores (Zustand: auth, cart, UI state)              │  │ │
│  │  ├──────────────────────────────────────────────────────┤  │ │
│  │  │ API Client (fetch with Authorization header)        │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────┬──────────────────────────────────────────────┘
                  │ HTTP Requests
                  │ GET /api/v1/products
                  │ POST /api/v1/auth/login
                  │ Authorization: Bearer <JWT>
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI PYTHON BACKEND                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ MIDDLEWARE LAYER                                           │ │
│  │ ├─ CORSMiddleware (allow frontend domain)                │ │
│  │ ├─ AuthMiddleware (verify JWT tokens)                    │ │
│  │ └─ ErrorHandlerMiddleware (catch exceptions)             │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ROUTES LAYER (api/v1/)                                    │ │
│  │ ├─ auth.py: /login, /register, /logout, /refresh        │ │
│  │ ├─ products.py: /products, /products/{id}, /search       │ │
│  │ ├─ cart.py: /cart, /cart/add, /cart/remove               │ │
│  │ ├─ orders.py: /orders, /orders/{id}, /orders/create     │ │
│  │ ├─ users.py: /profile, /profile/update                   │ │
│  │ └─ recommendations.py: /recommendations                   │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ SERVICES LAYER (services/)                               │ │
│  │ ├─ auth_service: Register, login, verify, create JWT    │ │
│  │ ├─ product_service: Filter, search, get details         │ │
│  │ ├─ cart_service: Calculate totals, validate             │ │
│  │ ├─ order_service: Create order, process payment         │ │
│  │ ├─ user_service: Manage profile                         │ │
│  │ └─ recommendation_service: Call AI model                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ REPOSITORIES LAYER (repositories/)                       │ │
│  │ ├─ user_repository: find_by_email, create, update       │ │
│  │ ├─ product_repository: find_all, filter_by_category     │ │
│  │ ├─ order_repository: create_order, get_user_orders     │ │
│  │ ├─ review_repository: add_review, get_reviews          │ │
│  │ └─ wishlist_repository: add, remove, get_wishlist      │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ MODELS LAYER (models/) - SQLAlchemy ORM                  │ │
│  │ ├─ User: Maps to users table                             │ │
│  │ ├─ Product: Maps to products table                       │ │
│  │ ├─ Order: Maps to orders table                           │ │
│  │ ├─ OrderItem: Maps to order_items table                  │ │
│  │ ├─ Review: Maps to reviews table                         │ │
│  │ ├─ Recommendation: Maps to recommendations table         │ │
│  │ └─ Wishlist: Maps to wishlists table                     │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ UTILS & CONFIG                                           │ │
│  │ ├─ jwt_utils: create_token, verify_token                │ │
│  │ ├─ password_utils: hash_password, verify_password       │ │
│  │ ├─ database.py: session management                      │ │
│  │ ├─ logger.py: logging setup                             │ │
│  │ └─ config.py: environment variables                     │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────┬──────────────────────────────────────────────┘
                  │ SQL Queries
                  │ SELECT * FROM products WHERE category = ?
                  │ INSERT INTO users (email, password_hash) VALUES (?, ?)
                  │ UPDATE orders SET status = 'shipped' WHERE id = ?
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│                      MYSQL DATABASE                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ TABLES (13 total)                                         │ │
│  │ ├─ users: id, email, password_hash, name, created_at   │ │
│  │ ├─ sessions: id, user_id, token, expires_at             │ │
│  │ ├─ products: id, name, price, stock, category_id        │ │
│  │ ├─ categories: id, name, description                    │ │
│  │ ├─ orders: id, user_id, total_price, status             │ │
│  │ ├─ order_items: id, order_id, product_id, qty, price   │ │
│  │ ├─ reviews: id, user_id, product_id, rating, text       │ │
│  │ ├─ carts: id, user_id, created_at                       │ │
│  │ ├─ cart_items: id, cart_id, product_id, qty             │ │
│  │ ├─ wishlists: id, user_id, product_id                   │ │
│  │ ├─ recommendations: id, user_id, product_id, score      │ │
│  │ ├─ ratings: id, user_id, product_id, rating             │ │
│  │ └─ brands: id, name, logo_url                           │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
         Separate Components (not in main request flow):
         ↓                                    ↓
┌────────────────────────────┐    ┌────────────────────────────┐
│  ML PIPELINE (PySpark)     │    │  AI SERVICE (Python ML)    │
│                            │    │                            │
│ Runs nightly (10 PM):      │    │ Runs on-demand:           │
│                            │    │                            │
│ 1. Extract from database   │    │ 1. Load trained models    │
│ 2. Engineer features       │    │ 2. Make prediction        │
│ 3. Train models (5 types)  │    │ 3. Return top 5 products  │
│ 4. Save to disk            │    │                            │
│                            │    │ Used by:                  │
│ Outputs:                   │    │ recommendation_service    │
│ saved_models/v1/          │    │                            │
│ ├─ collaborative.pkl      │    │ Speed: milliseconds       │
│ ├─ content_based.pkl      │    │                            │
│ └─ hybrid.pkl             │    │                            │
│                            │    │                            │
│ Technologies:              │    │ Technologies:             │
│ - PySpark                  │    │ - Scikit-learn           │
│ - Pandas                   │    │ - TensorFlow (optional)  │
│ - Scikit-learn            │    │ - NumPy                   │
│ - NumPy                    │    │ - Pickle                  │
└────────────────────────────┘    └────────────────────────────┘
```

## Request Flow: "Get Products"

```
STEP 1: User Action (Frontend)
┌─────────────────────────────────────────┐
│ User clicks "Electronics" category      │
│ Component: ProductFilter.tsx            │
│ Handler: onClick() event                │
│ State: useProducts hook triggers        │
└────────────────┬────────────────────────┘
                 │
                 ↓
STEP 2: API Call (Frontend)
┌─────────────────────────────────────────┐
│ const { data } = useSWR(                │
│   '/api/v1/products?category=electronics' │
│ )                                       │
│                                         │
│ lib/api-client.ts:                      │
│ - Create fetch request                  │
│ - Add Authorization: Bearer <JWT>       │
│ - Send to backend                       │
└────────────────┬────────────────────────┘
                 │ HTTP GET /api/v1/products?category=electronics
                 ↓
STEP 3: Route Handler (Backend)
┌─────────────────────────────────────────┐
│ api/v1/products.py:                     │
│ @router.get("/")                        │
│ async def get_products(                 │
│   category: str = Query(None),          │
│   db: Session = Depends(get_db)         │
│ )                                       │
│                                         │
│ 1. Middleware verified JWT ✓            │
│ 2. Pydantic validated query params ✓    │
│ 3. Now call service layer               │
└────────────────┬────────────────────────┘
                 │
                 ↓
STEP 4: Service Layer (Backend)
┌─────────────────────────────────────────┐
│ services/product_service.py:            │
│ def get_products(category, db):         │
│   1. Validate category (empty check)    │
│   2. Call repository for data           │
│   3. Apply business logic (sorting)     │
│   4. Return list of products            │
│                                         │
│ repository = ProductRepository(db)      │
│ products = repository.find_by_category( │
│   category='electronics'                │
│ )                                       │
└────────────────┬────────────────────────┘
                 │
                 ↓
STEP 5: Repository Layer (Backend)
┌─────────────────────────────────────────┐
│ repositories/product_repository.py:     │
│ def find_by_category(category):         │
│   query = session.query(Product)        │
│            .filter(                     │
│              Product.category ==        │
│              category                   │
│            )                            │
│   return query.all()                    │
│                                         │
│ SQLAlchemy translates to:               │
│ SELECT * FROM products                  │
│ WHERE category = 'electronics'          │
└────────────────┬────────────────────────┘
                 │ SQL Query
                 ↓
STEP 6: Database (MySQL)
┌─────────────────────────────────────────┐
│ Executes SQL:                           │
│ SELECT * FROM products                  │
│ WHERE category = 'electronics'          │
│                                         │
│ Results:                                │
│ id | name      | price | category      │
│ 1  | Laptop    | 999   | electronics   │
│ 2  | Mouse     | 25    | electronics   │
│ 3  | Keyboard  | 75    | electronics   │
└────────────────┬────────────────────────┘
                 │ Returns rows
                 ↓
STEP 7: Data Flows Back Up
┌─────────────────────────────────────────┐
│ Repository gets rows → Product objects  │
│                                         │
│ Service gets Product objects            │
│    - Already validated ✓                │
│    - Already filtered ✓                 │
│    - Return as is                       │
│                                         │
│ Route gets result from service          │
│    - Convert to Pydantic schema         │
│    - Serialize to JSON                  │
│    - Add HTTP headers                   │
└────────────────┬────────────────────────┘
                 │ HTTP 200
                 │ Content-Type: application/json
                 ↓
STEP 8: Frontend Receives Response
┌─────────────────────────────────────────┐
│ JSON Response:                          │
│ [                                       │
│   {                                     │
│     "id": 1,                            │
│     "name": "Laptop",                   │
│     "price": 999,                       │
│     "category": "electronics"           │
│   },                                    │
│   ...                                   │
│ ]                                       │
│                                         │
│ useSWR hook receives data               │
│ - Updates cache                         │
│ - Triggers re-render                    │
└────────────────┬────────────────────────┘
                 │
                 ↓
STEP 9: UI Updates
┌─────────────────────────────────────────┐
│ ProductGrid.tsx re-renders:             │
│ {products.map(product => (              │
│   <ProductCard product={product} />     │
│ ))}                                     │
│                                         │
│ User sees:                              │
│ ┌──────────────────┐                    │
│ │ Laptop    $999   │                    │
│ │ ⭐⭐⭐⭐⭐      │                    │
│ │ "Add to Cart"    │                    │
│ └──────────────────┘                    │
│ ┌──────────────────┐                    │
│ │ Mouse     $25    │                    │
│ │ ⭐⭐⭐⭐      │                    │
│ │ "Add to Cart"    │                    │
│ └──────────────────┘                    │
└─────────────────────────────────────────┘
```

## Authentication Flow

```
┌─────────────────────────────────────────────────────────┐
│ LOGIN REQUEST                                           │
│ Frontend: POST /api/v1/auth/login                       │
│ Body: {email: "john@example.com", password: "secret"} │
└─────────┬───────────────────────────────────────────────┘
          │
          ↓
┌─────────────────────────────────────────────────────────┐
│ BACKEND - AUTH ROUTE (api/v1/auth.py)                  │
│ 1. Validate request with LoginRequest schema           │
│ 2. Call auth_service.login(email, password)            │
└─────────┬───────────────────────────────────────────────┘
          │
          ↓
┌─────────────────────────────────────────────────────────┐
│ BACKEND - AUTH SERVICE (services/auth_service.py)      │
│ 1. Hash incoming password: bcrypt.hash(password)       │
│    Input: "secret"                                      │
│    Output: "$2b$12$sda9f7as8f..."                       │
│                                                         │
│ 2. Find user: repository.find_by_email(email)          │
│    Query: SELECT * FROM users WHERE email = ?          │
│                                                         │
│ 3. Compare hashes:                                      │
│    bcrypt.verify(                                       │
│      password="secret",                                 │
│      hashed="$2b$12$..." from DB                        │
│    ) → True/False                                       │
│                                                         │
│ 4. If match:                                            │
│    token = create_access_token(user_id)                │
│    Returns: {access_token: "...", token_type: "bearer"}│
│                                                         │
│ 5. If no match: raise LoginError                        │
└─────────┬───────────────────────────────────────────────┘
          │
          ↓
┌─────────────────────────────────────────────────────────┐
│ BACKEND - JWT UTILS (utils/jwt_utils.py)              │
│ create_access_token(user_id=1):                         │
│                                                         │
│ Payload: {                                              │
│   "user_id": 1,                                         │
│   "exp": 1704067200,  ← expiration time               │
│   "iat": 1704063600   ← issued at time                │
│ }                                                       │
│                                                         │
│ Sign with secret: HMAC-SHA256(payload, SECRET_KEY)     │
│                                                         │
│ Result:                                                 │
│ eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.                 │
│ eyJ1c2VyX2lkIjogMSwgImV4cCI6IDE3MDQwNjcyMDB9.         │
│ SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c          │
│                                                         │
│ (header . payload . signature)                          │
└─────────┬───────────────────────────────────────────────┘
          │
          ↓
┌─────────────────────────────────────────────────────────┐
│ FRONTEND - STORE TOKEN                                  │
│ Response: {                                             │
│   "access_token": "eyJhbGciOiJIUzI1NiIs...",          │
│   "token_type": "bearer"                                │
│ }                                                       │
│                                                         │
│ useAuthStore.login():                                   │
│   set({                                                 │
│     token: "eyJhbGciOiJIUzI1NiIs...",                  │
│     user: {id: 1, email: "john@example.com"}           │
│   })                                                    │
│                                                         │
│ localStorage.setItem("token", token)                    │
└─────────┬───────────────────────────────────────────────┘
          │
          ↓
┌─────────────────────────────────────────────────────────┐
│ SUBSEQUENT REQUESTS (NOW AUTHENTICATED)                 │
│ Frontend: GET /api/v1/products                          │
│ Header:   Authorization: Bearer eyJhbGciOiJIUzI1NiIs..│
└─────────┬───────────────────────────────────────────────┘
          │
          ↓
┌─────────────────────────────────────────────────────────┐
│ BACKEND - AUTH MIDDLEWARE                               │
│ 1. Extract token from header:                           │
│    "Bearer eyJhbGciOiJIUzI1NiIs..." → "eyJhbGciOiJIUzI1NiIs..." │
│                                                         │
│ 2. Verify signature:                                    │
│    HMAC-SHA256(header.payload, SECRET_KEY) == signature│
│    If NO match: Invalid token → 401 Unauthorized       │
│                                                         │
│ 3. Check expiration:                                    │
│    current_time > exp → Token expired → 401             │
│                                                         │
│ 4. Decode token:                                        │
│    payload = decode(token)                              │
│    user_id = payload["user_id"]                         │
│                                                         │
│ 5. Attach to request:                                   │
│    request.user = {id: 1}                               │
│                                                         │
│ 6. Continue to route handler (authenticated) ✓          │
└─────────────────────────────────────────────────────────┘
```

## Layered Architecture Benefits

```
WITHOUT LAYERS (Monolithic):
┌────────────────────────────────────┐
│ One giant file: app.py             │
│ ├─ HTTP handling                   │
│ ├─ Password hashing                │
│ ├─ Database queries (SQL mixed)    │
│ ├─ Business logic                  │
│ ├─ Error handling                  │
│ ├─ Logging                         │
│ └─ Configuration                   │
│                                    │
│ Problems:                          │
│ - Hard to test                     │
│ - Hard to modify                   │
│ - Hard to reuse                    │
│ - Hard to scale (team)             │
└────────────────────────────────────┘

WITH LAYERS (Separated Concerns):
┌────────────────────────────────────┐
│ Routes (api/)     ← HTTP handling  │
├────────────────────────────────────┤
│ Services (services/) ← Business logic
├────────────────────────────────────┤
│ Repositories (repositories/) ← DB  │
├────────────────────────────────────┤
│ Models (models/)  ← ORM definitions │
├────────────────────────────────────┤
│ Utils (utils/)    ← Helpers        │
└────────────────────────────────────┘

Benefits:
✓ Easy to test (mock each layer)
✓ Easy to modify (change one layer)
✓ Easy to reuse (business logic)
✓ Easy to scale (team)
✓ Clear responsibilities
```

## ML Recommendation Flow

```
NIGHTLY TRAINING (10:00 PM):
┌─────────────────────────────────────────┐
│ PySpark Job starts                      │
│ ml_pipeline/jobs/training_scheduler.py  │
└──────────┬────────────────────────────┘
           │
           ↓
┌─────────────────────────────────────────┐
│ 1. Extract Data                         │
│ ml_pipeline/jobs/data_extraction.py     │
│                                         │
│ users_df = spark.sql("""               │
│   SELECT id, email FROM users          │
│ """)                                    │
│                                         │
│ products_df = spark.sql("""            │
│   SELECT id, name, category FROM products │
│ """)                                    │
│                                         │
│ orders_df = spark.sql("""              │
│   SELECT user_id, product_id           │
│   FROM orders                          │
│ """)                                    │
└──────────┬────────────────────────────┘
           │
           ↓
┌─────────────────────────────────────────┐
│ 2. Engineer Features                    │
│ ml_pipeline/jobs/feature_engineering.py │
│                                         │
│ User Features:                          │
│ - engagement_score (0-10)               │
│ - purchase_count                        │
│ - avg_purchase_value                    │
│ - days_since_last_purchase              │
│                                         │
│ Product Features:                       │
│ - popularity_score (0-100)              │
│ - avg_rating (0-5)                      │
│ - price (normalized 0-1)                │
│ - category (encoded 1-50)               │
│                                         │
│ normalized_features = normalize(features) │
└──────────┬────────────────────────────┘
           │
           ↓
┌─────────────────────────────────────────┐
│ 3. Train Models                         │
│ ml_pipeline/jobs/model_training.py      │
│                                         │
│ Collaborative Filtering:                │
│   model = train_cf(features)            │
│   Learns: users with similar taste      │
│                                         │
│ Content-Based:                          │
│   model = train_cb(features)            │
│   Learns: similar products = similar ⭐│
│                                         │
│ Hybrid:                                 │
│   model = train_hybrid(cf, cb)          │
│   Combines both for better accuracy     │
└──────────┬────────────────────────────┘
           │
           ↓
┌─────────────────────────────────────────┐
│ 4. Save Models                          │
│ ai_service/saved_models/v1/            │
│ ├─ collaborative_filtering.pkl          │
│ ├─ content_based.pkl                    │
│ └─ hybrid.pkl                           │
│                                         │
│ Job complete! (usually in 30-60 mins)   │
└──────────────────────────────────────────┘

NEXT DAY - USER REQUESTS RECOMMENDATIONS:
┌─────────────────────────────────────────┐
│ Frontend: GET /api/v1/recommendations   │
│ (User viewing product on homepage)      │
└──────────┬────────────────────────────┘
           │
           ↓
┌─────────────────────────────────────────┐
│ Backend Route Handler                   │
│ api/v1/recommendations.py               │
│                                         │
│ def get_recommendations(                │
│   user_id: int,                         │
│   db: Session                           │
│ ):                                      │
│   service = RecommendationService(db)   │
│   result = service.get_recommendations( │
│     user_id                             │
│   )                                     │
│   return result                         │
└──────────┬────────────────────────────┘
           │
           ↓
┌─────────────────────────────────────────┐
│ Recommendation Service                  │
│ services/recommendation_service.py      │
│                                         │
│ from ai_service.inference import        │
│   recommender                           │
│                                         │
│ # Get predictions from AI service       │
│ top_5 = recommender.recommend(          │
│   user_id=user_id,                      │
│   n=5                                   │
│ )                                       │
│ Returns: [product_id_1, ...]            │
│                                         │
│ # Fetch full product details from DB    │
│ products = repository.find_by_ids(      │
│   top_5                                 │
│ )                                       │
│                                         │
│ return products                         │
└──────────┬────────────────────────────┘
           │
           ↓
┌─────────────────────────────────────────┐
│ AI Service Inference                    │
│ ai_service/inference/recommender.py     │
│                                         │
│ 1. Load trained models from disk        │
│    cf_model = pickle.load(              │
│      'saved_models/v1/cf.pkl'           │
│    )                                    │
│    (happens once at startup)            │
│                                         │
│ 2. Get user features from DB            │
│    user_features = get_user_features(   │
│      user_id                            │
│    )                                    │
│                                         │
│ 3. Make prediction                      │
│    scores = cf_model.predict(           │
│      user_features                      │
│    )                                    │
│    Returns: array of scores per product │
│                                         │
│ 4. Get top 5                            │
│    top_5 = argsort(scores)[-5:]         │
│    Returns: [2, 5, 10, 15, 3]           │
│                                         │
│ All in milliseconds! ⚡                 │
└──────────┬────────────────────────────┘
           │
           ↓
┌─────────────────────────────────────────┐
│ Frontend Displays Recommendations       │
│                                         │
│ "Recommended for You:"                  │
│ ┌──────────────────┐                    │
│ │ Product 2 $199   │                    │
│ │ ⭐⭐⭐⭐⭐      │                    │
│ │ "Add to Cart"    │                    │
│ └──────────────────┘                    │
│ ┌──────────────────┐                    │
│ │ Product 5 $79    │                    │
│ │ ⭐⭐⭐⭐       │                    │
│ │ "Add to Cart"    │                    │
│ └──────────────────┘                    │
└─────────────────────────────────────────┘
```

This is Phase 1! The entire structure is now clear and documented.
