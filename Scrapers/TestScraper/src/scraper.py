import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from crud import create_category, get_category_by_name
from schemas import CategoryCreate
from models import Category

BASE_URL = "https://webscraper.io/"
TEST_SITE_URL = "/test-sites/e-commerce/static"

def scrape_categories(db: Session):
    response = requests.get(BASE_URL + TEST_SITE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get the Element that contains the categories
    navigation = soup.find("ul", id="side-menu")
    categories = navigation.find_all("li")

    for category in categories:
        category_name = category.a.text.strip()
        category_url = category.a["href"]

        # Exclude the Nav to the Home Page
        if category_url == TEST_SITE_URL:
            continue

        complete_category_url = BASE_URL + category_url

        # Check if the category already exists in the database 
        if not get_category_by_name(db, category_name):
            create_category(db, CategoryCreate(name=category_name, url=complete_category_url, level="top"))

        # Also Scrape the subcategories
        scrape_subcategories(db, complete_category_url)


def scrape_subcategories(db: Session, category_url: str):
    # Ignoring the base url, to prevent recursion
    if category_url == BASE_URL + TEST_SITE_URL:
        return

    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get the Element that contains the subcategories
    subcategories = soup.find("ul", class_="nav nav-second-level").find_all("li")

    for subcategory in subcategories:
        subcategory_name = subcategory.a.text.strip()
        subcategory_url = subcategory.a["href"]

        complete_subcategory_url = BASE_URL + subcategory_url

        # Check if the subcategory already exists in the database
        if not get_category_by_name(db, subcategory_name):
            # Create the subcategory in the database if it does not exist
            create_category(db, CategoryCreate(name=subcategory_name, url=complete_subcategory_url, level="sub"))

def scrape_products(db: Session,):
    # Get all the subcategories, because they contain all the products
    categories = db.query(Category).filter(Category.level == "sub").all()

    products_to_create = []

    for category in categories:
        response = requests.get(category.url)
        soup = BeautifulSoup(response.text, "html.parser")

        products = soup.find_all("div", class_="col-md-4 col-xl-4 col-lg-4")
        products_to_create.extend(products) # Add all the products to the list

        # Go to the next page if it exists

        # scrape the products and add them to the list

    # Create the products in the database
