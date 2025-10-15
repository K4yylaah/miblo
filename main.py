from contextlib import asynccontextmanager
from typing import Optional
from models.model import User
from UserController import create_user_account
from fastapi import FastAPI

import jwt
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from Controllers.BanckAccountController import create_bank_account
from Controllers.BanckAccountController import get_bank_account
from database import create_db_and_tables
from Controllers.depositMoneyControlleur import depositMoney
from models.model import BankAccount, Transactions
from Controllers.cancelTransactionController import cancel_transaction
from database import engine
from sqlmodel import Session
from models.model import BankAccount
from sqlmodel import SQLModel, Field, select

from database import create_db_and_tables, get_session
from models.model import User

# from routes.users import router as users_router, LoginData


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


class DepositRequest(BaseModel):
    compteId: int
    amout: float


class CreateUserBody(BaseModel):
    name: str
    email: str
    password: str

class TransactionRequest(BaseModel):
    id_compteA: int
    id_compteB: int
    amout: float


class CreateAccountRequest(BaseModel):
    user_id: int
    solde: float
    rib: str

class CancelTransactionRequest(BaseModel):
    id_compteA: int
    id_compteB: int
    id_transaction: int
app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"test"}

@app.post("/create/bank/account")
def accountBank_root(request: BankAccount):
    return create_bank_account(
        request.id, request.user_id, request.solde, request.rib, request.is_primary
    )

@app.get("/bank/account/{user_id}")
def bank_account_root(user_id: int):
    return get_bank_account(user_id)

@app.post("/depositMoney")
def make_deposit(request: DepositRequest):
    return depositMoney(request.compteId, request.amout)

@app.post("/register")
def create_account(user: CreateUserBody):
    return create_user_account(user.name, user.password, user.email)



@app.post("/createTransaction")
def create_transaction(request: TransactionRequest):
    with Session(engine) as session:
        transaction = Transactions(
            id_compteA=request.id_compteA,
            id_compteB=request.id_compteB,
            amout=request.amout,
        )
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return {"message": "Transaction créée avec succès.", "transaction": transaction}

@app.post("/cancelTransaction")
def cancel_transaction_endpoint(request: CancelTransactionRequest):
    return cancel_transaction(
        request.id_compteA, request.id_compteB, request.id_transaction
    )




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

""" ""

""""compte = User(id=1, solde=100)
compte2 = User(id=2, solde=100)




def echange(compteA, compteB, var):
    transaction = Transactions(id =1, id_compteA=compteA.id, id_compteB=compteB.id)
    print(compteA.id, compteB.id)
    compteB.solde = compteB.solde + var
    compteA.solde= compteA.solde - var
    return transaction

print(echange(compte1, compte2, 50))
print(compte1.solde)
print(compte2.solde)""" ""
