from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    barcode = Column(String, unique=True, index=True)
    section = Column(String, nullable=False)
    stock = Column(Integer, default=0)
    expiration_date = Column(Date, nullable=True)
    image_url = Column(Text, nullable=True)
