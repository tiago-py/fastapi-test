from sqlalchemy import Column, Integer, String, UniqueConstraint, Boolean
from app.db.base import Base


class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Make sure this matches your DB constraint
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    cpf = Column(Integer)  # Make nullable if not required
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)