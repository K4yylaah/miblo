import re

from fastapi import HTTPException
from fastapi.routing import request_response
from sqlalchemy.util import b
from sqlmodel import Session, select, update
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



def close_account(bank_account_id: int):
    with Session(engine) as session:

        account = session.get(BankAccount, bank_account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Compte introuvable")


        if account.is_primary:
            raise HTTPException(status_code=400, detail="Impossible de fermer le compte principal")


        if account.is_closed:
            raise HTTPException(status_code=400, detail="Ce compte est déjà clôturé")


        stmt = select(BankAccount).where(
            BankAccount.user_id == account.user_id,
            BankAccount.is_primary == True,
            BankAccount.is_closed == False
        )
        main_account = session.scalars(stmt).first()

        if not main_account:
            raise HTTPException(status_code=400, detail="Aucun compte principal actif trouvé pour cet utilisateur")

        main_account.solde += account.solde
        account.solde = 0.0

        account.is_closed = True

        session.commit()
        session.refresh(account)
        session.refresh(main_account)

        return {
            "message": "Compte clôturé avec succès. Solde transféré vers le compte principal.",
            "closed_account_id": account.id,
            "main_account_solde": main_account.solde
        }