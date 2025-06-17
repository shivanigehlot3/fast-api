from pydantic import BaseModel

class CartAdd(BaseModel):
    product_id: int
    quantity: int

class CartUpdate(BaseModel):
    quantity: int

class CartItemOut(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True