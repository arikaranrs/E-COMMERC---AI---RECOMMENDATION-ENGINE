from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.models.database import get_db
from app.models.product import Product
from app.models.order import RecommendationCache
from app.schemas.product import ProductResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations"],
)

@router.get("", response_model=List[ProductResponse])
def get_recommendations(
    user_id: Optional[int] = None,
    type: str = "personalized",
    db: Session = Depends(get_db)
):
    """
    Get recommended products for a user based on selected algorithm type.
    
    Supported types:
    - personalized: Default user-specific recommendations
    - collaborative: Collaborative filtering
    - content_based: Content-based (item-item text similarity)
    - hybrid: Combined collaborative & content-based
    - trending: Globally popular products
    """
    try:
        # If user_id is not specified, we default to the admin/default user (user_id=4)
        # to ensure guests also get a full set of recommendations.
        effective_user_id = user_id if user_id is not None else 4
        
        # Query Recommendation Cache
        cache_entry = db.query(RecommendationCache).filter(
            RecommendationCache.user_id == effective_user_id,
            RecommendationCache.recommendation_type == type
        ).first()
        
        product_ids = []
        if cache_entry and cache_entry.product_ids:
            product_ids = cache_entry.product_ids
        
        # Fallback if no cache entry is found
        if not product_ids:
            logger.warning(f"No recommendation cache found for user {effective_user_id} and type {type}. Using fallback.")
            # Let's fetch the first 4 products as fallback
            fallback_products = db.query(Product).limit(4).all()
            return fallback_products
            
        # Fetch products from database
        products = db.query(Product).filter(Product.id.in_(product_ids)).all()
        
        # Sort products to match the exact order of product_ids inside cache
        products_map = {p.id: p for p in products}
        ordered_products = [products_map[pid] for pid in product_ids if pid in products_map]
        
        return ordered_products
        
    except Exception as e:
        logger.error(f"Error fetching recommendations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving recommendations"
        )
