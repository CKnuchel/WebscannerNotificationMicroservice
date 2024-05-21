import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from crud import create_category, get_category_by_name, create_product, create_product_detail
from schemas import CategoryCreate, ProductCreate, ProductDetailCreate
from models import Category, Product

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

    for category in categories:
        if not category:
            continue

        response = requests.get(category.url)
        soup = BeautifulSoup(response.text, "html.parser")

        products = soup.find_all("div", class_="col-md-4 col-xl-4 col-lg-4")
        
        for product in products:
            product_name = product.find("a", class_="title").text.strip()
            product_category_id = category.id
            product_url = BASE_URL + product.find("a", class_="title")["href"]

            # Check if the product already exists in the database
            if not get_product_by_name(db, product_name):
                create_product(db, ProductCreate(name=product_name, category_id=product_category_id, url=product_url))


        # Go to the next page if it exists
        next_page = soup.find("a", rel="next").get("href", None)
        if next_page:
            next_page_url = BASE_URL + next_page
            scrape_products(db, next_page_url)
          

def scrape_product_details(db: Session):
    products = db.query(Product).all()

    for product in products:
        response = requests.get(product.url)
        soup = BeautifulSoup(response.text, "html.parser")

        card = soup.find("div", class_="card")
        product_thumbnail = card.find("img", class_="img-responsive")["src"]
        product_description = card.find("p", class_="description").text.strip()
        product_price = card.find("h4", class_="price").text.strip()
        product_options = card.find_all("div", class_="swatches").find_all("button").text.strip()
        product_reviews = card.find("p", class_="review-count").text.split(' ')[0]

        # Create the product detail in the database, if it does not exist
        create_product_detail(db, ProductDetailCreate(
            product_id=product.id, 
            thumbnail=product_thumbnail, 
            description=product_description, 
            price=product_price, 
            options=product_options, 
            reviews_count=product_reviews))