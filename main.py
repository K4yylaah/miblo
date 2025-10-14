from contextlib import asynccontextmanager
from typing import Optional
from models.model import User
from UserController import create_user_account
from fastapi import FastAPI
from pydantic import BaseModel
from Controllers.BanckAccountController import create_bank_account
from Controllers.BanckAccountController import get_bank_account
from database import create_db_and_tables
from Controllers.depositMoneyControlleur import depositMoney
from models.model import BankAccount


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"test"}


@app.post("/create/bank/account")
def accountBank_root(request: BankAccount):
    return create_bank_account(request.id, request.user_id, request.solde, request.rib)


@app.get("/bank/account/{user_id}")
def bank_account_root(user_id: int):
    return get_bank_account(user_id)


class DepositRequest(BaseModel):
    compteId: int
    amout: float


@app.post("/depositMoney")
def make_deposit(request: DepositRequest):
    return depositMoney(request.compteId, request.amout)

class CreateUserBody(BaseModel):
    name: str
    email: str
    password: str

@app.post("/register/")
def create_account(user: CreateUserBody):
    return create_user_account (user.name, user.password, user.email)

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
