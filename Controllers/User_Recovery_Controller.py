#Controllers/User_Recovery_Controller.py

from fastapi import HTTPException
from sqlmodel import Session, select
from models.model import User, BankAccount
from database import engine

def get_user_by_id(user_id):
    with Session(engine) as session:
        # recherche l'utilisateur correspondant à l'id
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur introuvable")
        # recupere tout les compte de l'utilisateur
        bank_accounts = session.exec(
            select(BankAccount).where(BankAccount.user_id == user_id)
        ).all()
        user_data = user.dict()
        # Sup password pour ne pas afficher
        user_data.pop("password", None)
        # nombre totale de compte de l'utilisateur
        user_data["count_account"] = len(bank_accounts)
        # Recupere tout les compte de l'utilisateur avec leur id et leur solde
        user_data["comptes"] = [
            {"id": account.id, "solde": account.solde} for account in bank_accounts
        ]
        return {"user": user_data}
