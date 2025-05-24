from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_tokens(user_id: int):
    access_token = create_token({"sub": str(user_id)}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token({"sub": str(user_id)}, timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES))
    return access_token, refresh_token

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido ou expirado",
        )