# models.py
from typing import Optional
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class Transactions(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_compteA: int
    id_compteB: int

class BankAccount(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    solde: float
    rib : str

class Deposits(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_compte: int
    amout:float
