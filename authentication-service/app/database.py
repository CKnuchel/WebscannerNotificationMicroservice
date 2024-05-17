from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

MYSQL_USER = os.getenv("AUTH_USER")
MYSQL_PASSWORD = os.getenv("AUTH_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_SERVICE_NAME")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_AUTH_DB")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # This creates a Session to interact with the database
Base = declarative_base() # This is the base class for all the models in the application

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
