from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from app.core.database import Base
from datetime import datetime, timezone

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="paid")  # paid, cancelled
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False)
