from fastapi import Depends, HTTPException
from sqlmodel import select, Session
from urllib3 import request

from models.model import User
from database import get_session, engine
import jwt

def login(email, password):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email==email)).first()
        if not user or user.password != password:
            raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    return {"message": f"Bienvenue {user.email} !"}

secret_key = "1234567890123456789"
algorithm = "HS256"

def generate_token(user: User):
     return jwt.encode(user.dict(), secret_key, algorithm=algorithm)