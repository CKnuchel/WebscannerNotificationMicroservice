from fastapi import FastAPI
from .database import engine, Base
from .scraper import router as scraper_router

Base.metadata.create_all(bind=engine)  # This creates the tables in the database

app = FastAPI()

app.include_router(scraper_router, prefix="/scraper")
