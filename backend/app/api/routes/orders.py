from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
from datetime import datetime

from app.models.database import get_db
from app.models.order import Order, OrderItem, Cart, CartItem
from app.models.product import Product, UserActivity
from app.schemas.order import OrderResponse, CheckoutRequest

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"],
)

@router.get("", response_model=List[OrderResponse])
def get_orders(user_id: int, db: Session = Depends(get_db)):
    """
    Get order history for a user.
    """
    try:
        orders = db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()
        return orders
    except Exception as e:
        logger.error(f"Error fetching orders: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving order history"
        )

@router.post("", response_model=OrderResponse)
def checkout(checkout_data: CheckoutRequest, user_id: int, db: Session = Depends(get_db)):
    """
    Create a new order from the current shopping cart.
    """
    try:
        # Fetch cart
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart or not cart.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Shopping cart is empty"
            )
            
        total_amount = cart.get_total()
        
        # Create order
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            status="confirmed",
            shipping_address=checkout_data.shipping_address,
            billing_address=checkout_data.billing_address,
            payment_method=checkout_data.payment_method
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        
        # Create order items, update stock, and log user activity
        for item in cart.items:
            # Check stock
            if item.product.stock_quantity < item.quantity:
                # If insufficient stock, we proceed with whatever we have (simulated store)
                item.product.stock_quantity = 0
            else:
                item.product.stock_quantity -= item.quantity
                
            price = item.product.get_final_price()
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_per_unit=price,
                subtotal=price * item.quantity
            )
            db.add(order_item)
            
            # Log purchase activity for recommendations system
            activity = UserActivity(
                user_id=user_id,
                product_id=item.product_id,
                activity_type="purchase",
                timestamp=datetime.utcnow()
            )
            db.add(activity)
            
        # Empty cart
        for item in cart.items:
            db.delete(item)
            
        db.commit()
        db.refresh(order)
        
        return order
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking out cart: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing checkout"
        )
