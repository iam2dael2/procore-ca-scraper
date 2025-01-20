from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from typing import Annotated, List
from .. import models, schema, oauth2
from ..database import get_session, Session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter(prefix="/contractors", tags=["contractors"])

@router.get("/", response_model=List[schema.Contractor])
def get_contractors(db: SessionDep, limit: int = 10, user_login_first: models.User = Depends(oauth2.get_current_user)):
    contractors = db.exec(select(models.Contractor).limit(limit)).all()
    return contractors

@router.get("/{company_id}", response_model=schema.Contractor)
def get_one_contractor(company_id: int, db: SessionDep, user_login_first: models.User = Depends(oauth2.get_current_user)):
    contractor = db.exec(select(models.Contractor).where(models.Contractor.company_id == company_id)).first()
    if contractor == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Company with id: {company_id} is not found")
    
    return contractor