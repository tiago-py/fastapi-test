from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.future import select
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalars().first()

async def get_products(db: AsyncSession, skip: int = 0, limit: int = 10, 
                      section: str = None, available: bool = None, price: float = None):
    query = select(Product)
    
    if section:
        query = query.where(Product.section.ilike(f"%{section}%"))
    if available:
        query = query.where(Product.stock > 0)
    if price:
        query = query.where(Product.price <= price)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def create_product(db: AsyncSession, product_in: ProductCreate):
    db_product = Product(**product_in.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def update_product(db: AsyncSession, db_product: Product, product_in: ProductUpdate):
    update_data = product_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def delete_product(db: AsyncSession, db_product: Product):
    await db.delete(db_product)
    await db.commit()