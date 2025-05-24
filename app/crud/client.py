from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select
from sqlalchemy.future import select
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate

async def get_client(db: AsyncSession, client_id: int):
    result = await db.execute(select(Client).where(Client.id == client_id))
    return result.scalars().first()

async def get_clients(db: AsyncSession, skip: int = 0, limit: int = 10, name: str = None, email: str = None):
    query = select(Client)
    if name:
        query = query.where(Client.name.ilike(f"%{name}%"))
    if email:
        query = query.where(Client.email.ilike(f"%{email}%"))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def create_client(db: AsyncSession, client_in: ClientCreate):
    # Check for existing email or CPF
    existing = await db.execute(
        select(Client).where(
            or_(Client.email == client_in.email, 
                Client.cpf == client_in.cpf)
        )
    )
    if existing.scalars().first():
        raise ValueError("Email ou CPF já cadastrados")
    
    db_client = Client(**client_in.dict())
    db.add(db_client)
    await db.commit()
    await db.refresh(db_client)
    return db_client

async def update_client(db: AsyncSession, db_client: Client, client_in: ClientUpdate):
    update_data = client_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_client, field, value)
    await db.commit()
    await db.refresh(db_client)
    return db_client

async def delete_client(db: AsyncSession, db_client: Client):
    await db.delete(db_client)
    await db.commit()