from fastapi import APIRouter, status, Depends
from ..models.models import LohkoOut, LohkoBase, AnturiOut
from ..crud import lohkot_crud as crud
from sqlmodel import Session
from ..database.database import get_session

router = APIRouter(prefix="/lohkot", tags=["Lohkot"])

@router.post("/", status_code=status.HTTP_201_CREATED ,response_model=LohkoOut)
def create_lohko(*, session: Session = Depends(get_session), lohko_in: LohkoBase):
    return crud.create_lohko(session, lohko_in)

@router.get("/{lohko_id}/anturit")
def get_lohko_anturit(
    lohko_id: int,
    session: Session = Depends(get_session)
):
    return crud.get_lohko_anturit(session, lohko_id)