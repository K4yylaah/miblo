import pytest
from fastapi import HTTPException
from sqlmodel import Session
from Controllers.depositMoneyControlleur import depositMoney
from models.model import BankAccount

def test_deposit_money_success(test_engine):
    with Session(test_engine) as session:
        compte = BankAccount(id=1,user_id=1,solde=100,rib="FR761234598765",is_primary=True,is_closed=False)
        session.add(compte)
        session.commit()
    result = depositMoney(1, 50, test_engine)
    assert result["nouveau_solde"] == 150
    assert result["deposit"].amout == 50

def test_deposit_money_invalid_amount(test_engine):
    with pytest.raises(HTTPException) as exc:
        depositMoney(1, 0, test_engine)
    assert exc.value.status_code == 400

def test_deposit_money_account_not_found(test_engine):
    with pytest.raises(HTTPException) as exc:
        depositMoney(999, 50, test_engine)
    assert exc.value.status_code == 404
