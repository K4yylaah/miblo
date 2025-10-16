from sqlmodel import Session, select
from models.model import Transactions, BankAccount, User, Recipients
from database import engine

def findRecipientRib(rib):
    with (Session(engine)) as session:
        recipient = session.exec(select(BankAccount).where(BankAccount.rib == rib)).first()
        return recipient

def makeRecipient(user_id, recipient):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            return {"error": "Utilisateur introuvable"}

        existing = session.exec(select(Recipients).where((Recipients.user_id == user.id) & (Recipients.id_recipient == recipient.id))).first()

        if existing:
            return {"message": f"Le destinataire {recipient.id} est déjà ajouté pour l’utilisateur {user.name}"}

        recipientCreate = Recipients(user_id=user.id, id_recipient=recipient.id)
        session.add(recipientCreate)
        session.commit()
        session.refresh(recipientCreate)

        return {
            "message": "Le destinataire a bien été ajouté",
            "user_id": user_id,
            "user_name": user.name,
            "recipient_id": recipient.id
        }


def showRecipients(user_id):
    with Session(engine) as session:
        recipients = session.exec(select(Recipients).where(Recipients.user_id == user_id)).all()
    return recipients