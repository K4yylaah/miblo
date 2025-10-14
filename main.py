from contextlib import asynccontextmanager


from fastapi import FastAPI
from pydantic import BaseModel
from Controllers.BanckAccountController import create_bank_account
from database import create_db_and_tables
from Controllers.depositMoneyControlleur import depositMoney
from models.model import BankAccount, Transactions
from Controllers.cancelTransactionController import cancel_transaction
from database import engine
from sqlmodel import Session
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


@app.get("/bank/account")
def bank_account_root(bankAccount: BankAccount):
    return bankAccount


class DepositRequest(BaseModel):
    compteId: int
    amout: float
@app.post("/depositMoney")
def make_deposit(request: DepositRequest):
    return depositMoney(request.compteId, request.amout)

class TransactionRequest(BaseModel):
    id_compteA: int
    id_compteB: int
    amout: float

class CreateAccountRequest(BaseModel):
    user_id: int
    solde: float
    rib: str

@app.post("/createBankAccount")
def create_bank_account(request: CreateAccountRequest):
    with Session(engine) as session:
        account = BankAccount(
            user_id=request.user_id,
            solde=request.solde,
            rib=request.rib
        )
        session.add(account)
        session.commit()
        session.refresh(account)
        return {"message": "Compte créé avec succès.", "compte": account}

@app.post("/createTransaction")
def create_transaction(request: TransactionRequest):
    with Session(engine) as session:
        transaction = Transactions(
            id_compteA=request.id_compteA,
            id_compteB=request.id_compteB,
            amout=request.amout
        )
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return {
            "message": "Transaction créée avec succès.",
            "transaction": transaction
        }

class CancelTransactionRequest(BaseModel):
    id_compteA: int
    id_compteB: int
    id_transaction: int

@app.post("/cancelTransaction")
def cancel_transaction_endpoint(request: CancelTransactionRequest):
    return cancel_transaction(request.id_compteA, request.id_compteB, request.id_transaction)


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
