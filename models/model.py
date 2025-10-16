# models.py
import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


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
    created_at: datetime = Field(default_factory=datetime.now)
    amout: float    
    is_voidable: bool

class BankAccount(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    solde: int
    rib : str
    is_primary: Optional[bool] = Field(default=False)
    is_closed: Optional[bool] = Field(default=False)


class Deposits(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_compte: int
    amout: float

class Recipients(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    id_recipient: int