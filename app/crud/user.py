from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.client import Client 
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(Client).where(Client.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user_in: UserCreate):
    db_user = Client(
        name=user_in.name,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        cpf=user_in.cpf
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user