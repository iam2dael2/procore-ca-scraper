from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from .database import create_db_and_tables
from .routers import users, contractors, auth

# Initialize database and tables
# create_db_and_tables()

app = FastAPI()

# origins = ["https://www.google.com"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(users.router)
app.include_router(contractors.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}