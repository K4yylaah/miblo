#Controllers/User_Recovery_Controller.py

from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from models.model import User, BankAccount
from database import engine

def get_user_by_id(user_id):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur introuvable")
        bank_accounts = session.exec(
            select(BankAccount).where(BankAccount.user_id == user_id)
        ).all()
        user_data = user.dict()
        user_data.pop("password", None)
        user_data["comptes"] = [
            {"id": account.id, "solde": account.solde} for account in bank_accounts
        ]
        return {"user": user_data}
