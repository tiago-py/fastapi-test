from pydantic import BaseModel, EmailStr, constr

class ClientBase(BaseModel):
    name: str
    email: EmailStr
    cpf: constr(min_length=11, max_length=11)

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    cpf: constr(min_length=11, max_length=11) | None = None

class ClientOut(ClientBase):
    id: int

    class Config:
        orm_mode = True
