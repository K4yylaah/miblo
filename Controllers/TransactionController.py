from fastapi import HTTPException
from sqlmodel import Session, select
from models.model import Transactions, BankAccount, User
from database import engine

def is_avoidableCheck(id_transaction, timer):
    with Session(engine) as session:
        transaction = session.exec(select(Transactions).where(Transactions.id == id_transaction)).first()
        if timer > 5:
            transaction.is_voidable = False

def cancel_transaction(id_compteA, id_compteB, id_transaction):
    #Je recupere le montant de la transaction
    with Session(engine) as session:
        transaction = session.exec(select(Transactions).where(Transactions.id == id_transaction)).first()
        bankaccountA = session.exec(select(BankAccount).where(BankAccount.id == id_compteA)).first()
        bankaccountB = session.exec(select(BankAccount).where(BankAccount.id == id_compteB)).first()

        if not transaction:
            return {"Cette transaction n'existe pas"}

        if transaction.is_voidable==True:
        #Je rajoute le montant au solde du compteA
            bankaccountA.solde+=transaction.amout
        #Je soustret le montant au solde du compteB
            bankaccountB.solde-=transaction.amout
        #Je supprime la transaction
            session.delete(transaction)

        #Je sauvegarde les modifications dans la base
            session.add(bankaccountA)
            session.add(bankaccountB)
            session.commit()
            session.refresh(bankaccountA)
            session.refresh(bankaccountB)

            return {
                "message": f"Transaction {id_transaction} annulée avec succès.",
                "compteA_solde": bankaccountA.solde,
                "compteB_solde": bankaccountB.solde
            }
        else:
            return {
                "message" : "Cette transaction n'est plus annulable"
            }

def show_transaction(id_compteA, id_compteB, id_transaction):
    with Session(engine) as session:
        compteA = session.exec(select(BankAccount).where(BankAccount.id == id_compteA)).first()
        compteB = session.exec(select(BankAccount).where(BankAccount.id == id_compteB)).first()
        transaction = session.exec(select(Transactions).where(Transactions.id == id_transaction)).first()
        userCompteA = session.exec(select(User).where(User.id == compteA.user_id)).first()
        userCompteB = session.exec(select(User).where(User.id == compteB.user_id)).first()


        if not transaction:
            return {"Cette transaction n'existe pas"}
        return {
            "Nom du compte envoyeur" : userCompteA.name,
            "RIB du compte envoyeur" : compteA.rib,
            "Nom du compte qui recoit" : userCompteB.name,
            "RIB du compte qui recoit" : compteB.rib,
            "Montant de la transaction" : transaction.amout,
        }
        
def show_all_transactions(compte_id: int, user_id: int):
    with Session(engine) as session:
        # 1. Vérification de l'appartenance du compte à l'utilisateur
        compte = session.exec(
            select(BankAccount)
            .where(BankAccount.id == compte_id)
            .where(BankAccount.user_id == user_id) 
        ).first()
        
        if not compte: 
            
            raise HTTPException(status_code=404, detail="Compte introuvable")
        
        # 2. Récupération des transactions
        transactions = session.exec(select(Transactions).where(Transactions.id_compteA == compte_id)).all()
        
        if not transactions:
            # Préférer retourner une liste vide plutôt qu'une exception
            return [] 
        return transactions

def send_money(id_compteA: int, id_compteB: int, amout: float):
    if amout <= 0:
        raise HTTPException(status_code=400, detail="Le montant doit être positif")

    if id_compteA == id_compteB:
        raise HTTPException(status_code=400, detail="Le compte destinataire doit être différent du compte source")

    with Session(engine) as session:
        compteA = session.exec(select(BankAccount).where(BankAccount.id == id_compteA)).first()
        compteB = session.exec(select(BankAccount).where(BankAccount.id == id_compteB)).first()

        if not compteA:
            raise HTTPException(status_code=404, detail="Compte source introuvable")
        if not compteB:
            raise HTTPException(status_code=404, detail="Compte destinataire introuvable")

        if compteA.solde < amout:
            raise HTTPException(status_code=400, detail="Solde insuffisant")

        compteA.solde -= amout
        compteB.solde += amout

        transaction = Transactions(
            id_compteA=id_compteA,
            id_compteB=id_compteB,
            amout=amout,
            is_voidable=True
        )

        session.add(transaction)
        session.add(compteA)
        session.add(compteB)
        session.commit()
        session.refresh(compteA)
        session.refresh(compteB)
        session.refresh(transaction)

        return {
            "message": f"Transfert de {amout}€ effectué avec succès",
            "nouveau_solde_source": compteA.solde,
            "nouveau_solde_destinataire": compteB.solde,
            "transaction_id": transaction.id
        }