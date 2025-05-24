from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.schemas.client import ClientCreate, ClientUpdate, ClientOut
from app.crud import client as crud_client
from app.api.deps import get_db, get_current_user

router = APIRouter()

@router.get("/", response_model=List[ClientOut])
def list_clients(
    skip: int = 0,
    limit: int = 10,
    name: str = Query(None),
    email: str = Query(None),
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user)
):
    return crud_client.get_clients(db, skip=skip, limit=limit, name=name, email=email)

@router.post("/", response_model=ClientOut)
def create_new_client(
    client_in: ClientCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user)
):
    try:
        return crud_client.create_client(db, client_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{client_id}", response_model=ClientOut)
def get_client_by_id(client_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    db_client = crud_client.get_client(db, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_client

@router.put("/{client_id}", response_model=ClientOut)
def update_client_by_id(client_id: int, client_in: ClientUpdate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    db_client = crud_client.get_client(db, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return crud_client.update_client(db, db_client, client_in)

@router.delete("/{client_id}")
def delete_client_by_id(client_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    db_client = crud_client.get_client(db, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    crud_client.delete_client(db, db_client)
    return {"ok": True}
