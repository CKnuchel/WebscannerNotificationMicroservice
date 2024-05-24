import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from urllib.parse import urljoin
from typing import List

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
    categories = db.query(Category).filter(Category.level == "sub").all()

    for category in categories:
        category_url = category.url
        while category_url:
            soup = fetch_html(category_url)
            products = soup.find_all("div", class_="thumbnail")
            for product in products:
                product_name = product.find("a", class_="title").text.strip()
                product_category_id = category.id
                product_url = urljoin(BASE_URL, product.find("a", class_="title")["href"])

                if not get_product_by_name(db, product_name):
                    create_product(db, Product(
                        name=product_name,
                        category_id=product_category_id,
                        url=product_url
                    ))
                    send_message("products", "new", {
                        "name": product_name,
                        "category_id": product_category_id,
                        "url": product_url
                    })

            # Correctly handle pagination
            next_page_link = soup.select_one('a[rel="next"]')  # Using CSS selector to find the next page link
            if next_page_link and next_page_link.get('href'):
                category_url = urljoin(category_url, next_page_link['href'])
            else:
                category_url = None  # No more pages to scrape

@router.get("/scrape-product-details")
def scrape_product_details(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    for product in products:
        soup = fetch_html(product.url)

        card = soup.find("div", class_="card")
        product_thumbnail = card.find("img", class_="img-responsive")["src"]
        product_description = card.find("p", class_="description").text.strip()
        product_price = card.find("h4", class_="price").text.strip().removeprefix("$")
        product_price = float(product_price)
        product_reviews = card.find("p", class_="review-count").text.split(' ')[0]

        if not get_product_detail_by_product_id(db, product.id):
            create_product_detail(db, ProductDetail(
                product_id=product.id, 
                thumbnail=product_thumbnail, 
                description=product_description, 
                price=product_price, 
                reviews_count=int(product_reviews)
            ))
            send_message("product_details", "new", {
                "product_id": product.id, 
                "thumbnail": product_thumbnail, 
                "description": product_description, 
                "price": product_price,
                "reviews_count": int(product_reviews)
            })
