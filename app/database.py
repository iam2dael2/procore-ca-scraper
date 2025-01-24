from sqlmodel import SQLModel, Session, create_engine
from .config import settings

SQLMODEL_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# CONNECT_ARGS = {"check_same_thread": False}

engine = create_engine(SQLMODEL_DATABASE_URL) # , connect_args=CONNECT_ARGS)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session