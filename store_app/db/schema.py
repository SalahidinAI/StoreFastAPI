from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from .models import StatusChoices


class UserProfileSchema(BaseModel):
    first_name: str
    username: str
    email: EmailStr
    age: Optional[int]
    phone_number: Optional[str]
    status: StatusChoices
    password: str

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    category_name: str

    class Config:
        from_attributes = True


class ProductSchema(BaseModel):
    product_name: str
    category_id: int
    price: int
    description: str
    check_original: bool
    product_video: Optional[str]
    created_date: datetime
    owner_id: int

    class Config:
        from_attributes = True


class ReviewSchema(BaseModel):
    author_id: int
    stars: Optional[int]
    comment: str
    product_id: int

    class Config:
        from_attributes = True


class CartItemSchema(BaseModel):
    id: int
    product_id: int

    class Config:
        from_attributes = True


class CartSchema(BaseModel):
    user_id: int
    items: List[CartItemSchema] = []
    total_price: int

    class Config:
        from_attributes = True


class CartItemCreateSchema(BaseModel):
    product_id: int

    class Config:
        from_attributes = True


class FavoriteItemSchema(BaseModel):
    id: int
    product_id: int

    class Config:
        from_attributes = True


class FavoriteSchema(BaseModel):
    user_id: int
    items: List[FavoriteItemSchema] = []

    class Config:
        from_attributes = True


class FavoriteItemCreateSchema(BaseModel):
    product_id: int

    class Config:
        from_attributes = True
