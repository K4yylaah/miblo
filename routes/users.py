from pydantic import BaseModel
from fastapi import APIRouter
from fastapi import Depends
from sqlmodel import Session, select
from database import get_session
from models.model import User


class LoginData(BaseModel):
    email: str
    password: str

router = APIRouter()

@router.post("/login")
def login(data: LoginData, session: Session = Depends(get_session)):
    email = data.email
    password = data.password
    statement = select(User).where(User.email == email)
    result = session.exec(statement)
    user = result.first()

