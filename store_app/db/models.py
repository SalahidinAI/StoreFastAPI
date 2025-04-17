from .database import Base
from sqlalchemy import Integer, String, Text, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional
from enum import Enum as PyEnum
from passlib.hash import bcrypt


class StatusChoices(str, PyEnum):
    gold = 'gold'
    silver = 'silver'
    bronze = 'bronze'
    simple = 'simple'


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    username: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(Enum(StatusChoices), default=StatusChoices.simple.value)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    owner_product: Mapped[List['Product']] = relationship('Product', back_populates='owner',
                                                          cascade='all, delete-orphan')
    author_review: Mapped[List['Review']] = relationship('Review', back_populates='author',
                                                         cascade='all, delete-orphan')
    user_cart: Mapped['Cart'] = relationship('Cart', back_populates='user',
                                             cascade='all, delete-orphan', uselist=False)

    favorite: Mapped['Favorite'] = relationship('Favorite', back_populates='user',
                                                cascade='all, delete-orphan', uselist=False)

    def set_passwords(self, password: str):
        self.hashed_password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile')

    def __repr__(self):
        return f'{self.user_id}'


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(32), unique=True)

    category_products: Mapped[List['Product']] = relationship('Product', back_populates='category',
                                                              cascade='all, delete-orphan')


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(64))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    price: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    check_original: Mapped[bool] = mapped_column(Boolean, default=False)
    product_video: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    owner_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))

    category: Mapped['Category'] = relationship('Category', back_populates='category_products')
    owner: Mapped['UserProfile'] = relationship('UserProfile', back_populates='owner_product')
    product_reviews: Mapped[List['Review']] = relationship('Review', back_populates='product',
                                                           cascade='all, delete-orphan')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    stars: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))

    author: Mapped['UserProfile'] = relationship('UserProfile', back_populates='author_review')
    product: Mapped['Product'] = relationship('Product', back_populates='product_reviews')


class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'), unique=True)

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='user_cart')
    items: Mapped[List['CartItem']] = relationship('CartItem', back_populates='cart',
                                                   cascade='all, delete-orphan')


class CartItem(Base):
    __tablename__ = 'cart_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))

    cart: Mapped['Cart'] = relationship('Cart', back_populates='items')
    product: Mapped['Product'] = relationship('Product')


class Favorite(Base):
    __tablename__ = 'favorite'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='favorite')
    items: Mapped[List['FavoriteItem']] = relationship('FavoriteItem', back_populates='favorite',
                                                       cascade='all, delete-orphan')


class FavoriteItem(Base):
    __tablename__ = 'favorite_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    favorite_id: Mapped[int] = mapped_column(ForeignKey('favorite.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))

    favorite: Mapped['Favorite'] = relationship('Favorite', back_populates='items')
    product: Mapped['Product'] = relationship('Product')
