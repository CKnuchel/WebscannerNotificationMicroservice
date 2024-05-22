from sqlalchemy.orm import Session
from .models import Category, Product, ProductDetail
from .schemas import CategoryCreate, ProductCreate, ProductDetailCreate

# CRUD operations for the Category
def create_category(db: Session, category: CategoryCreate):
    """
    This function is used to create a new category in the database.
    - Parameters:
        - db: The database session
        - category: The data required to create a new category
    - Returns:
        - The newly created category
    """
    db_category = Category(name=category.name, url=category.url, level=category.level)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category_by_category_id(db: Session, category_id: int):
    """
    This function is used to retrieve a category from the database.
    - Parameters:
        - db: The database session
        - category_id: The unique identifier of the category
    - Returns:
        - The category with the specified unique identifier
    """
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_name(db: Session, name: str):
    """
    This function is used to retrieve a category from the database.
    - Parameters:
        - db: The database session
        - name: The name of the category
    - Returns:
        - The category with the specified name
    """
    return db.query(Category).filter(Category.name == name).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """
    This function is used to retrieve a list of categories from the database.
    - Parameters:
        - db: The database session
        - skip: The number of categories to skip
        - limit: The maximum number of categories to return
    - Returns:
        - A list of categories
    """
    return db.query(Category).offset(skip).limit(limit).all()


# CRUD operations for the Product
def create_product(db: Session, product: ProductCreate):
    """
    This function is used to create a new product in the database.
    - Parameters:
        - db: The database session
        - product: The data required to create a new product
    - Returns:
        - The newly created product
    """
    db_product = Product(name=product.name, category_id=product.category_id, url=product.url)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product_by_product_id(db: Session, product_id: int):
    """
    This function is used to retrieve a product from the database.
    - Parameters:
        - db: The database session
        - product_id: The unique identifier of the product
    - Returns:
        - The product with the specified unique identifier
    """
    return db.query(Product).filter(Product.id == product_id).first()

def get_product_by_name(db: Session, name: str):
    """
    This function is used to retrieve a product from the database.
    - Parameters:
        - db: The database session
        - name: The name of the product
    - Returns:
        - The product with the specified name
    """
    return db.query(Product).filter(Product.name == name).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    """
    This function is used to retrieve a list of products from the database.
    - Parameters:
        - db: The database session
        - skip: The number of products to skip
        - limit: The maximum number of products to return
    - Returns:
        - A list of products
    """
    return db.query(Product).offset(skip).limit(limit).all()


# CRUD operations for the ProductDetail
def create_product_detail(db: Session, product_detail: ProductDetailCreate):
    """
    This function is used to create a new product detail in the database.
    - Parameters:
        - db: The database session
        - product_detail: The data required to create a new product detail
    - Returns:
        - The newly created product detail
    """
    db_product_detail = ProductDetail(
        product_id=product_detail.product_id, 
        description=product_detail.description, 
        image_url=product_detail.image_url, 
        price=product_detail.price, 
        options=product_detail.options, 
        reviews_count=product_detail.reviews_count)
    
    db.add(db_product_detail)
    db.commit()
    db.refresh(db_product_detail)
    return db_product_detail

def get_product_detail_by_product_id(db: Session, product_id: int):
    """
    This function is used to retrieve a product detail from the database.
    - Parameters:
        - db: The database session
        - product_id: The unique identifier of the product
    - Returns:
        - The product detail with the specified unique identifier
    """
    return db.query(ProductDetail).filter(ProductDetail.product_id == product_id).first()

def get_product_detail_by_name(db: Session, name: str):
    """
    This function is used to retrieve a product detail from the database.
    - Parameters:
        - db: The database session
        - name: The name of the product
    - Returns:
        - The product detail with the specified name
    """
    return db.query(ProductDetail).filter(ProductDetail.name == name).first()

def get_product_detail(db: Session, skip: int = 0, limit: int = 100):
    """
    This function is used to retrieve a list of product details from the database.
    - Parameters:
        - db: The database session
        - skip: The number of product details to skip
        - limit: The maximum number of product details to return
    - Returns:
        - A list of product details
    """
    return db.query(ProductDetail).offset(skip).limit(limit).all()