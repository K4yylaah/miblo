from sqlmodel import Session, select
from models.model import Transactions, BankAccount, User, Recipients
from database import engine

def findRecipientRib(rib):
    with (Session(engine)) as session:
        recipient = session.exec(select(BankAccount).where(BankAccount.rib == rib)).first()
        return recipient

def makeRecipient(user_id, recipient):
    with Session(engine) as session:
        recipientCreate = Recipients(user_id=user_id, id_recipient=recipient.id)
        session.add(recipientCreate)
        session.commit()
        session.refresh(recipientCreate)
        return {
            "message": f"Le destinataire a bien été ajouté",
            "user_id": user_id,
            "recipient_id": recipient.id
        }
