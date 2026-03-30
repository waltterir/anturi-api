from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes import books, authors
from .database.database import create_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield