from fastapi import HTTPException
from sqlmodel import Session, select
from models.model import BankAccount, Deposits
from database import engine


def deposit_money(compte_id, amout, engine):
    if amout<=0:
        raise HTTPException(status_code=400, detail="Le dépôt doit être strictement supérieur à 0")

    with Session(engine) as session:
        compte = session.exec(select(BankAccount).where(BankAccount.id == compte_id)).first()

        if not compte:
            raise HTTPException(status_code=404, detail="Compte introuvable.")

        compte.solde += amout
        session.add(compte)

        deposit = Deposits(id_compte=compte_id, amout=amout)
        session.add(deposit)

        session.commit()
        session.refresh(compte)
        session.refresh(deposit)

        return {
            "message": f"Dépôt de {amout} € effectué ",
            "nouveau_solde": compte.solde,
            "deposit": deposit
        }

def get_deposit_by_id(id_deposit):
    with Session(engine) as session:
        deposit = session.exec(select(Deposits).where(Deposits.id == id_deposit)).first()
        return deposit

def get_account_deposits(id_account):
    with Session(engine) as session:
        account = session.exec(select(BankAccount).where(BankAccount.id == id_account)).first()
        deposits = session.exec(select(Deposits).where(Deposits.id_compte == account.id)).all()
        deposits_dict = {}
        for deposit in deposits:
            deposits_dict[deposit.id] = deposit
        return deposits_dict