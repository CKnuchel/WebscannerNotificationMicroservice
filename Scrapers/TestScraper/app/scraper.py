import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from urllib.parse import urljoin

from .database import get_db
from .crud import get_categories, get_products, get_product_detail, create_category, create_product, create_product_detail, get_category_by_name, get_product_by_name, get_product_detail_by_product_id
from .models import Category, Product, ProductDetail
from .schemas import CategoryBase, ProductBase, ProductDetailBase
from .rabbitmq import send_message

router = APIRouter()

BASE_URL = "https://webscraper.io"
TEST_SITE_URL = "/test-sites/e-commerce/static"

def fetch_html(url: str):
    response = requests.get(url)
    response.raise_for_status()  # Ensure HTTP request was successful
    return BeautifulSoup(response.text, "html.parser")

@router.get("/categories/", response_model=List[CategoryBase])
def read_categories(db: Session = Depends(get_db)):
    return get_categories(db)

@router.get("/products/", response_model=List[ProductBase])
def read_products(db: Session = Depends(get_db)):
    return get_products(db)

@router.get("/product-details/", response_model=List[ProductDetailBase])
def read_product_details(db: Session = Depends(get_db)):
    return get_product_detail(db)

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
            create_category(db, Category(name=category_name, url=complete_category_url, level="top"))
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
            create_category(db, Category(name=subcategory_name, url=complete_subcategory_url, level="sub"))
            send_message("categories", "sub", {"name": subcategory_name, "url": complete_subcategory_url})

@router.get("/scrape-products")
def scrape_products(db: Session = Depends(get_db)):
    categories = get_categories(db)
    for category in categories:
        soup = fetch_html(category.url)
        products = soup.find_all("div", class_="product")
        for item in products:
            product_name = item.find("h4", class_="product-name").text.strip()
            product_url = urljoin(BASE_URL, item.find("a")['href'])
            if not get_product_by_name(db, product_name):
                create_product(db, Product(name=product_name, category_id=category.id, url=product_url))

@router.get("/scrape-product-details")
def scrape_product_details(db: Session = Depends(get_db)):
    products = get_products(db)
    for product in products:
        soup = fetch_html(product.url)
        description = soup.find("p", class_="description").text.strip()
        if not get_product_detail_by_product_id(db, product.id):
            create_product_detail(db, ProductDetail(product_id=product.id, description=description))
