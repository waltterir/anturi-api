import os
import pytest
from app.database.database import get_database_url

def test_returns_database_url_when_set(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@host:5432/dbname")
    assert get_database_url() == "postgresql://user:pass@host:5432/dbname"

def test_returns_aws_database_url(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("DB_HOST", "db.example.com")
    monkeypatch.setenv("DB_NAME", "anturi-api")
    monkeypatch.setenv("DB_USER", "postgres")
    monkeypatch.setenv("DB_PASSWORD", "p@ss/word")
    assert get_database_url() == "postgresql://postgres:p%40ss%2Fword@db.example.com:5432/anturi-api"

def test_db_host_raises_error_if_password_missing(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("DB_HOST", "db.example.com")
    monkeypatch.setenv("DB_NAME", "anturi-api")
    monkeypatch.setenv("DB_USER", "postgres")
    monkeypatch.delenv("DB_PASSWORD", raising=False)
    with pytest.raises(RuntimeError, match="DB_PASSWORD"):
        get_database_url()

def test_returns_sqlite_when_no_db_env_set(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("DB_HOST", raising=False)
    assert get_database_url() == "sqlite:///database.db" 