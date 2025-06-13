from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.products import models, schemas
from app.utils.deps import get_db, get_current_user, admin_required

router = APIRouter()

# ---------- ADMIN CRUD ----------

@router.post("/admin/products", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), _ = Depends(admin_required)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/admin/products", response_model=List[schemas.ProductOut])
def list_products_admin(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _ = Depends(admin_required)):
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products

@router.get("/admin/products/{id}", response_model=schemas.ProductOut)
def get_product_admin(id: int, db: Session = Depends(get_db), _ = Depends(admin_required)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/admin/products/{id}", response_model=schemas.ProductOut)
def update_product(id: int, updates: schemas.ProductUpdate, db: Session = Depends(get_db), _ = Depends(admin_required)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for field, value in updates.dict(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product

@router.delete("/admin/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db), _ = Depends(admin_required)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

# ---------- PUBLIC PRODUCT APIs ----------

@router.get("/", response_model=List[schemas.ProductOut])
def list_products_public(
    category: str = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    sort_by: str = Query(None),
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)

    if category:
        query = query.filter(models.Product.category == category)
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)

    if sort_by == "price_asc":
        query = query.order_by(models.Product.price.asc())
    elif sort_by == "price_desc":
        query = query.order_by(models.Product.price.desc())

    products = query.offset((page - 1) * page_size).limit(page_size).all()
    return products

@router.get("/search", response_model=List[schemas.ProductOut])
def search_products(keyword: str, db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.name.ilike(f"%{keyword}%")).all()
    return products

@router.get("/{id}", response_model=schemas.ProductOut)
def get_product_public(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
