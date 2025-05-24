from sqlalchemy.orm import Session
from app.models.client import Client 
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(Client).filter(Client.email == email).first()

def create_user(db: Session, user_in: UserCreate):
    db_user = Client(
        email=user_in.email,
        hashed_password=hash_password(user_in.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
