import bcrypt
from sqlmodel import Session, create_engine, SQLModel

from Controllers.BanckAccountController import create_bank_account
from Controllers.depositMoneyControlleur import depositMoney
from database import engine
from models.model import BankAccount, User

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_user_account(name: str, password: str, email: str):
    with Session(engine) as session:
        hashed_pw = hash_password(password)
        user = User(name=name, password=hashed_pw, email=email)
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