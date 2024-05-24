from pydantic import BaseModel

# Schema for the Category
class CategoryBase(BaseModel):
    """
    The CategoryBaseModel schema is used to define the structure of the data that will be stored in the database.
    - Fields:
        - name: The name of the category
        - url: The URL of the category
    """
    name : str
    url : str
    level : str


class CategoryCreate(CategoryBase):
    """
    This Class is used to define the structure of the data that will be used to create a new category in the database.
    - Fields:
        - All fields from the CategoryBaseModel schema
    """
    pass # No additional fields are required for creating a new category


class Category(CategoryBase):
    """
    This Class is used to define the structure of the data that will be returned from the database.
    - Fields:
        - id: The unique identifier of the category
        - In addition all fields from the CategoryBaseModel schema
    """
    id : int
    # Inherit all fields from the CategoryBaseModel schema

    class Config:
        """
        The Config class is used to configure the behavior of the Pydantic model.
        - orm_mode: This attribute is set to True to allow the model to work with SQLAlchemy ORM models.
        """
        orm_mode = True



# Schema for the Product
class ProductBase(BaseModel):
    """
    The ProductBaseModel schema is used to define the structure of the data that will be stored in the database.
    - Fields:
        - name: The name of the product
        - category_id: The unique identifier of the category that the product belongs to
        - url: The URL of the product
    """
    name : str
    category_id : int
    url : str


class ProductCreate(ProductBase):
    """
    This Class is used to define the structure of the data that will be used to create a new product in the database.
    - Fields:
        - All fields from the ProductBaseModel schema
    """
    pass # No additional fields are required for creating a new product


class Product(ProductBase):
    """
    This Class is used to define the structure of the data that will be returned from the database.
    - Fields:
        - id: The unique identifier of the product
        - In addition all fields from the ProductBaseModel schema
    """
    id : int
    # inherit all fields from the ProductBaseModel schema

    class Config:
        """
        The Config class is used to configure the behavior of the Pydantic model.
        - orm_mode: This attribute is set to True to allow the model to work with SQLAlchemy ORM models.
        """
        orm_mode = True

    
# Schema for the ProductDetail
class ProductDetailBase(BaseModel):
    """
    The ProductDetailBaseModel schema is used to define the structure of the data that will be stored in the database.
    - Fields:
        - product_id: The unique identifier of the product that the detail belongs to
        - description: The description of the product
        - thumbnail: The URL of the product image
        - price: The price of the product
        - options: The options available for the product
        - reviews_count: The number of reviews for the product
    """
    product_id : int
    description : str
    thumbnail : str
    price : float
    reviews_count : int


class ProductDetailCreate(ProductDetailBase):
    """
    This Class is used to define the structure of the data that will be used to create a new product detail in the database.
    - Fields:
        - All fields from the ProductDetailBaseModel schema
    """
    pass # No additional fields are required for creating a new product detail


class ProductDetail(ProductDetailBase):
    """
    This Class is used to define the structure of the data that will be returned from the database.
    - Fields:
        - id: The unique identifier of the product detail
        - In addition all fields from the ProductDetailBaseModel schema
    """
    id : int
    # Inherit all fields from the ProductDetailBaseModel schema

    class Config:
        """
        The Config class is used to configure the behavior of the Pydantic model.
        - orm_mode: This attribute is set to True to allow the model to work with SQLAlchemy ORM models.
        """
        orm_mode = True