from fastapi.routing import request_response
from sqlmodel import Session
from database import engine
from models.model import BankAccount


def create_bank_account(id, user_id, solde, rib):
    with Session(engine) as session:
        bank_account = BankAccount(id=id, user_id=user_id, solde=solde, rib=rib)
        session.add(bank_account)
        session.commit()
        session.refresh(bank_account)

        return {"message": "OK"}
