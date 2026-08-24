import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from app.models.models import LohkoDB, AnturiDB, AnturiTila

from app.main import app
from app.database.database import get_session

TEST_DB = "test.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DB}"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

def override_get_session():
    with Session(test_engine) as session:
        yield session

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture(name="client")
def client_fixture(session):
    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

@pytest.fixture
def lohko(session):
    lohko = LohkoDB(lohko_name="Testilohko")
    session.add(lohko)
    session.commit()
    session.refresh(lohko)
    return lohko


@pytest.fixture
def anturi(session, lohko):
    anturi = AnturiDB(anturi_name="Testianturi", lohko_id=lohko.id, tila=AnturiTila.NORMAL)
    session.add(anturi)
    session.commit()
    session.refresh(anturi)
    return anturi