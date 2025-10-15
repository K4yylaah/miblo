from typing import Optional

from contextlib import asynccontextmanager

import jwt
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, select

from database import create_db_and_tables, get_session
from models.model import User

# from routes.users import router as users_router, LoginData


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
        return {"message": "Bienvenue sur FastAPI!"}




# app.include_router(users_router)

class LoginBody (BaseModel):
    email: str
    password: str

@app.post("/login")
def login(body : LoginBody, session = Depends(get_session)):
    user = session.exec(select(User).where(User.email==body.email)).first()
    if not user or user.password != body.password:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    return {"message": f"Bienvenue {user.email} !"}

secret_key = "1234567890123456789"
algorithm = "HS256"

def generate_token(user: User):
     return jwt.encode(user.dict(), secret_key, algorithm=algorithm)


""""class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    solde: int

class Transactions(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_compteA: int
    id_compteB: int

"""""

""""compte1 = User(id=1, solde=100)
compte2 = User(id=2, solde=100)




def echange(compteA, compteB, var):
    transaction = Transactions(id =1, id_compteA=compteA.id, id_compteB=compteB.id)
    print(compteA.id, compteB.id)
    compteB.solde = compteB.solde + var
    compteA.solde= compteA.solde - var
    return transaction

print(echange(compte1, compte2, 50))
print(compte1.solde)
print(compte2.solde)"""""