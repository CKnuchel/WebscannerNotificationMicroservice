from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class DeviceTokenBase(BaseModel):
    token: str
    user_id: int

class DeviceTokenCreate(DeviceTokenBase):
    pass

class DeviceToken(DeviceTokenBase):
    id: int

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class SubscriptionBase(BaseModel):
    username: str
    category_id: int = None
    product_id: int = None

class SubscriptionCreate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    id: int

    class Config:
        orm_mode = True