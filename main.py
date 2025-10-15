from contextlib import asynccontextmanager
from Controllers.UserController import create_user_account
import jwt
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from Controllers.BanckAccountController import (
    create_bank_account,
    get_bank_account,
    close_account,
)
from Controllers.depositMoneyControlleur import depositMoney
from Controllers.TransactionController import (
    cancel_transaction,
    show_transaction,
    show_all_transactions,
)
from models.model import BankAccount, Transactions, User
from Controllers.Account_LoginController import login
from sqlmodel import Session
from database import create_db_and_tables, get_session, engine

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


class LoginBody(BaseModel):
    email: str
    password: str


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


@app.post("/showTransaction")
def show_details_transaction(request: CancelTransactionRequest):
    return show_transaction(
        request.id_compteA, request.id_compteB, request.id_transaction
    )


@app.get("/showAllTransactions/{compte_id}")
def show_all_transactions_endpoint(compte_id: int):
    return show_all_transactions(compte_id)


# app.include_router(users_router)


@app.post("/login")
def login_root(request: LoginBody):
    print(request)
    return login(request.email, request.password)


@app.post("/bank/account/close/{banckAccount_id}")
def close_account_root(banckAccount_id: int):
    return close_account(banckAccount_id)
