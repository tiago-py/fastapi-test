from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.client import Client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Client:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        client_id: str = payload.get("sub")
        if client_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    client = db.query(Client).filter(Client.id == int(client_id)).first()
    if client is None:
        raise credentials_exception
    return client

def require_admin(Client: Client = Depends(get_current_user)) -> Client:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return user
