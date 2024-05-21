from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import requests
from typing import List

from database import SessionLocal
from crud import get_categories, get_products, get_product_details
import schemas
from scraper import run_scraper

oauth2scheme = OAuth2PasswordBearer(tokenUrl="token")
AUTH_SERVICE_URL = "http://fastapi-auth:8000"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_token_with_auth_service(token: str) -> dict:
    """
    Verify the token with the auth service
    Returns the user data if the token is valid, otherwise raises an HTTPException
    """
    response = requests.get(f"{AUTH_SERVICE_URL}/validate-token", headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        return response.json()
    raise HTTPException(
        status_code=response.status_code,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

def get_current_user(token: str = Depends(oauth2scheme)):
    """
    Dependency function to get the current user
    """
    return verify_token_with_auth_service(token)

app = FastAPI()

# Endpoint to trigger scraper
@app.post("/scraper/{scrape_option}")
def trigger_scraper(scrape_option: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    valid_options = ["categories", "subcategories", "products", "product_details"]
    if scrape_option not in valid_options:
        raise HTTPException(status_code=400, detail="Invalid scrape option")

    background_tasks.add_task(run_scraper, scrape_option)
    return {"message": f"Scraper triggered for {scrape_option}"}

# Endpoint to get categories
@app.get("/categories", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    categories = get_categories(db, skip=skip, limit=limit)
    return categories

# Endpoint to get products
@app.get("/products", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    products = get_products(db, skip=skip, limit=limit)
    return products

# Endpoint to get product details
@app.get("/product_details", response_model=List[schemas.ProductDetail])
def read_product_details(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    product_details = get_product_details(db, skip=skip, limit=limit)
    return product_details