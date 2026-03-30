from fastapi import APIRouter, status, Depends
from ..models.models import LohkoOut, LohkoBase
from ..crud import lohkot_crud as crud
from sqlmodel import Session
from ..database.database import get_session

router = APIRouter(prefix="/lohkot", tags=["Lohkot"])

@router.post("/", status_code=status.HTTP_201_CREATED ,response_model=LohkoOut)
def create_lohko(*, session: Session = Depends(get_session), lohko_in: LohkoBase):
    return crud.create_lohko(session, lohko_in)