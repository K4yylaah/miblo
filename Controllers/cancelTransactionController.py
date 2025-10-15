from sqlmodel import Session, select
from models.model import Transactions, BankAccount
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