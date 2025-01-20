from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from sqlalchemy import Column, TIMESTAMP, text

class Contractor(SQLModel, table=True):
    __tablename__ = "contractors"
    
    company_id: int = Field(primary_key=True)
    company_name: str = Field(index=True)
    company_website: str
    company_type: str
    company_province: str = Field(index=True)

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str
    created_at: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True),nullable=False, server_default=text("now()")))