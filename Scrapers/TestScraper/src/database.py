import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database connection variables
MYSQL_USER = os.getenv("MYSQL_TEST_SCRAPER_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_TEST_SCRAPER_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_TEST_SCRAPER_SERVICE_NAME")
MYSQL_PORT = os.getenv("MYSQL_TEST_SCRAPER_PORT")
MYSQL_DB = os.getenv("MYSQL_TEST_SCRAPER_DATABASE")

# Database connection URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the database models
Base = declarative_base()

# Create a function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()