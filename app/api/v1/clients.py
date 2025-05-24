from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.api.deps import get_db, get_current_user
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.crud import product as crud_product

router = APIRouter()

@router.get("/", response_model=List[ProductOut])
async def list_products(
    skip: int = 0,
    limit: int = 10,
    section: Optional[str] = Query(None),
    price: Optional[float] = Query(None),
    available: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db),
    _: str = Depends(get_current_user)
):
    return await crud_product.get_products(db, skip=skip, limit=limit, section=section, available=available, price=price)

@router.post("/", response_model=ProductOut)
async def create_product(
    product_in: ProductCreate, 
    db: AsyncSession = Depends(get_db), 
    _: str = Depends(get_current_user)
):
    return await crud_product.create_product(db, product_in)

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(
    product_id: int, 
    db: AsyncSession = Depends(get_db), 
    _: str = Depends(get_current_user)
):
    product = await crud_product.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int, 
    product_in: ProductUpdate, 
    db: AsyncSession = Depends(get_db), 
    _: str = Depends(get_current_user)
):
    db_product = await crud_product.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return await crud_product.update_product(db, db_product, product_in)

@router.delete("/{product_id}")
async def delete_product(
    product_id: int, 
    db: AsyncSession = Depends(get_db), 
    _: str = Depends(get_current_user)
):
    db_product = await crud_product.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    await crud_product.delete_product(db, db_product)
    return {"ok": True}