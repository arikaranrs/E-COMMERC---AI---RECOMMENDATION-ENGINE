from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.models.database import get_db
from app.models.product import Product, Category, Brand
from app.schemas.product import ProductResponse, CategoryResponse, BrandResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/products",
    tags=["Products"],
)

@router.get("", response_model=List[ProductResponse])
def get_products(
    category_id: Optional[int] = None,
    brand_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all products with optional filters and text search.
    """
    try:
        query = db.query(Product)
        
        if category_id is not None:
            query = query.filter(Product.category_id == category_id)
            
        if brand_id is not None:
            query = query.filter(Product.brand_id == brand_id)
            
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (Product.name.like(search_pattern)) | 
                (Product.description.like(search_pattern))
            )
            
        products = query.all()
        return products
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving products"
        )

@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """
    Get all product categories.
    """
    try:
        return db.query(Category).all()
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving categories"
        )

@router.get("/brands", response_model=List[BrandResponse])
def get_brands(db: Session = Depends(get_db)):
    """
    Get all product brands.
    """
    try:
        return db.query(Brand).all()
    except Exception as e:
        logger.error(f"Error fetching brands: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving brands"
        )

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get a single product by ID.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return product
