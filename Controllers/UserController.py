from sqlmodel import Session, create_engine, SQLModel

from Controllers.BanckAccountController import create_bank_account
from Controllers.depositMoneyControlleur import depositMoney
from database import engine
from models.model import BankAccount, User


def create_user_account(name: str, password: str, email: str):
    with Session(engine) as session:
        user = User(name=name, password=password, email=email)
        session.add(user)
        session.flush()
        # crée un compte principal
        bank_account = create_bank_account(user.id, session)
        # ajouter 100 pour la creation du compte
        bank_account.solde += 100
        session.commit()
        session.refresh(user)
        session.refresh(bank_account)

    return {
        "message": "User account created successfully",
        "user": user,
        "bank_account": bank_account
    }

