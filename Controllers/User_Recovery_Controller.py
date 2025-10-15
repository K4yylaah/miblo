#Controllers/User_Recovery_Controller.py

from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from models.model import User
from database import engine

def get_user_by_id(user_id):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur introuvable")
        user_data = user.dict()
        user_data.pop("password", None)
        return {"user": user_data}
