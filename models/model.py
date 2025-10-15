# models.py
from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    password: str = Field(min_length=6, max_length=9)
    count_account: float = Field(default=0.0)


class Transactions(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_compteA: int
    id_compteB: int
    amout: float

class BankAccount(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    solde: float
    rib : str
    is_primary: bool

class Deposits(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_compte: int
    amout:float

