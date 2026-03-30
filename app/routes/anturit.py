from fastapi import APIRouter, status, Depends
from ..models.models import AnturiBase, AnturiOut
from ..crud import anturit_crud as crud
from sqlmodel import Session 
from ..database.database import get_session


router = APIRouter(prefix="/anturit", tags=["Anturit"])

@router.get("/", response_model=list[AnturiOut])
def get_anturit(*, session: Session = Depends(get_session), 
                id: int | None = None, 
                lohko_id: int | None = None, 
                tila: str | None = None):
    return crud.get_anturit(session, id, lohko_id, tila)