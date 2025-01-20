from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from typing import Annotated
from .. import models, schema, utils
from ..database import get_session, Session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{id}", response_model=schema.User)
def get_one_user(id: int, db: SessionDep):
    user = db.exec(select(models.User).where(models.User.id == id)).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} is not found")
    
    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.User)
def create_user(user: schema.UserCreate, db: SessionDep):
    user.password = utils.hash(user.password)
    user = models.User(**user.model_dump())

    db.add(user)
    db.commit()
    db.refresh(user)
    return user