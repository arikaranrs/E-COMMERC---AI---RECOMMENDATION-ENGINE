# ML Pipeline & Data Engineering (Phase 1)

## What is the ML Pipeline?

The ML pipeline processes user behavior data and trains recommendation models.

## Pipeline Flow

```
Raw Data from Database
    ↓
Extract Features (PySpark)
├─ User behavior: clicks, purchases, views
├─ Product features: price, category, ratings
└─ Time-based features: seasonality, trends
    ↓
Feature Engineering (Data Transformation)
├─ Normalize prices (0-1 scale)
├─ Encode categories (electronics=1, clothing=2)
├─ Calculate user engagement score
    ↓
Machine Learning Models
├─ Collaborative Filtering: users like similar things
├─ Content-Based: similar products have similar ratings
├─ Hybrid: combine multiple approaches
    ↓
Trained Models Saved to Disk
    ↓
Inference Service Loads Models
    ↓
User views product
    ↓
AI Service: "Recommend these 5 products"
    ↓
Backend: Fetch product details
    ↓
Frontend: Display recommendations
```

## Data Processing

### What is PySpark?

- Distributed computing framework
- Process GB/TB of data in parallel
- Runs on multiple servers/cores
- Fast processing

### Why PySpark?

Without PySpark (single server):
- 100GB of data = 10 minutes to process
- Can only use one CPU core

With PySpark (distributed):
- 100GB of data = 1 minute (10x servers)
- Uses all CPU cores efficiently

### ETL = Extract, Transform, Load

1. **Extract**
   - Query database for raw data
   - User clicks, purchases, product ratings

2. **Transform**
   - Clean data (remove nulls, duplicates)
   - Engineer features (calculate scores)
   - Normalize values (0-1 range)

3. **Load**
   - Save processed data
   - Train models on processed data
   - Save trained models

### Example: Process User Behavior

Raw Data:
```
user_id  product_id  action      timestamp
1        10          view        2024-01-10 10:00
1        10          view        2024-01-10 10:05
1        10          click       2024-01-10 10:10
1        10          purchase    2024-01-10 11:00
2        20          view        2024-01-10 12:00
```

Transformed Data:
```
user_id  product_id  engagement_score  purchased
1        10          3.5               1
2        20          0.5               0
```

## Machine Learning Models

### 1. Collaborative Filtering

**Idea:** Users who bought similar things have similar taste

Example:
- John bought: laptop, mouse, keyboard
- Jane bought: laptop, mouse, headphones
- John hasn't bought headphones yet
- Recommend headphones to John (Jane likes it too!)

Algorithm:
```
1. Build user-product matrix
   Users: rows
   Products: columns
   Values: rating (0-5) or 1/0 (bought/not bought)

2. Find similar users
   Compare user vectors (similarity = dot product)

3. Recommend products
   Get products liked by similar users
```

### 2. Content-Based Filtering

**Idea:** Similar products have similar ratings

Example:
- John bought: Laptop (gaming, 4.5★)
- Recommend: Desktop Computer (gaming, 4.6★)
  (Similar features → similar ratings)

Algorithm:
```
1. Extract product features
   - Category
   - Price range
   - Average rating
   - Number of reviews

2. Calculate similarity
   - Euclidean distance between feature vectors
   - Products close together = similar

3. Recommend products
   - Rank by similarity to previously liked products
```

### 3. Hybrid Approach

**Idea:** Combine both methods

```
score = 0.6 * collaborative_score + 0.4 * content_score

Pros:
- Better accuracy
- Handles cold start (new users/products)
- More diverse recommendations
```

## ML Pipeline Components

### jobs/
```
jobs/
├── data_extraction.py
│   ├─ Query users table
│   ├─ Query products table
│   ├─ Query order history
│   └─ Save to Spark DataFrame
│
├── feature_engineering.py
│   ├─ User features: engagement score, purchase count
│   ├─ Product features: price, category, popularity
│   ├─ Normalize features (0-1 scale)
│   └─ Handle missing values
│
└── model_training.py
    ├─ Train collaborative filtering model
    ├─ Train content-based model
    ├─ Train hybrid model
    └─ Save trained models to disk
```

### config/
```
config/
├── spark_config.py
│   ├─ Number of executors (servers)
│   ├─ Memory per executor
│   ├─ Shuffle partitions
│   └─ Optimization settings
│
└── paths.py
    ├─ Data input paths
    ├─ Model output paths
    └─ Log file paths
```

