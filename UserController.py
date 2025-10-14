from sqlmodel import Session, create_engine, SQLModel
from database import engine
from models.model import User

def create_user_account(name, password, email):
    with Session(engine) as session:
        user = User(name =name, password=password, email=email)
        session.add(user)
        session.commit()
        session.refresh(user)
        
    return {"message": "User account created successfully", "user": user}