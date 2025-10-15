from sqlmodel import Session, select
from models.model import Transactions, BankAccount, User
from database import engine


def cancel_transaction(id_compteA, id_compteB, id_transaction):
    #Je recupere le montant de la transaction
    with Session(engine) as session:
        transaction = session.exec(select(Transactions).where(Transactions.id == id_transaction)).first()
        bankaccountA = session.exec(select(BankAccount).where(BankAccount.id == id_compteA)).first()
        bankaccountB = session.exec(select(BankAccount).where(BankAccount.id == id_compteB)).first()

        if not transaction:
            return {"Cette transaction n'existe pas"}
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
        
def show_all_transactions(compte_id):
    with Session(engine) as session:
        transactions = session.exec(select(Transactions).where((Transactions == compte_id) | (Transactions == compte_id))).all()
        if not transactions:
            return {"Aucune transaction trouvée pour ce compte."}
        return transactions