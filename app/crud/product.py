from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip=0, limit=10, section=None, available=None, price=None):
    query = db.query(Product)
    if section:
        query = query.filter(Product.section.ilike(f"%{section}%"))
    if available:
        query = query.filter(Product.stock > 0)
    if price:
        query = query.filter(Product.price <= price)
    return query.offset(skip).limit(limit).all()

def create_product(db: Session, product_in: ProductCreate):
    db_product = Product(**product_in.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, db_product: Product, product_in: ProductUpdate):
    update_data = product_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, db_product: Product):
    db.delete(db_product)
    db.commit()
