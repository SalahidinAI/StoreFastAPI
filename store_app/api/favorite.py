from store_app.db.models import Favorite, Product, UserProfile, CartItem, FavoriteItem
from store_app.db.schema import FavoriteItemSchema, FavoriteSchema, FavoriteItemCreateSchema
from store_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException

favorite_router = APIRouter(prefix='/favorite', tags=['Favorite'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@favorite_router.get('/', response_model=FavoriteSchema)
async def favorite_list(user_id: int, db: Session = Depends(get_db)):
    favorite_db = db.query(Favorite).filter(Favorite.user_id == user_id).first()
    if not favorite_db:
        raise HTTPException(status_code=404, detail='Favorite not found')
    return favorite_db


@favorite_router.post('/', response_model=FavoriteItemCreateSchema)
async def favorite_add(item_data: FavoriteItemCreateSchema, user_id: int,
                       db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    favorite_db = db.query(Favorite).filter(Favorite.user_id == user_id).first()
    if not favorite_db:
        favorite_db = Favorite(user_id=user_id)
        db.add(favorite_db)
        db.commit()
        db.refresh(favorite_db)

    product_db = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Product not found')

    favorite_item_db = db.query(FavoriteItem).filter(FavoriteItem.favorite_id == favorite_db.id,
                                                     FavoriteItem.product_id == item_data.product_id).first()
    if favorite_item_db:
        raise HTTPException(status_code=404, detail='Product already exists in Favorite')

    favorite_item_db = FavoriteItem(favorite_id=favorite_db.id, product_id=item_data.product_id)
    db.add(favorite_item_db)
    db.commit()
    db.refresh(favorite_item_db)
    return favorite_item_db


@favorite_router.delete('/{product_id}/')
async def favorite_delete(product_id: int, user_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Product not found')

    favorite_db = db.query(Favorite).filter(Favorite.user_id == user_id).first()
    if not favorite_db:
        raise HTTPException(status_code=404, detail='Favorite not found')

    favorite_item_db = db.query(FavoriteItem).filter(FavoriteItem.favorite_id == favorite_db.id,
                                                     FavoriteItem.product_id == product_id).first()
    if not favorite_item_db:
        raise HTTPException(status_code=404, detail='Product does not exist in Favorites')

    db.delete(favorite_item_db)
    db.commit()
    return {'message': 'Item is deleted'}
