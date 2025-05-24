from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserOut  # Assuming you'll rename these to Client...
from app.schemas.token import Token
from app.crud.user import create_user, authenticate_user, get_user_by_email  # These should be updated too
from app.core.security import create_tokens, decode_token
from app.models.client import Client  # Changed from User to Client

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    if await get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado"
        )
    return await create_user(db, user_in)

@router.post("/login", response_model=Token)
async def login(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    client = await authenticate_user(db, user_in.email, user_in.password)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    access, refresh = create_tokens(client.id)
    return {"access_token": access, "refresh_token": refresh}

@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    refresh_token: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    payload = decode_token(refresh_token)
    client_id = payload.get("sub")
    if client_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    result = await db.execute(select(Client).where(Client.id == int(client_id)))
    client = result.scalars().first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    
    access, _ = create_tokens(client.id)
    return {"access_token": access, "refresh_token": refresh_token}