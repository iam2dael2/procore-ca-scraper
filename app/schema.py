from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Contractor(BaseModel):
    company_name: str
    company_website: str
    company_type: str
    company_province: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserLogin(UserCreate):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None