"""
Order and shopping-related models.

Includes orders, order items, cart, wishlist, and recommendation cache.
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON, DECIMAL, Enum, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.models.database import Base


class OrderStatus(str, PyEnum):
    """Order status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    """
    Purchase orders.
    
    Represents a completed checkout with one or more items.
    Used for:
    - Purchase history (collaborative filtering signal)
    - Revenue tracking
    - Order fulfillment
    - Customer support
    
    Attributes:
        id: Order ID
        user_id: Customer
        total_amount: Total order value
        status: Order processing status
        shipping_address: Shipping address JSON
        billing_address: Billing address JSON
        payment_method: Payment method used
        created_at: Order placement time
        updated_at: Last status update
    """
    
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(20), default=OrderStatus.PENDING.value, index=True)
    shipping_address = Column(Text, nullable=False)
    billing_address = Column(Text, nullable=False)
    payment_method = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, total={self.total_amount})>"
    
    def is_completed(self) -> bool:
        """Check if order is delivered."""
        return self.status == OrderStatus.DELIVERED.value
    
    def get_items_count(self) -> int:
        """Get total items in order."""
        return sum(item.quantity for item in self.items)


class OrderItem(Base):
    """
    Individual line items in an order.
    
    Captures what was purchased at what price/quantity.
    Separated from product to preserve historical pricing.
    
    Attributes:
        id: Item ID
        order_id: Parent order
        product_id: What was purchased
        quantity: How many
        price_per_unit: Price at time of purchase (snapshot)
        subtotal: quantity * price_per_unit
    """
    
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(DECIMAL(10, 2), nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product")
    
    def __repr__(self):
        return f"<OrderItem(order_id={self.order_id}, product_id={self.product_id}, qty={self.quantity})>"


class Cart(Base):
    """
    Shopping cart (one per user, one-to-one).
    
    Attributes:
        id: Cart ID
        user_id: Owner (unique)
        created_at: Cart creation
        updated_at: Last modification
    """
    
    __tablename__ = "cart"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Cart(user_id={self.user_id}, items={len(self.items)})>"
    
    def get_total(self) -> float:
        """Calculate cart total."""
        return sum(float(item.product.get_final_price()) * item.quantity for item in self.items)
    
    def get_items_count(self) -> int:
        """Get total items in cart."""
        return sum(item.quantity for item in self.items)


class CartItem(Base):
    """
    Items in shopping cart.
    
    Attributes:
        id: Item ID
        cart_id: Parent cart
        product_id: Product in cart
        quantity: Item quantity
        added_at: When added to cart
    """
    
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("cart.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    added_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint("cart_id", "product_id", name="uq_cart_product"),
    )
    
    # Relationships
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")
    
    def __repr__(self):
        return f"<CartItem(cart_id={self.cart_id}, product_id={self.product_id}, qty={self.quantity})>"


class Wishlist(Base):
    """
    User's wishlist (bookmarks for later purchase).
    
    Used for:
    - Content-based recommendation signals
    - Purchase intent
    - Personalization
    
    Attributes:
        id: Wishlist item ID
        user_id: Owner
        product_id: Wishlist item
        added_at: When added
    """
    
    __tablename__ = "wishlist"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_user_product_wishlist"),
    )
    
    def __repr__(self):
        return f"<Wishlist(user_id={self.user_id}, product_id={self.product_id})>"


class RecommendationType(str, PyEnum):
    """Types of recommendations."""
    PERSONALIZED = "personalized"
    COLLABORATIVE = "collaborative"
    CONTENT_BASED = "content_based"
    HYBRID = "hybrid"
    TRENDING = "trending"


class RecommendationCache(Base):
    """
    Pre-computed recommendation cache for performance.
    
    Instead of generating recommendations on every request,
    pre-compute daily/weekly and cache results. Reduces:
    - Latency (no model inference needed)
    - Computational load
    - Database load
    
    Attributes:
        id: Cache ID
        user_id: Target user
        product_ids: Array of recommended product IDs (JSON)
        recommendation_type: Which algorithm generated
        generated_at: When recommendations were generated
        expires_at: Cache expiration time
    """
    
    __tablename__ = "recommendation_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_ids = Column(JSON, nullable=False)  # List of product IDs
    recommendation_type = Column(String(50), nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, index=True)
    
    __table_args__ = (
        UniqueConstraint("user_id", "recommendation_type", name="uq_user_rec_type"),
        Index("idx_expires_at", "expires_at"),
    )
    
    def __repr__(self):
        return f"<RecommendationCache(user_id={self.user_id}, type={self.recommendation_type})>"
    
    def is_expired(self) -> bool:
        """Check if cache entry has expired."""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
