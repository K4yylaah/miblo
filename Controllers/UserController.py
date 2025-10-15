from sqlmodel import Session, create_engine, SQLModel
from database import engine
from models.model import BankAccount, User


def create_user_account(name, password, email):
    with Session(engine) as session:
        user = User(name=name, password=password, email=email)
        session.add(user)
        session.flush()
        solde = 100
        rib = generate_rib()
        bank_account = BankAccount(
            user_id=user.id, solde=solde, rib=rib, is_primary=True
        )
        session.add(bank_account)
        session.commit()
        session.refresh(user)
        session.refresh(bank_account)

    return {"message": "User account created successfully", "user": user}


def generate_rib():
    return "123456789123456789"
