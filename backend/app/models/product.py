"""
Product-related models for e-commerce catalog.

Includes products, categories, brands, ratings, reviews,
and user activity tracking.
"""

from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Enum, DECIMAL, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.models.database import Base


class Category(Base):
    """
    Product categories for organizing catalog.
    
    Attributes:
        id: Category ID
        name: Category name (unique)
        description: Category description
        icon_url: URL to category icon
        created_at: Creation timestamp
    """
    
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    icon_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"


class Brand(Base):
    """
    Product brands.
    
    Attributes:
        id: Brand ID
        name: Brand name (unique)
        logo_url: URL to brand logo
        description: Brand description
        created_at: Creation timestamp
    """
    
    __tablename__ = "brands"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    logo_url = Column(String(500))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    products = relationship("Product", back_populates="brand", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Brand(id={self.id}, name={self.name})>"


class Product(Base):
    """
    Core product catalog with pricing, inventory, and ratings.
    
    Why TF-IDF content-based recommendations work with this:
    - name + description provide text for TF-IDF vectorization
    - category_id + brand_id for feature-based similarity
    - price for price-range filtering
    
    Why collaborative filtering works:
    - Tracks user interactions through ratings/reviews
    - Multiple users rating same products create the user-item matrix
    
    Attributes:
        id: Product ID
        name: Product name (searchable)
        description: Product description (searchable, used for embeddings)
        price: Current selling price
        discount_price: Discounted price (nullable)
        category_id: Foreign key to category
        brand_id: Foreign key to brand
        stock_quantity: Items in stock
        image_url: Product image
        rating: Average rating (calculated from ratings table)
        review_count: Number of reviews
        sku: Stock keeping unit (unique)
        created_at: When product was added
        updated_at: Last modification
    """
    
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False, index=True)
    discount_price = Column(DECIMAL(10, 2))
    
    # Foreign Keys
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), index=True)
    
    # Inventory & Metadata
    stock_quantity = Column(Integer, default=0)
    image_url = Column(String(500))
    sku = Column(String(100), unique=True, index=True)
    
    # Aggregated Ratings (denormalized for performance)
    rating = Column(Float, default=0.0, index=True)
    review_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    ratings = relationship("Rating", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"
    
    def is_in_stock(self) -> bool:
        """Check if product is in stock."""
        return self.stock_quantity > 0
    
    def get_final_price(self) -> float:
        """Get final price after discount."""
        return float(self.discount_price) if self.discount_price else float(self.price)


class Rating(Base):
    """
    Product ratings (1-5 stars).
    
    Critical for collaborative filtering:
    - Creates user-item matrix for CF algorithms
    - Multiple users rating same products enables similarity computation
    - Ratings are numerical, enabling distance/similarity calculations
    
    Attributes:
        id: Rating ID
        user_id: User who gave rating
        product_id: Product being rated
        rating: Rating value (1-5)
        created_at: When rating was given
        updated_at: When rating was last updated
    """
    
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)  # 1-5 stars (validation in service layer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_user_product_rating"),
    )
    
    # Relationships
    user = relationship("User", back_populates="ratings")
    product = relationship("Product", back_populates="ratings")
    
    def __repr__(self):
        return f"<Rating(user_id={self.user_id}, product_id={self.product_id}, rating={self.rating})>"


class Review(Base):
    """
    Product reviews (text reviews with ratings).
    
    Used for:
    - Content-based recommendations (review text → TF-IDF)
    - User feedback and product information
    - Social proof and trust building
    
    Attributes:
        id: Review ID
        user_id: Author
        product_id: Reviewed product
        title: Review title
        content: Review content (used for TF-IDF)
        helpful_count: Helpful votes
        unhelpful_count: Unhelpful votes
        created_at: When review was written
        updated_at: When review was last edited
    """
    
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    helpful_count = Column(Integer, default=0)
    unhelpful_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")
    
    def __repr__(self):
        return f"<Review(id={self.id}, user_id={self.user_id}, product_id={self.product_id})>"


class ActivityType(str, PyEnum):
    """User activity types for tracking."""
    VIEW = "view"
    CLICK = "click"
    ADD_TO_CART = "add_to_cart"
    REMOVE_FROM_CART = "remove_from_cart"
    PURCHASE = "purchase"
    WISHLIST_ADD = "wishlist_add"
    WISHLIST_REMOVE = "wishlist_remove"
    REVIEW = "review"
    RATING = "rating"


class UserActivity(Base):
    """
    User activity log for behavior tracking and ML features.
    
    Critical for ML training:
    - Purchase history (implicit feedback for CF)
    - Browse history (content-based features)
    - Click patterns (engagement signals)
    - Wishlist (purchase intent signals)
    
    This table grows large → partition by date in production,
    aggregate for training data periodically.
    
    Attributes:
        id: Activity ID
        user_id: User performing activity
        product_id: Target product
        activity_type: Type of activity (view, click, purchase, etc.)
        timestamp: When activity occurred
    """
    
    __tablename__ = "user_activity"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    activity_type = Column(String(50), nullable=False, index=True)  # Enum string
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        Index("idx_user_timestamp", "user_id", "timestamp"),
        Index("idx_product_timestamp", "product_id", "timestamp"),
    )
    
    # Relationships
    user = relationship("User", back_populates="activity")
    
    def __repr__(self):
        return f"<UserActivity(user_id={self.user_id}, activity_type={self.activity_type})>"