## Training Schedule

### Batch Processing (Nightly Training)

```
10:00 PM - Start training job (after peak usage)
├─ Extract data for last 7 days
├─ Engineer features
├─ Train all models (takes 30 minutes)
└─ Save models to disk

10:30 PM - Job complete
├─ New models ready for inference
├─ Models are loaded by AI service
└─ Next day: users see recommendations

Why at night?
- Database has fewer queries
- Don't compete with user requests
- Takes time, doesn't block users
```

### Model Versioning

```
saved_models/
├── v1.0/
│   ├── collaborative_filtering.pkl
│   ├── content_based.pkl
│   └── hybrid.pkl (trained 2024-01-10)
│
├── v1.1/
│   ├── collaborative_filtering.pkl
│   ├── content_based.pkl
│   └── hybrid.pkl (trained 2024-01-11)
│
└── current → v1.1 (symlink to latest)
```

## AI Service (Inference)

### What is Inference?

Using trained models to make predictions.

Training: "Learn patterns from historical data" (1 hour nightly)
Inference: "Predict for this specific user" (milliseconds)

### Inference Service

```
ai_service/
├── models/
│   ├── collaborative_filtering.py
│   │   ├─ Class: CollaborativeFilteringModel
│   │   ├─ method: recommend(user_id, n=5)
│   │   └─ Returns: [product_id, product_id, ...]
│   │
│   ├── content_based.py
│   │   ├─ Class: ContentBasedModel
│   │   ├─ method: recommend(user_id, n=5)
│   │   └─ Returns: [product_id, product_id, ...]
│   │
│   └── hybrid.py
│       ├─ Class: HybridModel
│       ├─ method: recommend(user_id, n=5)
│       └─ Returns: [product_id, product_id, ...]
│
├── inference/
│   ├── recommender.py
│   │   ├─ Load all models at startup
│   │   ├─ method: get_recommendations(user_id)
│   │   └─ Returns: [product_id, product_id, ...]
│   │
│   └── model_loader.py
│       ├─ Load .pkl files from disk
│       └─ Cache in memory for speed
│
└── data/
    └── data_loader.py
        ├─ Fetch user features from database
        ├─ Fetch product features from database
        └─ Format for model input
```

## Data Flow: End to End

### Step 1: Training (Nightly at 10 PM)
```python
# ml_pipeline/jobs/data_extraction.py
users_df = spark.sql("SELECT * FROM users")
products_df = spark.sql("SELECT * FROM products")
orders_df = spark.sql("SELECT * FROM orders")
```

### Step 2: Feature Engineering
```python
# ml_pipeline/jobs/feature_engineering.py
user_engagement = calculate_engagement(orders_df)
product_popularity = calculate_popularity(orders_df)
normalized_features = normalize(user_engagement, product_popularity)
```

### Step 3: Model Training
```python
# ml_pipeline/jobs/model_training.py
cf_model = train_collaborative_filtering(normalized_features)
cb_model = train_content_based(normalized_features)
hybrid_model = train_hybrid(cf_model, cb_model)

# Save models
save_model(cf_model, "ml_pipeline/saved_models/v1/collaborative_filtering.pkl")
save_model(cb_model, "ml_pipeline/saved_models/v1/content_based.pkl")
```

### Step 4: Backend Requests Recommendations
```python
# backend/app/services/recommendation_service.py
from ai_service.inference.recommender import recommender

def get_recommendations(user_id: int):
    # Call AI service with user_id
    top_5_products = recommender.get_recommendations(user_id, n=5)
    
    # Fetch full product details
    products = session.query(Product).filter(Product.id.in_(top_5_products))
    
    return products  # Return to frontend
```

### Step 5: Frontend Displays
```typescript
// frontend/components/recommendations/RecommendationList.tsx
const Recommendations = () => {
  const { data: recommendations } = useSWR('/api/v1/recommendations')
  
  return (
    <div>
      {recommendations.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  )
}
```

## Technologies Used

```
PySpark:
- Distributed processing
- DataFrame API (SQL on big data)

Scikit-learn:
- Collaborative filtering
- Content-based filtering
- Model serialization

Pandas:
- Data manipulation
- Feature engineering

NumPy:
- Numerical computations
- Matrix operations
```

## Phase 1 Status

Structure explained. Implementation in Phases 6-7.

Next phases:
- Phase 6: Feature engineering with PySpark
- Phase 7: ML model training (5 algorithms)
- Phase 8: Inference service and API
