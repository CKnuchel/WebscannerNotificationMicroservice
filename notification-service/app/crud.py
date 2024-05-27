from sqlalchemy.orm import Session
from .models import Category, Product, Subscription, User, Device_Token
from .schemas import CategoryCreate, ProductCreate, SubscriptionCreate, UserCreate, DeviceTokenCreate

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
    db_category = Category(name=category.name)
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
    db_product = Product(name=product.name, category_id=product.category_id)
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


# CRUD operations for the Subscription
def create_subscription(db: Session, subscription: SubscriptionCreate):
    """
    This function is used to create a new subscription in the database.
    - Parameters:
        - db: The database session
        - subscription: The data required to create a new subscription
    - Returns:
        - The newly created subscription
    """
    db_subscription = Subscription(username=subscription.username, product_id=subscription.product_id)
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

def get_subscription_by_subscription_id(db: Session, subscription_id: int):
    """
    This function is used to retrieve a subscription from the database.
    - Parameters:
        - db: The database session
        - subscription_id: The unique identifier of the subscription
    - Returns:
        - The subscription with the specified unique identifier
    """
    return db.query(Subscription).filter(Subscription.id == subscription_id).first()

def get_subscriptions(db: Session, skip: int = 0, limit: int = 100):
    """
    This function is used to retrieve a list of subscriptions from the database.
    - Parameters:
        - db: The database session
        - skip: The number of subscriptions to skip
        - limit: The maximum number of subscriptions to return
    - Returns:
        - A list of subscriptions
    """
    return db.query(Subscription).offset(skip).limit(limit).all()

def get_subscriptions_by_product_id(db: Session, product_id: int):
    """
    This function is used to retrieve a list of subscriptions for a specific product from the database.
    - Parameters:
        - db: The database session
        - product_id: The unique identifier of the product
    - Returns:
        - A list of subscriptions for the specified product
    """
    return db.query(Subscription).filter(Subscription.product_id == product_id).all()

def get_subscriptions_by_category_id(db: Session, category_id: int):
    """
    This function is used to retrieve a list of subscriptions for a specific category from the database.
    - Parameters:
        - db: The database session
        - category_id: The unique identifier of the category
    - Returns:
        - A list of subscriptions for the specified category
    """
    return db.query(Subscription).filter(Subscription.category_id == category_id).all()

def get_subscriptions_by_username(db: Session, username: str):
    """
    This function is used to retrieve a list of subscriptions for a specific user from the database.
    - Parameters:
        - db: The database session
        - username: The username of the user
    - Returns:
        - A list of subscriptions for the specified user
    """
    return db.query(Subscription).filter(Subscription.username == username).all()

def get_subscriptions_by_username_and_category_id(db: Session, username: str, category_id: int):
    """
    This function is used to retrieve a list of subscriptions for a specific user and category from the database.
    - Parameters:
        - db: The database session
        - username: The username of the user
        - category_id: The unique identifier of the category
    - Returns:
        - A list of subscriptions for the specified user and category
    """
    return db.query(Subscription).filter(Subscription.username == username, Subscription.category_id == category_id).all()


# CRUD operations for the User
def create_user(db: Session, user: UserCreate):
    """
    This function is used to create a new user in the database.
    - Parameters:
        - db: The database session
        - user: The data required to create a new user
    - Returns:
        - The newly created user
    """
    db_user = User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    """
    This function is used to retrieve a user from the database.
    - Parameters:
        - db: The database session
        - username: The username of the user
    - Returns:
        - The user with the specified username
    """
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    This function is used to retrieve a list of users from the database.
    - Parameters:
        - db: The database session
        - skip: The number of users to skip
        - limit: The maximum number of users to return
    - Returns:
        - A list of users
    """
    return db.query(User).offset(skip).limit(limit).all()


# CRUD operations for the Device Token
def create_device_token(db: Session, device_token: DeviceTokenCreate):
    """
    This function is used to create a new device token in the database.
    - Parameters:
        - db: The database session
        - device_token: The data required to create a new device token
    - Returns:
        - The newly created device token
    """
    db_device_token = Device_Token(token=device_token.token, user_id=device_token.user_id)
    db.add(db_device_token)
    db.commit()
    db.refresh(db_device_token)
    return db_device_token

def get_device_token_by_user_id(db: Session, user_id: int):
    """
    This function is used to retrieve a device token from the database.
    - Parameters:
        - db: The database session
        - user_id: The unique identifier of the user
    - Returns:
        - The device token with the specified unique identifier
    """
    return db.query(Device_Token).filter(Device_Token.user_id == user_id).first()

def update_device_token_for_user_id(db: Session, user_id: int, device_token: str):
    """
    This function is used to update the device token for a specific user in the database.
    - Parameters:
        - db: The database session
        - user_id: The unique identifier of the user
        - device_token: The new device token
    - Returns:
        - The updated device token
    """
    db_device_token = db.query(Device_Token).filter(Device_Token.user_id == user_id).first()
    db_device_token.token = device_token
    db.commit()
    db.refresh(db_device_token)
    return db_device_token
