import re

from fastapi import HTTPException
from fastapi.routing import request_response
from sqlalchemy.util import b
from sqlmodel import Session, select, update
from database import engine
from models.model import BankAccount
import random


def rib_generator():
    numberRib = ""
    for _ in range(8):
        numberRib += str(random.randint(0, 9))
    rib = "FR-" + numberRib
    return rib



def create_bank_account(user_id: int, session: Session = None):
    solde = 0
    rib = rib_generator()

    try:
        if session is None:
            with Session(engine) as new_session:
                bank_account = BankAccount(
                    user_id=user_id,
                    solde=solde,
                    rib=rib,
                    is_primary=False
                )
                new_session.add(bank_account)
                new_session.commit()
                new_session.refresh(bank_account)
                return bank_account
        else:
            bank_account = BankAccount(
                user_id=user_id,
                solde=solde,
                rib=rib,
                is_primary=True
            )
            session.add(bank_account)
            session.flush()
            session.refresh(bank_account)
            return bank_account

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création du compte : {str(e)}")



def get_bank_account(user_id):
    with Session(engine) as session:
        test = session.exec(
            select(BankAccount).where(BankAccount.user_id == user_id)
        ).all()
        return test

def get_bank_account_by_rib(rib):
    with Session(engine) as session:
        account = session.exec(
            select(BankAccount).where(BankAccount.rib == rib)
        ).first()

        if not account:
            raise HTTPException(404, "Compte introuvable")

        return account


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
