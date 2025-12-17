from fastapi import HTTPException
from sqlmodel import Session, select
from models.model import BankAccount, Deposits
from database import engine


def depositMoney(compteId, amout, engine):
    if amout<=0:
        raise HTTPException(status_code=400, detail="Le dépôt doit être strictement supérieur à 0")

    with Session(engine) as session:
        compte = session.exec(select(BankAccount).where(BankAccount.id == compteId)).first()

        if not compte:
            raise HTTPException(status_code=404, detail="Compte introuvable.")

        compte.solde += amout
        session.add(compte)

        deposit = Deposits(id_compte=compteId, amout=amout)
        session.add(deposit)

        session.commit()
        session.refresh(compte)
        session.refresh(deposit)

        return {
            "message": f"Dépôt de {amout} € effectué ",
            "nouveau_solde": compte.solde,
            "deposit": deposit
        }

def get_depositById(id_deposit):
    with Session(engine) as session:
        deposit = session.exec(select(Deposits).where(Deposits.id == id_deposit)).first()
        return deposit

def getAccountDeposits(id_account):
    with Session(engine) as session:
        account = session.exec(select(BankAccount).where(BankAccount.id == id_account)).first()
        deposits = session.exec(select(Deposits).where(Deposits.id_compte == account.id)).all()
        depositsDict = {}
        for deposit in deposits:
            depositsDict[deposit.id] = deposit
        return depositsDict