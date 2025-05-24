from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate

def get_client(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()

def get_clients(db: Session, skip: int = 0, limit: int = 10, name: str = None, email: str = None):
    query = db.query(Client)
    if name:
        query = query.filter(Client.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Client.email.ilike(f"%{email}%"))
    return query.offset(skip).limit(limit).all()

def create_client(db: Session, client_in: ClientCreate):
    if db.query(Client).filter(or_(Client.email == client_in.email, Client.cpf == client_in.cpf)).first():
        raise ValueError("Email ou CPF já cadastrados")
    db_client = Client(**client_in.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def update_client(db: Session, db_client: Client, client_in: ClientUpdate):
    update_data = client_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_client, field, value)
    db.commit()
    db.refresh(db_client)
    return db_client

def delete_client(db: Session, db_client: Client):
    db.delete(db_client)
    db.commit()
