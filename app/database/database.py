import os
from sqlmodel import Session, create_engine, SQLModel
from urllib.parse import quote_plus


def get_database_url():
    database_url = os.environ.get("DATABASE_URL")
    database_host = os.environ.get("DB_HOST")
    if database_url:
        return database_url
    if database_host:
        database_name = os.environ.get("DB_NAME")
        database_user = os.environ.get("DB_USER")
        database_password = os.environ.get("DB_PASSWORD")
        db_list = [database_name, database_user, database_password]
        if not all(db_list):
            raise RuntimeError("DB_HOST is set but DB_NAME, DB_USER or DB_PASSWORD is missing")
        quoted = quote_plus(database_password)
        return f"postgresql://{database_user}:{quoted}@{database_host}:5432/{database_name}"
    return "sqlite:///database.db"

DATABASE_URL = get_database_url()


connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session