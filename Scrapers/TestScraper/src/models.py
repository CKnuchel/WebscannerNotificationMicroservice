from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from database import Base

# Database models

class Category(Base):
    __tablename__ = 'categories'

    # Columns
    id = Column(Integer, primary_key=True) # Primary key
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)

    # Relationships
    products = relationship('Product', back_populates='category') # One to many relationship with Product. One category can have many products


class Product(Base):
    __tablename__ = 'products'

    # Columns
    id = Column(Integer, primary_key=True) # Primary key
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False) # Foreign key to categories table
    url = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    # Relationships
    category = relationship('Category', back_populates='products') # Many to one relationship with Category. Many products can belong to one category
    details = relationship('ProductDetail', back_populates='product', uselist=False) # One to one relationship with ProductDetail. One product can have one detail


class ProductDetail(Base):
    __tablename__ = 'product_details'
    
    # Columns
    id = Column(Integer, primary_key=True) # Primary key
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False) # Foreign key to products table
    description = Column(Text, nullable=False)
    image_url = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    options = Column(Text, nullable=False) # Computers: HDD, Phones: Color
    reviews_count = Column(Integer, nullable=False) # Number of reviews

    # Relationships
    product = relationship('Product', back_populates='details') # One to one relationship with Product. One product can have one detail