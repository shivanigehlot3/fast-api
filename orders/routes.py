from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.utils.deps import get_db, get_current_user
from app.auth.models import User
from app.orders import models, schemas
from app.orders.models import Order, OrderItem

router = APIRouter()

@router.get("/", response_model=List[schemas.OrderOut])
def view_order_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()
    return orders

@router.get("/{order_id}", response_model=schemas.OrderDetailOut)
def view_order_details(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

    order_items_out = [
        schemas.OrderItemOut(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=item.price_at_purchase
        )
        for item in order_items
    ]

    return schemas.OrderDetailOut(
        id=order.id,
        total_amount=order.total_amount,
        status=order.status,
        created_at=order.created_at,
        items=order_items_out
    )
