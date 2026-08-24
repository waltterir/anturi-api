from fastapi import APIRouter, status, Depends
from ..models.models import MittausBase, MittausOut
from ..crud import mittaukset_crud as crud
from sqlmodel import Session
from ..database.database import get_session


router = APIRouter(prefix="/mittaukset", tags=["Mittaukset"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MittausOut)
def create_mittaus(*, session: Session = Depends(get_session), mittaus_in: MittausBase):
    return crud.create_mittaus(session, mittaus_in)

@router.delete("/{mittaus_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mittaus(*, session: Session = Depends(get_session), mittaus_id: int):
    return crud.delete_mittaus(session, mittaus_id)