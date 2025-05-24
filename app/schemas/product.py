from pydantic import BaseModel
from datetime import date
from typing import Optional

class ProductBase(BaseModel):
    description: str
    price: float
    barcode: str
    section: str
    stock: int
    expiration_date: Optional[date] = None
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    description: Optional[str]
    price: Optional[float]
    barcode: Optional[str]
    section: Optional[str]
    stock: Optional[int]
    expiration_date: Optional[date]
    image_url: Optional[str]

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
