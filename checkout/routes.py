from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.deps import get_db, get_current_user
from app.auth.models import User
from app.cart.models import Cart
from app.products.models import Product
from app.orders.models import Order, OrderItem

router = APIRouter()

@router.post("/")
def checkout(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = 0
    order_items = []

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if item.quantity > product.stock:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")

        subtotal = item.quantity * product.price
        total_amount += subtotal

        order_items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price_at_purchase": product.price
        })

        product.stock -= item.quantity

    new_order = Order(   #create order
        user_id=current_user.id,
        total_amount=total_amount
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for oi in order_items:  # add order items
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=oi["product_id"],
            quantity=oi["quantity"],
            price_at_purchase=oi["price_at_purchase"]
        )
        db.add(order_item)

    db.query(Cart).filter(Cart.user_id == current_user.id).delete() #cart clear

    db.commit()
    return {"message": "Order placed successfully", "order_id": new_order.id}
