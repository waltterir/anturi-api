from fastapi import HTTPException, status, Response
from sqlmodel import Session, select, desc
from ..models.models import AnturiDB, AnturiBase, LohkoDB, MittausDB
from datetime import datetime


def get_anturit(session: Session, 
                id: int | None = None,
                name: str | None = None,
                lohko_id: int | None = None,
                tila: str | None = None,
                ):
    statement = select(AnturiDB)
    if id is not None:
        statement = statement.where(AnturiDB.id == id)
    if name is not None:
        statement = statement.where(AnturiDB.name == name)
    if lohko_id is not None:
        statement = statement.where(AnturiDB.lohko_id == lohko_id)
    if tila is not None:
        statement = statement.where(AnturiDB.tila == tila)

    return session.exec(statement).all()

def create_anturi(session: Session, anturi_in: AnturiBase):
    lohko = session.get(LohkoDB, anturi_in.lohko_id)
    if not lohko: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Lohko not found")
    anturi = AnturiDB.model_validate(anturi_in)
    session.add(anturi)
    session.commit()
    session.refresh(anturi)
    return anturi
   

def get_anturi_by_id(session: Session, 
                     anturi_id: int, 
                     start_time: datetime | None = None, 
                     end_time: datetime | None = None, 
                     page: int = 1, 
                     limit: int = 10):
    
    anturi = session.get(AnturiDB, anturi_id)
    if not anturi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Anturi with {anturi_id} not found")
    if page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Page must be atleast 1")
    if limit < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Limit must be atleast 1")
    if limit > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Limit must be under 100")
    if start_time is not None:
        mittaus_statement = mittaus_statement.where(MittausDB.ajankohta >= start_time)
    if end_time is not None: 
        mittaus_statement = mittaus_statement.where(MittausDB.ajankohta <= end_time)    
    
    mittaus_statement = select(MittausDB).where(MittausDB.anturi_id == anturi_id)

    if start_time is not None and end_time is not None:
        if start_time > end_time:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Start time cannot be greater than end time")
    
    

    

    mittaus_statement = mittaus_statement.order_by(desc(MittausDB.ajankohta))
    mittaus_statement = mittaus_statement.offset((page - 1) * limit)
    mittaus_statement = mittaus_statement.limit(limit)
    
    mittaus_statement = session.exec(mittaus_statement).all()

    return {"anturi": anturi, "mittaukset": mittaus_statement}

