from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    """Model um Benutzer zu speichern, welche nach ihrem Benutzernamen indiziert sind"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), index=True)

    subscriptions = relationship("Subscription", back_populates="user")

class Device_Token(Base):
    """Model um Geräte-Token zu speichern, welche nach ihrem Token indiziert sind"""
    __tablename__ = "device_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(100), index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="device_tokens")

class Category(Base):
    """Model um Kategorien zu speichern, welche nach ihrem Namen indiziert sind"""
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)

    products = relationship("Product", back_populates="category")

class Product(Base):
    """Model um Produkte zu speichern, welche nach ihrem Namen indiziert sind"""
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), index=True)
    
    # Entity links
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    # ...

    # Relationships
    category = relationship("Category", back_populates="subscriptions")
    product = relationship("Product", back_populates="subscriptions")
    user = relationship("User", back_populates="subscriptions")
    # ...
