from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_db, get_current_user

from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.crud import product as crud_product

router = APIRouter()

@router.get("/", response_model=List[ProductOut])
def list_products(
    skip: int = 0,
    limit: int = 10,
    section: Optional[str] = Query(None),
    price: Optional[float] = Query(None),
    available: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user)
):
    return crud_product.get_products(db, skip=skip, limit=limit, section=section, available=available, price=price)

@router.post("/", response_model=ProductOut)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    return crud_product.create_product(db, product_in)

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    product = crud_product.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product_in: ProductUpdate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    db_product = crud_product.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return crud_product.update_product(db, db_product, product_in)

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    db_product = crud_product.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    crud_product.delete_product(db, db_product)
    return {"ok": True}
