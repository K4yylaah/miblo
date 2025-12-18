import pytest
from sqlmodel import SQLModel, create_engine, Session
from models.model import BankAccount, Deposits

@pytest.fixture
def test_engine():
    engine = create_engine("sqlite://", echo=False)

    SQLModel.metadata.create_all(engine)

    yield engine

    SQLModel.metadata.drop_all(engine)
