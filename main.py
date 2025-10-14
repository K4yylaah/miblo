from fastapi import FastAPI
from pydantic import BaseModel

from database import create_db_and_tables

""""app = FastAPI()
@app.get("/")
def read_root():
        return {"message": "Bienvenue sur FastAPI!"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()"""

class User(BaseModel):
    id: int
    solde: int

class Transactions(BaseModel):
    id: int
    id_compteA: int
    id_compteB: int

compte1 = User(id=1, solde=100)
compte2 = User(id=2, solde=100)




def echange(compteA, compteB, var):
    transaction = Transactions(id =1, id_compteA=compteA.id, id_compteB=compteB.id)
    print(compteA.id, compteB.id)
    compteB.solde = compteB.solde + var
    compteA.solde= compteA.solde - var
    return transaction

print(echange(compte1, compte2, 50))
print(compte1.solde)
print(compte2.solde)