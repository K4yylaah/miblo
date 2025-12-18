from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
from contextlib import asynccontextmanager
from Controllers.UserController import create_user_account
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from Controllers.BanckAccountController import (
    create_bank_account,
    get_bank_account,
    close_account, get_bank_account_by_rib,
)
from Controllers.depositMoneyControlleur import deposit_money, get_deposit_by_id, get_account_deposits
from Controllers.Account_Login_Controller import get_user
from Controllers.User_Recovery_Controller import get_user_by_id
from Controllers.recipientController import find_recipient_rib, make_recipient, show_recipients
from Controllers.TransactionController import cancel_transaction, show_transaction, get_all_transactions, send_money
from Controllers.Account_Login_Controller import login
from database import create_db_and_tables, engine


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

class SendMoneyRequest(BaseModel):
    id_compteA: int
    id_compteB: int
    amout: float

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/create/bank/account/{user_id}")
def accountBank_root(user_id: int):
    return create_bank_account(user_id)

@app.get("/bank/account/{user_id}")
def bank_account_root(user_id: int):
    return get_bank_account(user_id)

@app.get("/bank/account-by-rib/{rib}")
def bank_account_get_by_rib(rib: str):
    return get_bank_account_by_rib(rib)

@app.post("/depositMoney")
def make_deposit(request: DepositRequest):
    return deposit_money(request.compteId, request.amout, engine)

@app.post("/register")
def create_account(user: CreateUserBody):
    return create_user_account(user.name, user.password, user.email)



@app.post("/cancelTransaction")
def cancel_transaction_endpoint(request: CancelTransactionRequest):
    return cancel_transaction(
        request.id_compteA, request.id_compteB, request.id_transaction
    )

@app.get("/showTransaction/{id_transaction}")
def show_details_transaction(id_transaction: int):
    return show_transaction(id_transaction)


@app.get("/transactions/{account_id}/{user_id}")
def show_all_transactions(account_id: int, user_id: int):
    return get_all_transactions(account_id, user_id)


@app.post("/login")
def login_root(request: LoginBody):
    print(request)
    return login(request.email, request.password)


@app.post("/bank/account/close/{banckAccount_id}")
def close_account_root(banckAccount_id: int):
    return close_account(banckAccount_id)

@app.get("/me")
def get_user(user=Depends(get_user)):
    print(user)
    return get_user_by_id(user["id"])

class RecipientRequest(BaseModel):
    rib: str
    recipient_name: str

import traceback

@app.post("/createRecipient/{user_id}")
def create_recipient(user_id: int, request: RecipientRequest):
    try:
        recipient = find_recipient_rib(request.rib)
        if not recipient:
            return {"error": "Aucun compte trouvé avec ce RIB"}
        return make_recipient(user_id, recipient, request.recipient_name)
    except Exception as e:
        print("🔥 ERREUR BACKEND :", e)
        print(traceback.format_exc())
        raise e




@app.get("/show/recipients/{user_id}")
def show_recipients(user_id: int):
    return show_recipients(user_id)
    
@app.post("/createTransaction")
def send_money_endpoint(request: SendMoneyRequest = Body(...)):
    return send_money(request.id_compteA, request.id_compteB, request.amout)

@app.get("/getDepositById/{deposit_id}")
def get_deposits_by_id_endpoint(deposit_id: int):
    return get_deposit_by_id(deposit_id)

@app.get("/getAccountDeposits/{account_id}")
def get_account_deposits_endpoint(account_id: int):
    return get_account_deposits(account_id)
