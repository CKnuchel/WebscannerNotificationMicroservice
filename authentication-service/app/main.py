from fastapi import FastAPI
from .auth import router as auth_router
from .database import engine, Base

Base.metadata.create_all(bind=engine) # This creates the tables in the database

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
