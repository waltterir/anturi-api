from fastapi import APIRouter, status, Depends
from ..models.models import AnturiBase, AnturiOut, AnturiMittausResponse, AnturiTilamuutosHistoriaOut, AnturiTila
from ..crud import anturit_crud as crud
from sqlmodel import Session 
from ..database.database import get_session
from datetime import datetime


router = APIRouter(prefix="/anturit", tags=["Anturit"])

@router.get("/", response_model=list[AnturiOut])
def get_anturit(*, session: Session = Depends(get_session), 
                id: int | None = None, 
                lohko_id: int | None = None, 
                tila: AnturiTila| None = None):
    return crud.get_anturit(session, id, lohko_id, tila)

@router.post("/", status_code=201, response_model=AnturiOut)
def create_anturi(*, session: Session = Depends(get_session), anturi_in: AnturiBase):
    return crud.create_anturi(session, anturi_in)

@router.get("/{anturi_id}/mittaus_tulokset", response_model=AnturiMittausResponse)
def get_anturi_by_id(*, session: Session = Depends(get_session), 
                     anturi_id: int, 
                     start_time: datetime | None = None,
                     end_time: datetime | None = None,
                     page: int = 1,
                     limit: int = 10):
    return crud.get_anturi_by_id(session, anturi_id, start_time, end_time, page, limit)

@router.get("/{anturi_id}/tilamuutokset", response_model=AnturiTilamuutosHistoriaOut)
def get_anturi_tilamuutos(*, session: Session = Depends(get_session), anturi_id: int, tila: AnturiTila):
    return crud.get_anturi_tilamuutos(session, anturi_id)
    

@router.put("/{anturi_id}", response_model=AnturiOut)
def update_anturi(*, session: Session = Depends(get_session), anturi_id: int, anturi_update: AnturiBase):
    return crud.update_anturi(session, anturi_id, anturi_update)