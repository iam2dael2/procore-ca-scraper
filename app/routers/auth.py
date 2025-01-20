from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from sqlmodel import select

from .. import schema, models, utils, oauth2
from ..database import get_session, Session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: SessionDep):
    # Verify whether the email is contained in the database
    user_by_email = db.exec(select(models.User).where(models.User.email == user_credentials.username)).first()
    
    if user_by_email == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # Verify the password of user
    if not utils.verify_password(user_credentials.password, hashed_password=user_by_email.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token: dict = oauth2.create_access_token(data={"user_id": user_by_email.id})
    return schema.Token(access_token=access_token, token_type="bearer")