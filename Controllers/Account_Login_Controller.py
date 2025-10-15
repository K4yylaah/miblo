#Controllers/Account_Login_Controller.py

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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

    return {"token": generate_token(user)}

secret_key = "very_secret_key"
algorithm = "HS256"

def generate_token(user: User):
     return jwt.encode(user.dict(), secret_key, algorithm=algorithm)

bearer_scheme = HTTPBearer()

def get_user(authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
     return jwt.decode(authorization.credentials, secret_key, algorithms=[algorithm])