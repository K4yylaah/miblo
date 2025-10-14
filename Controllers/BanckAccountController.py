import re
from fastapi.routing import request_response
from sqlmodel import Session, select
from database import engine
from models.model import BankAccount


def create_bank_account(id, user_id, solde, rib, is_primary):

    with Session(engine) as session:
        bank_account = BankAccount(
            id=id, user_id=user_id, solde=solde, rib=rib, is_primary=is_primary
        )
        session.add(bank_account)
        session.commit()
        session.refresh(bank_account)

    return {"message": "OK"}


def get_bank_account(user_id):
    with Session(engine) as session:
        test = session.exec(
            select(BankAccount).where(BankAccount.user_id == user_id)
        ).all()
        return test
