from fastapi import HTTPException, status, Response
from sqlmodel import Session, select
from ..models.models import MittausBase, MittausDB, AnturiDB






def create_mittaus(session: Session, mittaus_in: MittausBase):
    anturi = session.get(AnturiDB, mittaus_in.anturi_id)
    if not anturi: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Anturi not found")
    mittaus = MittausDB.model_validate(mittaus_in)
    session.add(mittaus)
    session.commit()
    session.refresh(mittaus)
    return mittaus

def delete_mittaus(session: Session, anturi_id: int):
    mittaus = session.get(MittausDB, anturi_id)
    if not mittaus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Anturi not found")
    session.delete(mittaus)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
   