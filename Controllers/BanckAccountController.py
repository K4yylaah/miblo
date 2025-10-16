from fastapi import HTTPException
from fastapi.routing import request_response
from sqlalchemy.util import b
from sqlmodel import Session, select, update
from database import engine
from models.model import BankAccount, User


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

# amoutCheck verifie si le depot peut etre effectué sans depasser la limite de 5000€. Si la limite est dépassé, alors l'argent exedant est envoyé sur le compte principal
def amoutCheck(acount_id, amout):
    with Session(engine) as session:
        account = session.exec(select(BankAccount).where(BankAccount.user_id == acount_id)).first()
        user = session.exec(select(User).where(User.id == account.user_id)).first()
        primaryAccount = session.exec(select(BankAccount).where(BankAccount.user_id == user.id)) and (BankAccount.is_primary == True)
        if account.solde + amout > 5000:
            amoutToPrimaryAccount = 5000 - (account.solde + amout)
            primaryAccount.solde = account.solde + amoutToPrimaryAccount
            account.solde = 5000
            return {
                "message": "Ce compte a atteint sa limite de solde, le montant exedant a été transferé au compte principal."
            }
        return {
            "message": "La transaction peut etre effectué"
        }