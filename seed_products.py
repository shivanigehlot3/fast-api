from app.core.database import SessionLocal
from app.products.models import Product

db = SessionLocal()

sample_products = [
    {
        "name": "iPhone 15",
        "description": "Latest Apple iPhone",
        "price": 999.99,
        "stock": 50,
        "category": "Electronics",
        "image_url": "https://example.com/iphone.jpg"
    },
    {
        "name": "Samsung Galaxy S23",
        "description": "Latest Samsung phone",
        "price": 899.99,
        "stock": 60,
        "category": "Electronics",
        "image_url": "https://example.com/galaxy.jpg"
    },
    {
        "name": "MacBook Pro",
        "description": "Apple laptop",
        "price": 1999.99,
        "stock": 30,
        "category": "Laptops",
        "image_url": "https://example.com/macbook.jpg"
    }
]

for data in sample_products:
    product = Product(**data)
    db.add(product)

db.commit()
db.close()

print("Seed data added successfully")

