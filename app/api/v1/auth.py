from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token
from app.crud.user import create_user, authenticate_user, get_user_by_email
from app.core.security import create_tokens

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email já registrado")
    return create_user(db, user_in)

@router.post("/login", response_model=Token)
def login(user_in: UserCreate, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_in.email, user_in.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access, refresh = create_tokens(user.id)
    return {"access_token": access, "refresh_token": refresh}

@router.post("/refresh-token", response_model=Token)
def refresh_token(
    refresh_token: str = Body(..., embed=True), db: Session = Depends(get_db)
):
    payload = decode_token(refresh_token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    access, _ = create_tokens(user.id)
    return {"access_token": access, "refresh_token": refresh_token}