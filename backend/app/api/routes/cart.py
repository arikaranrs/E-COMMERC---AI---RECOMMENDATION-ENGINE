from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.models.database import get_db
from app.models.order import Cart, CartItem
from app.models.product import Product
from app.schemas.order import CartResponse, CartItemAddRequest, CartItemUpdateRequest

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/cart",
    tags=["Cart"],
)

def get_or_create_cart(db: Session, user_id: int) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

@router.get("", response_model=CartResponse)
def get_cart(user_id: int, db: Session = Depends(get_db)):
    """
    Get user's shopping cart. Creates one if it doesn't exist.
    """
    try:
        cart = get_or_create_cart(db, user_id)
        
        # Calculate total and count manually to ensure they are float/int
        total = cart.get_total()
        items_count = cart.get_items_count()
        
        return {
            "id": cart.id,
            "user_id": cart.user_id,
            "items": cart.items,
            "total": total,
            "items_count": items_count
        }
    except Exception as e:
        logger.error(f"Error fetching cart: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving cart"
        )

@router.post("", response_model=CartResponse)
def add_to_cart(item_data: CartItemAddRequest, user_id: int, db: Session = Depends(get_db)):
    """
    Add a product to the user's cart or increment its quantity if it already exists.
    """
    try:
        # Check if product exists
        product = db.query(Product).filter(Product.id == item_data.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item_data.product_id} not found"
            )
            
        cart = get_or_create_cart(db, user_id)
        
        # Check if item is already in cart
        cart_item = db.query(CartItem).filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == item_data.product_id
        ).first()
        
        if cart_item:
            cart_item.quantity += item_data.quantity
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity
            )
            db.add(cart_item)
            
        db.commit()
        db.refresh(cart)
        
        return {
            "id": cart.id,
            "user_id": cart.user_id,
            "items": cart.items,
            "total": cart.get_total(),
            "items_count": cart.get_items_count()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding to cart: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error adding item to cart"
        )

@router.put("/{item_id}", response_model=CartResponse)
def update_cart_item(item_id: int, update_data: CartItemUpdateRequest, user_id: int, db: Session = Depends(get_db)):
    """
    Update the quantity of an item in the cart. If quantity is 0 or less, the item is removed.
    """
    try:
        cart = get_or_create_cart(db, user_id)
        cart_item = db.query(CartItem).filter(
            CartItem.id == item_id,
            CartItem.cart_id == cart.id
        ).first()
        
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )
            
        if update_data.quantity <= 0:
            db.delete(cart_item)
        else:
            cart_item.quantity = update_data.quantity
            
        db.commit()
        db.refresh(cart)
        
        return {
            "id": cart.id,
            "user_id": cart.user_id,
            "items": cart.items,
            "total": cart.get_total(),
            "items_count": cart.get_items_count()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating cart item: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating cart item"
        )

@router.delete("/{item_id}", response_model=CartResponse)
def remove_from_cart(item_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Remove an item from the cart.
    """
    try:
        cart = get_or_create_cart(db, user_id)
        cart_item = db.query(CartItem).filter(
            CartItem.id == item_id,
            CartItem.cart_id == cart.id
        ).first()
        
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )
            
        db.delete(cart_item)
        db.commit()
        db.refresh(cart)
        
        return {
            "id": cart.id,
            "user_id": cart.user_id,
            "items": cart.items,
            "total": cart.get_total(),
            "items_count": cart.get_items_count()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing from cart: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error removing item from cart"
        )
