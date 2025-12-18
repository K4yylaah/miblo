from sqlmodel import Session, select
from models.model import BankAccount, User, Recipients
from database import engine
from datetime import datetime

def find_recipient_rib(rib):
    with (Session(engine)) as session:
        recipient = session.exec(select(BankAccount).where(BankAccount.rib == rib)).first()
        return recipient

def make_recipient(user_id, recipient, recipient_name):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            return {"error": "Utilisateur introuvable"}

        existing = session.exec(select(Recipients).where((Recipients.user_id == user.id) & (Recipients.id_recipient == recipient.id))).first()

        if existing:
            return {"message": f"Le destinataire {recipient.id} est déjà ajouté pour l’utilisateur {user.name}"}

        recipientCreate = Recipients(user_id=user.id, id_recipient=recipient.id, name=recipient_name, date=datetime.now())
        session.add(recipientCreate)
        session.commit()
        session.refresh(recipientCreate)

        return {
            "message": "Le destinataire a bien été ajouté",
            "user_id": user_id,
            "user_name": user.name,
            "recipient_id": recipient.id,
            "recipient_name": recipient_name
        }


def show_recipients(user_id):
    with Session(engine) as session:
        results = session.exec(
            select(Recipients.id, Recipients.name, Recipients.date,BankAccount.rib).join(BankAccount, Recipients.id_recipient == BankAccount.id).where(Recipients.user_id == user_id)).all()
        formatted = []
        for r in results:
            formatted.append({
                "id": r[0],
                "name": r[1],
                "date": r[2],
                "rib": r[3]
            })

        return formatted