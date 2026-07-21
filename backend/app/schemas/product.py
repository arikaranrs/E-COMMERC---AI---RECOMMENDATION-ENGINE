from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    icon_url: Optional[str] = None

    class Config:
        from_attributes = True

class BrandResponse(BaseModel):
    id: int
    name: str
    logo_url: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    discount_price: Optional[float] = None
    category_id: int
    brand_id: Optional[int] = None
    stock_quantity: int
    image_url: Optional[str] = None
    sku: Optional[str] = None
    rating: float
    review_count: int
    created_at: datetime
    category: Optional[CategoryResponse] = None
    brand: Optional[BrandResponse] = None

    class Config:
        from_attributes = True
