import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from typing import List
from .database import get_db
from .crud import create_category, get_category_by_name, create_product, create_product_detail, get_product_by_name, get_product_detail_by_name, get_categories, get_products, get_product_detail
from .schemas import CategoryCreate, ProductCreate, ProductDetailCreate, Category, Product, ProductDetail
from .rabbitmq import send_message

router = APIRouter()

BASE_URL = "https://webscraper.io"
TEST_SITE_URL = "/test-sites/e-commerce/static"

def fetch_html(url: str):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return BeautifulSoup(response.text, "html.parser")

@router.get("/scrape-categories")
def scrape_categories(db: Session = Depends(get_db)):
    soup = fetch_html(BASE_URL + TEST_SITE_URL)
    navigation = soup.find("ul", id="side-menu")
    categories = navigation.find_all("li")

    for category in categories:
        category_name = category.a.text.strip()
        category_url = category.a["href"]

        if category_url == TEST_SITE_URL:
            continue

        complete_category_url = BASE_URL + category_url

        if not get_category_by_name(db, category_name):
            create_category(db, CategoryCreate(name=category_name, url=complete_category_url, level="top"))
            send_message("categories", "top", {"name": category_name, "url": complete_category_url})

        scrape_subcategories(db, complete_category_url)

def scrape_subcategories(db: Session, category_url: str):
    if category_url == BASE_URL + TEST_SITE_URL:
        return

    soup = fetch_html(category_url)
    subcategories = soup.find("ul", class_="nav nav-second-level").find_all("li")

    for subcategory in subcategories:
        subcategory_name = subcategory.a.text.strip()
        subcategory_url = subcategory.a["href"]
        complete_subcategory_url = BASE_URL + subcategory_url

        if not get_category_by_name(db, subcategory_name):
            create_category(db, CategoryCreate(name=subcategory_name, url=complete_subcategory_url, level="sub"))
            send_message("categories", "sub", {"name": subcategory_name, "url": complete_subcategory_url})

@router.get("/scrape-products")
def scrape_products(db: Session = Depends(get_db)):
    categories = db.query(Category).filter(Category.level == "sub").all()

    for category in categories:
        if not category:
            continue

        soup = fetch_html(category.url)
        products = soup.find_all("div", class_="thumbnail")

        for product in products:
            product_name = product.find("a", class_="title").text.strip()
            product_category_id = category.id
            product_url = BASE_URL + product.find("a", class_="title")["href"]
            product_price = float(product.find("h4", class_="pull-right price").text.strip().replace("$", ""))
            product_description = product.find("p", class_="description").text.strip()

            if not get_product_by_name(db, product_name):
                create_product(db, ProductCreate(
                    name=product_name,
                    category_id=product_category_id,
                    url=product_url,
                    price=product_price,
                    description=product_description
                ))
                send_message("products", "new", {
                    "name": product_name,
                    "category_id": product_category_id,
                    "url": product_url,
                    "price": product_price,
                    "description": product_description
                })

        next_page = soup.find("a", rel="next")
        if next_page and next_page.get("href"):
            next_page_url = BASE_URL + next_page["href"]
            scrape_products(db, next_page_url)

@router.get("/scrape-product-details")
def scrape_product_details(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    for product in products:
        soup = fetch_html(product.url)

        card = soup.find("div", class_="card")
        product_thumbnail = card.find("img", class_="img-responsive")["src"]
        product_description = card.find("p", class_="description").text.strip()
        product_price = card.find("h4", class_="price").text.strip()
        product_options = [option.text.strip() for option in card.find_all("div", class_="swatches").find_all("button")]
        product_reviews = card.find("p", class_="review-count").text.split(' ')[0]

        if not get_product_detail_by_name(db, product.name):
            create_product_detail(db, ProductDetailCreate(
                product_id=product.id, 
                thumbnail=product_thumbnail, 
                description=product_description, 
                price=product_price, 
                options=product_options, 
                reviews_count=int(product_reviews)
            ))
            send_message("product_details", "new", {
                "product_id": product.id, 
                "thumbnail": product_thumbnail, 
                "description": product_description, 
                "price": product_price, 
                "options": product_options, 
                "reviews_count": int(product_reviews)
            })

# Read endpoints

@router.get("/categories/", response_model=List[Category])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = get_categories(db, skip=skip, limit=limit)
    return categories

@router.get("/products/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = get_products(db, skip=skip, limit=limit)
    return products

@router.get("/product-details/", response_model=List[ProductDetail])
def read_product_details(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    product_details = get_product_detail(db, skip=skip, limit=limit)
    return product_details
