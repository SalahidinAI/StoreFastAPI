from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from store_app.db.models import Category
from store_app.db.schema import CategorySchema
from store_app.db.database import SessionLocal, DB_URL
from sqlalchemy.orm import Session

category_router = APIRouter(prefix='/category', tags=['Categories'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@category_router.post('/', response_model=CategorySchema)
async def category_create(category: CategorySchema, db: Session = Depends(get_db)):
    category_db = Category(**category.dict())
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db


@category_router.get('/', response_model=List[CategorySchema])
async def category_list(db: Session = Depends(get_db)):
    return db.query(Category).all()


@category_router.get('/{category_id}/', response_model=CategorySchema)
async def category_detail(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if category_db is None:
        raise HTTPException(status_code=404, detail='Category not found')
    return category_db


@category_router.put('/{category_id}/', response_model=CategorySchema)
async def category_update(category_id: int, category: CategorySchema, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if category_db is None:
        raise HTTPException(status_code=404, detail='Category not found')
    category_db.category_name = category.category_name
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db


@category_router.delete('/{category_id}/')
async def category_delete(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if category_db is None:
        raise HTTPException(status_code=404, detail='Category not found')
    db.delete(category_db)
    db.commit()
    return {'message': 'it is deleted'}
