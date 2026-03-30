from fastapi import HTTPException, status
from sqlmodel import Session, select, desc
from ..models.models import LohkoDB, LohkoBase

def create_lohko(session: Session, lohko_in: LohkoBase):
    lohko = LohkoDB.model_validate(lohko_in)
    if not lohko:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Lohko not found")
    session.add(lohko)
    session.commit()
    session.refresh(lohko)
    return lohko

