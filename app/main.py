from fastapi import FastAPI
from app.api.v1 import auth
from app.api.v1 import clients
from app.api.v1 import products


app = FastAPI(title="API Lu Estilo")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(clients.router, prefix="/clients", tags=["Clientes"])
app.include_router(products.router, prefix="/products", tags=["Produtos"])