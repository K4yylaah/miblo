from fastapi import HTTPException
from sqlmodel import Session, select
from models.model import Transactions, BankAccount, User
from database import engine


def is_avoidable_check(id_transaction, timer):
    with Session(engine) as session:
        transaction = session.exec(select(Transactions).where(Transactions.id == id_transaction)).first()
        if timer > 5:
            transaction.is_voidable = False

def cancel_transaction(id_compteA, id_compteB, id_transaction):
    #Je recupere le montant de la transaction
    with Session(engine) as session:
        transaction = session.exec(select(Transactions).where(Transactions.id == id_transaction)).first()
        bankaccount_a = session.exec(select(BankAccount).where(BankAccount.id == id_compteA)).first()
        bankaccount_b = session.exec(select(BankAccount).where(BankAccount.id == id_compteB)).first()

        if not transaction:
            return {"Cette transaction n'existe pas"}

        if transaction.is_voidable==True:
        #Je rajoute le montant au solde du compteA
            bankaccount_a.solde+=transaction.amout
        #Je soustret le montant au solde du compteB
            bankaccount_b.solde-=transaction.amout
        #Je supprime la transaction
            session.delete(transaction)

        #Je sauvegarde les modifications dans la base
            session.add(bankaccount_a)
            session.add(bankaccount_b)
            session.commit()
            session.refresh(bankaccount_a)
            session.refresh(bankaccount_b)

            return {
                "message": f"Transaction {id_transaction} annulée avec succès.",
                "compteA_solde": bankaccount_a.solde,
                "compteB_solde": bankaccount_b.solde
            }
        else:
            return {
                "message" : "Cette transaction n'est plus annulable"
            }

def show_transaction(id_transaction):
    with Session(engine) as session:
        transaction = session.exec(select(Transactions).where(Transactions.id == id_transaction)).first()
        compte_a = session.exec(select(BankAccount).where(BankAccount.id == Transactions.id_compteA)).first()
        compte_b = session.exec(select(BankAccount).where(BankAccount.id == Transactions.id_compteB)).first()
        user_compte_b = session.exec(select(User).where(User.id == Transactions.id_compteA)).first()
        user_compte_b = session.exec(select(User).where(User.id == Transactions.id_compteB)).first()

        if not transaction:
            return {"Cette transaction n'existe pas"}
        return {
            "Nom du compte envoyeur" : user_compte_b.name,
            "RIB du compte envoyeur" : compte_a.rib,
            "Nom du compte qui recoit" : user_compte_b.name,
            "RIB du compte qui recoit" : compte_b.rib,
            "Montant de la transaction" : transaction.amout,
        }
        
def get_all_transactions(compte_id, user_id): 
    with Session(engine) as session:
        # 1. Vérification de l'appartenance du compte à l'utilisateur
        compte = session.exec(select(BankAccount).where((BankAccount.id == compte_id) & (BankAccount.user_id == user_id))).first()
        if not compte: 
            raise HTTPException(status_code=404, detail="Compte introuvable")
        
        # 2. Récupération des transactions
        transactions = session.exec(select(Transactions).where(Transactions.id_compteA == compte_id)).all() # Inclus les transactions où le compte est source
        transactions += session.exec(select(Transactions).where(Transactions.id_compteB == compte_id)).all() # Inclus les transactions où le compte est destinataire
        
        transactions.sort(key=lambda x: x.id, reverse=True) # Tri par ordre décroissant plus récentes en premières
        transactions = list({t.id: t for t in transactions}.values()) # Suppression des doublons si une transaction est à la fois source et destinataire
        
        if not transactions:
            # Préférer retourner une liste vide plutôt qu'une exception
            return [] 
        return transactions

def send_money(id_compte_a: int, id_compte_b: int, amout: float):
    if amout <= 0:
        raise HTTPException(status_code=400, detail="Le montant doit être positif")

    if id_compte_a == id_compte_b:
        raise HTTPException(status_code=400, detail="Le compte destinataire doit être différent du compte source")



    with Session(engine) as session:
        compte_a = session.exec(select(BankAccount).where(BankAccount.id == id_compte_a)).first()
        compte_b = session.exec(select(BankAccount).where(BankAccount.id == id_compte_b)).first()

        if compte_a.is_closed == True:
            return {"message": "Le compte est fermer impossbile de faire le transfert"}
        if compte_b.is_closed == True:
            return {"message": "Le compte est fermer impossbile de faire le transfert"}

        if not compte_a:
            raise HTTPException(status_code=404, detail="Compte source introuvable")
        if not compte_b:
            raise HTTPException(status_code=404, detail="Compte destinataire introuvable")

        if compte_a.solde < amout:
            raise HTTPException(status_code=400, detail="Solde insuffisant")

        compte_a.solde -= amout
        compte_b.solde += amout

        # Créer un enregistrement de la transaction
        transaction = Transactions(
            id_compteA=id_compte_a,
            id_compteB=id_compte_b,
            amout=amout,
            is_voidable=True
        )

        # Sauvegarde les changements
        session.add(transaction)
        session.add(compte_a)
        session.add(compte_b)
        session.commit()
        #Refresh pour avoir les valeurs a jours
        session.refresh(compte_a)
        session.refresh(compte_b)
        session.refresh(transaction)

        return {
            "message": f"Transfert de {amout}€ effectué avec succès",
            "nouveau_solde_source": compte_a.solde,
            "nouveau_solde_destinataire": compte_b.solde,
            "transaction_id": transaction.id
        }