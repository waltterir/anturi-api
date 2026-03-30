from fastapi import HTTPException, status, Response
from sqlmodel import Session, select
from ..models.models import AnturiDB, AnturiOut


def get_anturit(session: Session, 
                id: int,
                lohko_id: int,
                tila: str,
                ):
    statement = select(AnturiDB)
    if id is not None:
        statement = statement.where(AnturiDB.id == id)
    if lohko_id is not None:
        statement = statement.where(AnturiDB.lohko_id == lohko_id)
    if tila is not None:
        statement = statement.where(AnturiDB.tila == tila)

    return session.exec(statement).all()
   

def get_anturi_by_id(session: Session, anturi_id: int):
    anturi = session.get(AnturiDB, anturi_id)
    if not anturi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Anturi with {anturi_id} not found")
    return anturi

