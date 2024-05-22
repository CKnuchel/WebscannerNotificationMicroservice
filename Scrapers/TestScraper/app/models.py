from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    url = Column(String(255), unique=True, index=True)
    level = Column(String(25))

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    url = Column(String(255), unique=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")
    details = relationship("ProductDetail", back_populates="product")


class ProductDetail(Base):
    __tablename__ = "product_details"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    thumbnail = Column(String(255))
    description = Column(String(255))
    price = Column(String(25))
    options = Column(String(255))
    reviews_count = Column(String(25))

    product = relationship("Product", back_populates="details")
